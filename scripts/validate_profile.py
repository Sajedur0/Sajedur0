#!/usr/bin/env python3
"""Offline checks for the GitHub profile. Run: python3 scripts/validate_profile.py

Validates:
- All local SVG/JPEG image references, alt text, and anchor links
- SVG XML integrity, unique IDs, valid url(#...) paint/clip references, and SMIL animations
- Responsive <picture> contract: every wide artwork ships a compact -mobile variant,
  stays legible on a 358px phone column, never overflows its canvas, and has no colliding labels
- Clean non-programmer/non-developer content contract across README and all SVGs
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

PHONE_COLUMN_PX = 358
DESKTOP_COLUMN_PX = 890

GRID_CARDS = [
    "assets/card-zeromind.svg",
    "assets/card-backup-tools.svg",
    "assets/card-temp-cleaner.svg",
    "assets/card-icon-converter.svg",
    "assets/card-speed-meter.svg",
    "assets/card-payroll.svg",
    "assets/card-frp.svg",
    "assets/card-excel-cleaner.svg",
    "assets/card-photos-remover.svg",
    "assets/card-sdk-installer.svg",
    "assets/card-play-scraper.svg",
    "assets/card-in-app-update.svg",
    "assets/card-pc-software.svg",
    "assets/card-privacy-hub.svg",
]

PLAY_STORE_ICONS = {
    "assets/icons/router-page-setup.png": "Router Page Setup",
    "assets/icons/apk-organizer.png": "APK Organizer",
    "assets/icons/disk-partition-calculator.png": "Disk Partition Calculator",
    "assets/icons/mic-to-speaker.png": "Mic to Speaker",
    "assets/icons/pinsaver.png": "PinSaver",
}

RESPONSIVE_ART = {
    "header.svg": (1.0, 1.0, 640),
    "divider.svg": (1.0, 1.0, 640),
    **{path: (0.49, 0.49, 768) for path in GRID_CARDS},
}

MIN_RENDERED_FONT_PX = 4.5
DECORATIVE_SVGS = {"divider.svg", "divider-mobile.svg", "footer-wave.svg"}

FORBIDDEN_JARGON = (
    r"\bprogrammer\b",
    r"\bdeveloper\b",
    r"\bcoder\b",
    r"\bcoding\b",
    r"\bsoftware engineer\b",
    r"\bflutter\b",
    r"\bdart\b",
    r"\brust\b",
    r"\bpython\b",
    r"\btypescript\b",
    r"\bjavascript\b",
    r"\bpowershell\b",
    r"\bc\+\+",
    r"\bc#",
    r"\bthe_builder\b",
    r"\bview source\b",
    r"\bcommit history\b",
    r"\bnull safety\b",
    r"\bhello world\b",
)


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
    x = y = 0.0
    for holder in ancestors:
        match = re.match(r"translate\(\s*(-?[\d.]+)[\s,]*(-?[\d.]+)?\s*\)", holder.attrib.get("transform", ""))
        if match:
            x += float(match.group(1))
            y += float(match.group(2) or 0)
    return x, y


def font_units(text, font_size, weight, family, letter_spacing):
    if "monospace" in family or "SFMono" in family or "Consolas" in family:
        units = 0.601
    elif str(weight) in {"600", "700", "800", "bold", "900"}:
        units = 0.585
    else:
        units = 0.53
    return len(text) * font_size * units + len(text) * letter_spacing


def text_bounds(run):
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
    holders = [element] + ancestors[-1:]
    for holder in holders:
        for anim in holder:
            if anim.tag == SVG_NS + "animate" and anim.attrib.get("attributeName") == "opacity":
                return True
    return False


def svg_texts(path):
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

        chunks = [(element.text or "", size)]
        for child in element:
            if child.tag == SVG_NS + "tspan":
                child_size = to_float(child.attrib.get("font-size"), size)
                chunks.append((child.text or "", child_size))
                if child.tail:
                    chunks.append((child.tail, size))
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

    def test_no_orphan_svgs(self):
        raw_used = {i["src"] for i in self.html.images} | {s["srcset"] for s in self.html.sources}
        used = {s for s in raw_used if not urlsplit(s).scheme and s.endswith(".svg")}
        all_svgs = {
            str(p.relative_to(ROOT))
            for p in list(ROOT.glob("*.svg")) + list((ROOT / "assets").glob("*.svg"))
        }
        self.assertEqual(all_svgs, used, f"Unused SVGs in repo: {sorted(all_svgs - used)}")

    def test_google_play_apps_use_clickable_png_icons(self):
        self.assertEqual(list((ROOT / "assets").glob("app-*.svg")), [])
        for icon_path, app_name in PLAY_STORE_ICONS.items():
            with self.subTest(app=app_name):
                data = (ROOT / icon_path).read_bytes()
                self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))
                width = int.from_bytes(data[16:20], "big")
                height = int.from_bytes(data[20:24], "big")
                self.assertEqual((width, height), (256, 256))
                pattern = (
                    r'<a href="https://play\.google\.com/store/apps/[^"]+">'
                    r'<img src="' + re.escape(icon_path) + r'"[^>]+/>'
                    r"<br /><b>" + re.escape(app_name) + r"</b></a>"
                )
                self.assertRegex(README, pattern)

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
                for ref in re.findall(r"url\(#([^)]*)\)", path.read_text(encoding="utf-8")):
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
            | {"footer-wave.svg"}
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

    def test_mobile_variants_exist(self):
        for rel_path, (_desktop, _mobile, _bp) in RESPONSIVE_ART.items():
            variant = mobile_variant(rel_path)
            with self.subTest(svg=variant):
                self.assertTrue((ROOT / variant).is_file(), f"Missing compact artwork: {variant}")
                width, _ = viewbox_size(ROOT / variant)
                desktop_width, _ = viewbox_size(ROOT / rel_path)
                self.assertLessEqual(width, 760)
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
                )
                self.assertIn(rel_path, [i["src"] for i in self.html.images])

        for index, picture in enumerate(self.html.pictures):
            with self.subTest(picture=index):
                self.assertEqual(len(picture["images"]), 1)
                self.assertTrue(picture["sources"])
                self.assertTrue(all("media" in s for s in picture["sources"]))
                self.assertTrue(all(s.get("srcset") for s in picture["sources"]))

    def test_mobile_artwork_stays_legible_on_a_phone(self):
        for rel_path, (desktop_share, mobile_share, _bp) in RESPONSIVE_ART.items():
            variant = mobile_variant(rel_path)
            desktop_width, _ = viewbox_size(ROOT / rel_path)
            mobile_width, _ = viewbox_size(ROOT / variant)
            desktop_sizes = [size for run in svg_texts(ROOT / rel_path) if run[5] for size in run[2]]
            mobile_sizes = [size for run in svg_texts(ROOT / variant) if run[5] for size in run[2]]

            with self.subTest(svg=variant):
                if not desktop_sizes:
                    self.assertEqual(mobile_sizes, [])
                    continue
                self.assertTrue(mobile_sizes, f"No text found in {variant}")
                desktop_px = min(desktop_sizes) * DESKTOP_COLUMN_PX * desktop_share / desktop_width
                mobile_px = min(mobile_sizes) * PHONE_COLUMN_PX * mobile_share / mobile_width
                self.assertGreaterEqual(mobile_px, MIN_RENDERED_FONT_PX)
                self.assertGreaterEqual(
                    mobile_px,
                    desktop_px,
                    f"{variant}: smallest label renders at {mobile_px:.1f}px on a phone, "
                    f"worse than desktop at {desktop_px:.1f}px",
                )

    def test_no_text_overflows_its_canvas(self):
        svg_paths = sorted(list(ROOT.glob("*.svg")) + list((ROOT / "assets").glob("*.svg")))
        tolerance = 6.0
        for path in svg_paths:
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
                        f'"{content[:40]}" runs past the right edge ({right:.1f} > {canvas_width})',
                    )
                    self.assertGreaterEqual(left, -tolerance)
                    self.assertLessEqual(y, canvas_height + tolerance)

    def test_text_labels_do_not_collide(self):
        svg_paths = sorted(list(ROOT.glob("*.svg")) + list((ROOT / "assets").glob("*.svg")))
        for path in svg_paths:
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
        svg_paths = sorted(list(ROOT.glob("*.svg")) + list((ROOT / "assets").glob("*.svg")))
        for path in svg_paths:
            if path.name == "footer-wave.svg":
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
                if width >= canvas_width or height >= canvas_height:
                    continue
                dx, dy = translate_of(ancestors)
                left = to_float(element.attrib.get("x"), 0.0) + dx
                top = to_float(element.attrib.get("y"), 0.0) + dy
                if left < 0 or top < 0:
                    continue
                with self.subTest(svg=str(path.relative_to(ROOT)), rect=(left, top, width, height)):
                    self.assertLessEqual(left + width, canvas_width - margin)
                    self.assertLessEqual(top + height, canvas_height - margin)

    def test_no_programmer_or_developer_jargon(self):
        for pattern in FORBIDDEN_JARGON:
            with self.subTest(source="README.md", pattern=pattern):
                self.assertIsNone(re.search(pattern, README, re.IGNORECASE))

        svg_paths = sorted(list(ROOT.glob("*.svg")) + list((ROOT / "assets").glob("*.svg")))
        for path in svg_paths:
            root = ET.parse(path).getroot()
            texts = [el.text or "" for el in root.iter() if el.tag in {SVG_NS + "title", SVG_NS + "desc"}]
            texts += [run[5] for run in svg_texts(path)]
            joined = "\n".join(texts)
            for pattern in FORBIDDEN_JARGON:
                with self.subTest(source=str(path.relative_to(ROOT)), pattern=pattern):
                    self.assertIsNone(re.search(pattern, joined, re.IGNORECASE))


if __name__ == "__main__":
    unittest.main(verbosity=2)
