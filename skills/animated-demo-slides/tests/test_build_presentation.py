"""Standard-library regression tests for the presentation generator."""

import base64
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "build_presentation.py"
sys.path.insert(0, str(SCRIPT.parent))

from build_presentation import build_presentation, generate_html, svg_to_base64_uri

FIXTURE = json.loads(
    (SKILL_DIR / "evals" / "fixtures" / "reference-deck.json").read_text(encoding="utf-8")
)


class Elements(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.elements = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def find(self, tag):
        return [attrs for name, attrs in self.elements if name == tag]


class RenderingTests(unittest.TestCase):
    def test_legacy_raw_and_documented_base64_formats(self):
        svg = FIXTURE["slides"][0]["svg"]
        encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
        uri = "data:image/svg+xml;base64," + encoded
        for content in (svg, encoded, uri):
            with self.subTest(content=content[:30]):
                self.assertEqual(svg_to_base64_uri(content), uri)
                html = generate_html("Legacy deck", [{"name": "Legacy slide", "svg": content}])
                self.assertIn("Legacy slide</h2>", html)
                self.assertIn(uri, html)

    def test_preserves_all_slides_and_exact_approved_text(self):
        html = generate_html(FIXTURE["title"], FIXTURE["slides"])
        elements = Elements(html)
        self.assertEqual(len(elements.find("section")), len(FIXTURE["slides"]))
        for slide in FIXTURE["slides"]:
            self.assertIn(escape(slide["title"]), html)
            self.assertIn(escape(slide["description"]), html)
            self.assertIn(escape(slide["notes"]), html)
            for qualification in slide["qualifications"]:
                self.assertIn(f"<li>{escape(qualification)}</li>", html)
        self.assertTrue(all("hidden" not in item for item in elements.find("section")))

    def test_reference_is_native_visible_equivalent_and_commit_pinned(self):
        html = generate_html(FIXTURE["title"], FIXTURE["slides"])
        reference = FIXTURE["slides"][0]["references"][0]
        links = [
            item for item in Elements(html).find("a") if item["href"] == reference["url"]
        ]
        self.assertEqual(len(links), 3)  # Hotspot, reader/slide list, notes.
        hotspot = next(item for item in links if item.get("class") == "hotspot")
        self.assertEqual(hotspot["style"], "left:8%;top:12%;width:40%;height:28%")
        self.assertEqual(hotspot["aria-label"], f"Ref 1: {reference['label']}")
        self.assertTrue(all(item["rel"] == "noopener noreferrer" for item in links))
        self.assertIn(f'<span class="source-url">{reference["url"]}</span>', html)

    def test_text_and_urls_cannot_break_out_of_their_html_context(self):
        slides = copy.deepcopy(FIXTURE["slides"])
        text = '<script>alert("not markup")</script> & exact "\u00e9"'
        slides[0].update(title=text, description=text, notes=text, qualifications=[text])
        slides[0]["references"][0].update(
            label=text, url='https://example.org/source?term="literal"&mode=read#section'
        )
        html = generate_html(text, slides)
        self.assertNotIn(text, html)
        self.assertIn(escape(text), html)
        self.assertEqual(len(Elements(html).find("script")), 1)
        self.assertEqual(
            Elements(html).find("a")[0]["href"], slides[0]["references"][0]["url"]
        )

    def test_motion_alternative_and_honest_fallback(self):
        html = generate_html(FIXTURE["title"], FIXTURE["slides"])
        self.assertEqual(
            len(Elements(html).find("source")),
            sum("static_svg" in slide for slide in FIXTURE["slides"]),
        )
        self.assertIn("Animated diagram hidden for reduced motion.", html)
        html = generate_html("Legacy", [{"svg": FIXTURE["slides"][0]["svg"]}])
        self.assertIn("No text description was supplied", html)

    def test_no_url_navigation_or_external_runtime_dependencies(self):
        html = generate_html(FIXTURE["title"], FIXTURE["slides"])
        script = html.split("<script>", 1)[1].split("</script>", 1)[0]
        for operation in ("history.", "location.", "fetch(", "XMLHttpRequest", "window.open"):
            self.assertNotIn(operation, script)
        elements = Elements(html)
        self.assertFalse(any("src" in item for item in elements.find("script")))
        self.assertFalse(elements.find("link"))
        self.assertTrue(all(not item["href"].startswith("#") for item in elements.find("a")))
        self.assertTrue(any(item.get("id") == "skip" for item in elements.find("button")))

    def test_rejects_invalid_input_without_success_shaped_empty_deck(self):
        cases = [
            ("title", {"title": None, "slides": FIXTURE["slides"]}),
            ("slides", {"title": "Deck", "slides": []}),
            ("slides", {"title": "Deck", "slides": {}}),
            ("object", {"title": "Deck", "slides": ["not a slide"]}),
            ("svg", {"title": "Deck", "slides": [{}]}),
            ("SVG", {"title": "Deck", "slides": [{"svg": "<div/>"}]}),
            ("SVG", {"title": "Deck", "slides": [{"svg": "<svg>"}]}),
            ("base64", {"title": "Deck", "slides": [{"svg": "not base64"}]}),
            ("viewBox", {"title": "Deck", "slides": [{"svg": '<svg viewBox="0 0 0 450"/>'}]}),
            ("viewBox", {"title": "Deck", "slides": [{"svg": '<svg viewBox="0 0 wide tall"/>'}]}),
            ("viewBox", {"title": "Deck", "slides": [{"svg": '<svg viewBox="0 0 inf 450"/>'}]}),
        ]
        for message, data in cases:
            with self.subTest(data=data):
                with self.assertRaisesRegex(ValueError, message):
                    generate_html(data["title"], data["slides"])

    def test_validates_reference_and_caveat_shapes(self):
        reference = FIXTURE["slides"][0]["references"][0]
        invalid_updates = [
            {"qualifications": "not a list"}, {"qualifications": [""]},
            {"description": None}, {"references": {}}, {"references": [None]},
            {"references": [{"label": "", "url": "https://example.org"}]},
            {"references": [{"label": "Source", "url": "javascript:alert(1)"}]},
            {"references": [{"label": "Source", "url": "//example.org"}]},
            {"references": [{"label": "Source", "url": "https://:443/design"}]},
            {"references": [{"label": "Source", "url": "https://example.org/a b"}]},
            {"references": [{**reference, "region": {"x": 90, "y": 0, "width": 20, "height": 20}}]},
            {"references": [{**reference, "region": {"x": 0, "y": 0, "width": 0, "height": 20}}]},
            {"references": [{**reference, "region": {"x": True, "y": 0, "width": 20, "height": 20}}]},
            {"references": [{**reference, "region": {"x": float("nan"), "y": 0, "width": 20, "height": 20}}]},
            {"references": [{**reference, "region": {"x": 0, "y": 0, "width": float("inf"), "height": 20}}]},
            {"references": [{**reference, "region": {"x": 10**400, "y": 0, "width": 20, "height": 20}}]},
        ]
        for update in invalid_updates:
            with self.subTest(update=update):
                with self.assertRaises(ValueError):
                    generate_html("Deck", [{**FIXTURE["slides"][0], **update}])


class PreservationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "deck.json"
        self.output = self.root / "current.html"
        self.source.write_text(json.dumps(FIXTURE), encoding="utf-8")

    def test_default_build_creates_only_one_deliverable_and_preserves_source(self):
        source_before = self.source.read_bytes()
        count = build_presentation(self.source, self.output)
        self.assertEqual(count, len(FIXTURE["slides"]))
        self.assertEqual(self.source.read_bytes(), source_before)
        self.assertEqual({item.name for item in self.root.iterdir()}, {"deck.json", "current.html"})

    def test_refuses_existing_output_unless_explicitly_authorized(self):
        self.output.write_bytes(b"approved previous output")
        with self.assertRaisesRegex(FileExistsError, "--overwrite"):
            build_presentation(self.source, self.output)
        self.assertEqual(self.output.read_bytes(), b"approved previous output")

    def test_small_reference_edit_updates_only_intended_artifact(self):
        build_presentation(self.source, self.output)
        before = self.output.read_text(encoding="utf-8")
        preserved = self.root / "preserved.html"
        preserved.write_bytes(self.output.read_bytes())
        preserved_before = preserved.read_bytes()
        data = copy.deepcopy(FIXTURE)
        old_url = data["slides"][0]["references"][0]["url"]
        new_url = "https://example.org/designs/queue-worker#revised-retries"
        data["slides"][0]["references"][0]["url"] = new_url
        self.source.write_text(json.dumps(data), encoding="utf-8")
        build_presentation(self.source, self.output, overwrite=True)
        self.assertEqual(
            self.output.read_text(encoding="utf-8"), before.replace(escape(old_url), escape(new_url))
        )
        self.assertEqual(preserved.read_bytes(), preserved_before)
        self.assertEqual(len(list(self.root.iterdir())), 3)

    def test_failed_generation_keeps_existing_output_and_leaves_no_temporary_files(self):
        self.output.write_bytes(b"approved")
        for invalid in ("not JSON", "[]", '{"slides": []}'):
            with self.subTest(invalid=invalid):
                self.source.write_text(invalid, encoding="utf-8")
                with self.assertRaises(ValueError):
                    build_presentation(self.source, self.output, overwrite=True)
                self.assertEqual(self.output.read_bytes(), b"approved")
        self.assertEqual(len(list(self.root.iterdir())), 2)

    def test_failed_replacement_keeps_existing_output_and_cleans_temporary_file(self):
        self.output.write_bytes(b"approved")
        with patch("build_presentation.Path.replace", side_effect=OSError("replacement denied")):
            with self.assertRaisesRegex(OSError, "replacement denied"):
                build_presentation(self.source, self.output, overwrite=True)
        self.assertEqual(self.output.read_bytes(), b"approved")
        self.assertEqual(len(list(self.root.iterdir())), 2)

    def test_refuses_source_as_output_including_hardlink(self):
        before = self.source.read_bytes()
        with self.assertRaisesRegex(ValueError, "different files"):
            build_presentation(self.source, self.source, overwrite=True)
        os.link(self.source, self.output)
        with self.assertRaisesRegex(ValueError, "different files"):
            build_presentation(self.source, self.output, overwrite=True)
        self.assertEqual(self.source.read_bytes(), before)

    def test_utf8_content_round_trips_through_cli(self):
        title = "R\u00e9sum\u00e9 \u6d4b\u8bd5"
        self.source.write_text(json.dumps({**FIXTURE, "title": title}), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), str(self.source), str(self.output)],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(title, self.output.read_text(encoding="utf-8"))
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), str(self.source), str(self.output)],
            capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Output already exists", result.stderr)
        self.assertNotIn("Generated presentation", result.stdout)


if __name__ == "__main__":
    unittest.main()
