#!/usr/bin/env python3
"""Offline checks for the GitHub profile. Run: python scripts/validate_profile.py

Besides the existing art and link checks, this validates the responsive
contract of the README: every wide piece of custom artwork must ship a
compact ``-mobile`` variant, that variant has to stay legible inside a
phone-width README column, and no label may be drawn outside its canvas.
"""

from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
SVG_NS = "{http://www.w3.org/2000/svg}"

# A GitHub README column is ~358 CSS px wide on a phone and ~890 CSS px wide
# on a desktop browser. Shares describe how much of that column each artwork
# occupies (1.0 = full width, 0.49 = the two-up project card grid).
PHONE_COLUMN_PX = 358
DESKTOP_COLUMN_PX = 890

# desktop artwork: (desktop share, compact share, breakpoint in CSS px)
#
# The hero and the rules only need help on phones, so they switch at 640. The
# text-dense pieces (terminal strip, toolkit grid, project cards) drop below
# ~10 px type somewhere between 640 and 768, so they switch at the tablet
# breakpoint instead.
RESPONSIVE_ART = {
    "header.svg": (1.0, 1.0, 640),
    "divider.svg": (1.0, 1.0, 640),
    "assets/typing-banner.svg": (1.0, 1.0, 768),
    "assets/toolkit-matrix.svg": (1.0, 1.0, 768),
    # The project grid stays two-up on phones, so the compact tiles are drawn
    # for the same 49% slot rather than for the full column.
    "assets/card-zeromind.svg": (0.49, 0.49, 768),
    "assets/card-backup-tools.svg": (0.49, 0.49, 768),
    "assets/card-in-app-update.svg": (0.49, 0.49, 768),
    "assets/card-icon-converter.svg": (0.49, 0.49, 768),
}

# Type should never shrink below this when rendered on a phone.
MIN_RENDERED_FONT_PX = 4.5

DECORATIVE_SVGS = {"divider.svg", "divider-mobile.svg", "footer-wave.svg"}


def mobile_variant(rel_path):
    return rel_path[: -len(".svg")] + "-mobile.svg"


class Images(HTMLParser):
    """Collects <img>, <source> and <picture> structure from the README."""

    def __init__(self):
        super().__init__()
        self.images = []
        self.sources = []
        self.pictures = []
        self._stack = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img":
            self.images.append(attrs)
        if tag == "source":
            self.sources.append(attrs)
        if tag == "picture":
            self._stack = {"sources": [], "images": []}
        elif self._stack is not None:
            if tag == "source":
                self._stack["sources"].append(attrs)
            elif tag == "img":
                self._stack["images"].append(attrs)

    def handle_endtag(self, tag):
        if tag == "picture" and self._stack is not None:
            self.pictures.append(self._stack)
            self._stack = None


def viewbox_size(path):
    root = ET.parse(path).getroot()
    values = root.attrib["viewBox"].split()
    return float(values[2]), float(values[3])


def to_float(value, fallback):
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def is_text_tag(tag):
    return tag in {SVG_NS + "text", SVG_NS + "tspan"}


def walk(root):
    """Yield (element, ancestors) for every element, skipping <defs>."""
    def recurse(element, ancestors):
        for child in element:
            if child.tag == SVG_NS + "defs":
                continue
            yield child, ancestors
            yield from recurse(child, ancestors + [child])

    yield from recurse(root, [])


def inherited(ancestors, element, name, default=None):
    for holder in reversed(ancestors + [element]):
        if name in holder.attrib:
            return holder.attrib[name]
    return default


def translate_of(ancestors):
    """Absolute offset contributed by ancestor groups (a <text> x/y is pre-transform)."""
    x = y = 0.0
    for holder in ancestors:
        match = re.match(r"translate\(\s*(-?[\d.]+)[\s,]*(-?[\d.]+)?\s*\)", holder.attrib.get("transform", ""))
        if match:
            x += float(match.group(1))
            y += float(match.group(2) or 0)
    return x, y


def font_units(text, font_size, weight, family, letter_spacing):
    """Conservative average advance width per character, in em."""
    if "monospace" in family or "SFMono" in family or "Consolas" in family:
        units = 0.601
    elif str(weight) in {"600", "700", "800", "bold", "900"}:
        units = 0.585
    else:
        units = 0.53
    return len(text) * font_size * units + len(text) * letter_spacing


