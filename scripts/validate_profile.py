#!/usr/bin/env python3
"""Offline checks for the GitHub profile. Run: python scripts/validate_profile.py"""

from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
SVG_NS = "{http://www.w3.org/2000/svg}"


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.sources = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img":
            self.images.append(attrs)
        if tag == "source":
            self.sources.append(attrs)


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
            if image["src"] not in {"divider.svg", "footer-wave.svg"}:
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
        animated_svgs = [
            "header.svg",
            "profile-frame.svg",
            "divider.svg",
            "footer-wave.svg",
            "assets/typing-banner.svg",
            "assets/card-zeromind.svg",
            "assets/card-backup-tools.svg",
            "assets/card-in-app-update.svg",
            "assets/card-icon-converter.svg",
            "assets/toolkit-matrix.svg",
        ]
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