def text_bounds(run):
    """Estimated ink box for a text run: (left, top, right, bottom)."""
    x, y, sizes, width, anchor, content = run[:6]
    size = max(sizes) if sizes else 16.0
    if anchor == "middle":
        left, right = x - width / 2, x + width / 2
    elif anchor == "end":
        left, right = x - width, x
    else:
        left, right = x, x + width
    return left, y - size * 0.78, right, y + size * 0.24


def overlaps(a, b, slack=0.0):
    return (
        a[0] < b[2] - slack
        and b[0] < a[2] - slack
        and a[1] < b[3] - slack
        and b[1] < a[3] - slack
    )


def is_alternate_state(ancestors, element):
    """True when the run belongs to a group that fades in and out (cycling text states).

    Only the run itself and its immediate parent count: an opacity animation deep
    inside a shared ancestor (a blinking cursor, say) does not make every sibling
    label an alternate state.
    """
    holders = [element] + ancestors[-1:]
    for holder in holders:
        for anim in holder:
            if anim.tag == SVG_NS + "animate" and anim.attrib.get("attributeName") == "opacity":
                return True
    return False


def svg_texts(path):
    """Return [(abs_x, abs_y, font_sizes, estimated_width, anchor, content, cycling)] per run."""
    root = ET.parse(path).getroot()
    runs = []
    for element, ancestors in walk(root):
        if element.tag != SVG_NS + "text":
            continue
        dx, dy = translate_of(ancestors)
        family = inherited(ancestors, element, "font-family", "")
        weight = inherited(ancestors, element, "font-weight", "400")
        size = to_float(inherited(ancestors, element, "font-size", "16"), 16.0)
        spacing = to_float(inherited(ancestors, element, "letter-spacing", "0"), 0.0)
        anchor = inherited(ancestors, element, "text-anchor", "start")
        x = float(element.attrib.get("x", 0)) + dx
        y = float(element.attrib.get("y", 0)) + dy

        # A <text> may mix plain characters with styled <tspan> runs.
        chunks = [(element.text or "", size)]
        for child in element:
            if child.tag == SVG_NS + "tspan":
                child_size = to_float(child.attrib.get("font-size"), size)
                chunks.append((child.text or "", child_size))
                if child.tail:
                    chunks.append((child.tail, size))
        # Source indentation around a multi-line <text> is not rendered, so drop it.
        stripped = [(chunk, chunk_size) for chunk, chunk_size in chunks]
        if stripped:
            stripped[0] = (stripped[0][0].lstrip(), stripped[0][1])
            stripped[-1] = (stripped[-1][0].rstrip(), stripped[-1][1])
        stripped = [(chunk, chunk_size) for chunk, chunk_size in stripped if chunk]

        content = "".join(chunk for chunk, _ in stripped).strip()
        sizes = sorted({chunk_size for _, chunk_size in stripped})
        width = sum(font_units(chunk, chunk_size, weight, family, spacing) for chunk, chunk_size in stripped)
        runs.append((x, y, sizes, width, anchor, content, is_alternate_state(ancestors, element)))
    return runs


class ProfileChecks(unittest.TestCase):
    def setUp(self):
        self.html = Images()
        self.html.feed(README)

    def test_local_images_exist(self):
        sources = [i["src"] for i in self.html.images]
        sources += [s["srcset"] for s in self.html.sources]
        for source in sources:
            with self.subTest(source=source):
                if urlsplit(source).scheme:
                    self.assertEqual(urlsplit(source).scheme, "https")
                else:
                    self.assertTrue((ROOT / source).is_file(), source)

    def test_images_have_alt_text(self):
        for image in self.html.images:
            self.assertIn("alt", image)
            if image["src"] not in DECORATIVE_SVGS:
                self.assertTrue(image["alt"].strip())

    def test_svg_integrity(self):
        svg_paths = sorted(list(ROOT.glob("*.svg")) + list((ROOT / "assets").glob("*.svg")))
        for path in svg_paths:
            with self.subTest(path=str(path.relative_to(ROOT))):
                root = ET.parse(path).getroot()
                self.assertEqual(root.tag, SVG_NS + "svg")
                self.assertEqual(len(root.attrib["viewBox"].split()), 4)
                self.assertFalse(list(root.iter(SVG_NS + "script")))
                ids = [e.attrib["id"] for e in root.iter() if "id" in e.attrib]
                self.assertEqual(len(ids), len(set(ids)), "Duplicate SVG IDs")
                for ref in re.findall(r"url\(#([^)]*)\)", path.read_text()):
                    self.assertIn(ref, ids, "Missing SVG paint or clip reference")

    def test_navigation_targets_exist(self):
        headings = {
            re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-")
            for title in re.findall(r"^## (.+)$", README, re.MULTILINE)
        }
        for target in re.findall(r"\]\(#([^)]*)\)", README):
            self.assertIn(target, headings)

    def test_custom_svgs_have_animations(self):
        animated_svgs = sorted(
            set(RESPONSIVE_ART)
            | {mobile_variant(p) for p in RESPONSIVE_ART}
            | {"footer-wave.svg", "profile-frame.svg"}
        )
        anim_tags = {
            SVG_NS + "animate",
            SVG_NS + "animateTransform",
            SVG_NS + "animateMotion",
        }
        for rel_path in animated_svgs:
            with self.subTest(svg=rel_path):
                root = ET.parse(ROOT / rel_path).getroot()
                found = [el for el in root.iter() if el.tag in anim_tags]
                self.assertGreater(len(found), 0, f"Expected animations in {rel_path}")

    def test_avatar_is_a_jpeg(self):
        data = (ROOT / "assets/avatar.jpg").read_bytes()
        self.assertTrue(data.startswith(b"\xff\xd8\xff"))
        self.assertTrue(data.endswith(b"\xff\xd9"))

    # ------------------------------------------------------------------
    # Responsive layout checks
    # ------------------------------------------------------------------

    def test_mobile_variants_exist(self):
        for rel_path, (_desktop, _mobile, _bp) in RESPONSIVE_ART.items():
            variant = mobile_variant(rel_path)
            with self.subTest(svg=variant):
                self.assertTrue((ROOT / variant).is_file(), f"Missing compact artwork: {variant}")
                width, _ = viewbox_size(ROOT / variant)
                desktop_width, _ = viewbox_size(ROOT / rel_path)
                self.assertLessEqual(
                    width,
                    760,
                    "Compact artwork should use a narrow canvas so type scales up on phones",
                )
                self.assertLess(width, desktop_width)

    def test_readme_uses_picture_sources_for_responsive_art(self):
        media_by_srcset = {s["srcset"]: s.get("media") for s in self.html.sources}
        for rel_path, (_desktop, _mobile, breakpoint_px) in RESPONSIVE_ART.items():
            variant = mobile_variant(rel_path)
            with self.subTest(svg=rel_path):
                self.assertIn(variant, media_by_srcset, f"{variant} is never served to small screens")
                self.assertEqual(
                    media_by_srcset.get(variant),
                    f"(max-width: {breakpoint_px}px)",
                    f"{variant} should be served below {breakpoint_px}px",
                )
                self.assertIn(rel_path, [i["src"] for i in self.html.images], f"{rel_path} lost its fallback <img>")

        # Every <picture> must fall back to a plain image and offer a media condition.
        for index, picture in enumerate(self.html.pictures):
            with self.subTest(picture=index):
                self.assertEqual(len(picture["images"]), 1, "<picture> needs exactly one fallback <img>")
                self.assertTrue(picture["sources"], "<picture> without <source> is pointless")
                self.assertTrue(all("media" in s for s in picture["sources"]))
                self.assertTrue(all(s.get("srcset") for s in picture["sources"]))

    def test_mobile_artwork_stays_legible_on_a_phone(self):
        """Compact art must render its smallest label at least as large as the desktop art."""
        for rel_path, (desktop_share, mobile_share, _bp) in RESPONSIVE_ART.items():
            variant = mobile_variant(rel_path)
            desktop_width, _ = viewbox_size(ROOT / rel_path)
            mobile_width, _ = viewbox_size(ROOT / variant)
            desktop_sizes = [size for run in svg_texts(ROOT / rel_path) if run[5] for size in run[2]]
            mobile_sizes = [size for run in svg_texts(ROOT / variant) if run[5] for size in run[2]]

            with self.subTest(svg=variant):
                if not desktop_sizes:
                    self.assertEqual(mobile_sizes, [], "Decorative art gained text in the compact variant")
                    continue
                self.assertTrue(mobile_sizes, f"No text found in {variant}")
                desktop_px = min(desktop_sizes) * DESKTOP_COLUMN_PX * desktop_share / desktop_width
                mobile_px = min(mobile_sizes) * PHONE_COLUMN_PX * mobile_share / mobile_width
                self.assertGreaterEqual(mobile_px, MIN_RENDERED_FONT_PX)
                self.assertGreaterEqual(
                    mobile_px,
                    desktop_px,
                    f"{variant}: smallest label renders at {mobile_px:.1f}px on a phone, "
                    f"worse than the desktop artwork at {desktop_px:.1f}px",
                )

    def test_no_text_overflows_its_canvas(self):
        svg_paths = sorted(list(ROOT.glob("*.svg")) + list((ROOT / "assets").glob("*.svg")))
        tolerance = 6.0  # estimated glyph metrics are approximate
        for path in svg_paths:
            if "contribution-grid-snake" in path.name:
                continue  # generated by the snake workflow
            canvas_width, canvas_height = viewbox_size(path)
            for x, y, _, width, anchor, content, _cycling in svg_texts(path):
                if not content:
                    continue
                if anchor == "middle":
                    left, right = x - width / 2, x + width / 2
                elif anchor == "end":
                    left, right = x - width, x
                else:
                    left, right = x, x + width
                with self.subTest(svg=str(path.relative_to(ROOT)), text=content[:32]):
                    self.assertLessEqual(
                        right,
                        canvas_width + tolerance,
                        f'"{content[:40]}" is estimated to run past the right edge',
                    )
                    self.assertGreaterEqual(left, -tolerance, f'"{content[:40]}" starts left of the canvas')
                    self.assertLessEqual(y, canvas_height + tolerance, f'"{content[:40]}" sits below the canvas')


    def test_text_labels_do_not_collide(self):
        """Guard against artwork where two labels are drawn on top of each other."""
        svg_paths = sorted(list(ROOT.glob("*.svg")) + list((ROOT / "assets").glob("*.svg")))
        for path in svg_paths:
            if "contribution-grid-snake" in path.name:
                continue
            runs = [run for run in svg_texts(path) if run[5] and not run[6]]
            boxes = [(run[5], text_bounds(run)) for run in runs]
            for i, (first_text, first) in enumerate(boxes):
                for second_text, second in boxes[i + 1 :]:
                    if not overlaps(first, second, slack=1.0):
                        continue
                    with self.subTest(svg=str(path.relative_to(ROOT)), pair=(first_text[:24], second_text[:24])):
                        self.fail(
                            f'"{first_text[:40]}" and "{second_text[:40]}" overlap in '
                            f"{path.relative_to(ROOT)}"
                        )

    def test_artwork_content_stays_inside_the_frame(self):
        """Every drawn box must sit inside the rounded frame, with a small margin."""
        svg_paths = sorted(list(ROOT.glob("*.svg")) + list((ROOT / "assets").glob("*.svg")))
        for path in svg_paths:
            if "contribution-grid-snake" in path.name or path.name == "footer-wave.svg":
                continue
            canvas_width, canvas_height = viewbox_size(path)
            margin = 0.5
            root = ET.parse(path).getroot()
            for element, ancestors in walk(root):
                if element.tag != SVG_NS + "rect":
                    continue
                if element.attrib.get("fill") == "none" and not element.attrib.get("width"):
                    continue
                width = to_float(element.attrib.get("width"), None)
                height = to_float(element.attrib.get("height"), None)
                if width is None or height is None:
                    continue
                # Full-bleed backgrounds and off-canvas animation frames are intentional.
                if width >= canvas_width or height >= canvas_height:
                    continue
                dx, dy = translate_of(ancestors)
                left = to_float(element.attrib.get("x"), 0.0) + dx
                top = to_float(element.attrib.get("y"), 0.0) + dy
                if left < 0 or top < 0:  # shimmer beams travel from off-canvas
                    continue
                with self.subTest(svg=str(path.relative_to(ROOT)), rect=(left, top, width, height)):
                    self.assertLessEqual(left + width, canvas_width - margin)
                    self.assertLessEqual(top + height, canvas_height - margin)


if __name__ == "__main__":
    unittest.main(verbosity=2)
