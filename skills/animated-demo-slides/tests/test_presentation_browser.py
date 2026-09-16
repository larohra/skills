"""Opt-in browser regressions; requires Playwright and an available browser."""

import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from build_presentation import build_presentation

FIXTURE = json.loads(
    (SKILL_DIR / "evals" / "fixtures" / "reference-deck.json").read_text(encoding="utf-8")
)


class PresentationBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.addClassCleanup(cls.playwright.stop)
        options = {"headless": True}
        if os.environ.get("SLIDES_BROWSER_CHANNEL"):
            options["channel"] = os.environ["SLIDES_BROWSER_CHANNEL"]
        cls.browser = cls.playwright.chromium.launch(**options)
        cls.addClassCleanup(cls.browser.close)
        temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(temporary.cleanup)
        cls.root = Path(temporary.name)
        source = cls.root / "deck.json"
        source.write_text(json.dumps(FIXTURE), encoding="utf-8")
        cls.output = cls.root / "deck.html"
        build_presentation(source, cls.output)
        cls.html = cls.output.read_text(encoding="utf-8")

    def setUp(self):
        self.context = self.browser.new_context(
            viewport={"width": 1280, "height": 900}, reduced_motion="no-preference"
        )
        # Test link activation without sending any requests to an external reference.
        self.context.route(
            re.compile(r"^https?://"),
            lambda route: route.fulfill(content_type="text/plain", body="Neutral reference fixture"),
        )
        self.page = self.context.new_page()
        self.errors = []
        self.requests = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))
        self.context.on("request", lambda request: self.requests.append(request.url))
        self.page.goto(self.output.as_uri())
        expect(self.page.locator("#toolbar")).to_be_visible()

    def tearDown(self):
        self.context.close()
        self.assertEqual(self.errors, [], "Unexpected browser exceptions")

    def assert_current(self, index, surface=None):
        surface = surface or self.page
        slides = surface.locator(".slide")
        for position in range(len(FIXTURE["slides"])):
            if position == index:
                expect(slides.nth(position)).to_be_visible()
            else:
                expect(slides.nth(position)).to_be_hidden()
        expect(surface.locator("#counter")).to_have_text(f"{index + 1} / {len(FIXTURE['slides'])}")

    def test_navigation_boundaries_and_native_keyboard_focus(self):
        page = self.page
        self.assert_current(0)
        expect(page.locator("#prev")).to_be_disabled()
        page.locator("#skip").focus()
        page.keyboard.press("Enter")
        expect(page.locator("#slides")).to_be_focused()
        for index in range(1, len(FIXTURE["slides"])):
            page.keyboard.press("ArrowRight")
            self.assert_current(index)
        page.keyboard.press("ArrowRight")
        self.assert_current(len(FIXTURE["slides"]) - 1)
        expect(page.locator("#next")).to_be_disabled()
        page.keyboard.press("Home")
        self.assert_current(0)
        page.keyboard.press("Space")
        self.assert_current(1)
        page.keyboard.press("End")
        self.assert_current(len(FIXTURE["slides"]) - 1)
        page.locator("#prev").click()
        self.assert_current(len(FIXTURE["slides"]) - 2)
        page.locator("#slides").focus()
        page.keyboard.press("Home")
        summary = page.locator(".slide").first.locator("summary")
        summary.focus()
        page.keyboard.press("Space")
        expect(page.locator(".slide").first.locator("details")).to_have_attribute("open", "")
        self.assert_current(0)
        page.keyboard.press("Space")
        expect(page.locator(".slide").first.locator("details")).not_to_have_attribute("open", "")
        page.locator("#next").focus()
        page.keyboard.press("Space")
        self.assert_current(1)

    def test_reader_and_editable_targets_keep_native_keys(self):
        self.page.locator("#reader").click()
        expect(self.page.locator("#reader")).to_have_attribute("aria-pressed", "true")
        for slide in self.page.locator(".slide").all():
            expect(slide).to_be_visible()
        prevented = self.page.locator("#slides").evaluate("""element => {
            const event = new KeyboardEvent('keydown', {key: ' ', bubbles: true, cancelable: true});
            element.dispatchEvent(event);
            return event.defaultPrevented;
        }""")
        self.assertFalse(prevented)
        self.page.locator("#reader").click()
        self.page.evaluate("""() => {
            const field = document.createElement('input');
            field.id = 'test-input';
            document.querySelector('.slide').append(field);
            field.focus();
        }""")
        self.page.keyboard.press("End")
        self.assert_current(0)
        self.page.locator("#slides").focus()
        prevented = self.page.locator("#slides").evaluate("""element => {
            const event = new KeyboardEvent('keydown', {
                key: 'ArrowRight', ctrlKey: true, bubbles: true, cancelable: true
            });
            element.dispatchEvent(event);
            return event.defaultPrevented;
        }""")
        self.assertFalse(prevented)
        self.assert_current(0)

    def test_references_are_keyboard_usable_without_automatic_fetches(self):
        self.assertFalse(any(url.startswith(("https:", "http:")) for url in self.requests))
        reference = FIXTURE["slides"][0]["references"][0]
        hotspot = self.page.locator(".hotspot").first
        expect(hotspot).to_have_attribute("href", reference["url"])
        expect(hotspot).to_have_accessible_name(f"Ref 1: {reference['label']}")
        hotspot.focus()
        expect(hotspot).to_be_focused()
        with self.context.expect_page() as opened:
            self.page.keyboard.press("Enter")
        popup = opened.value
        popup.wait_for_load_state()
        self.assertEqual(popup.url, reference["url"])
        popup.close()
        self.page.locator(".slide").first.locator("summary").click()
        notes = self.page.locator(".slide").first.locator(".notes")
        expect(notes.get_by_role("link", name=reference["label"])).to_have_attribute("href", reference["url"])
        expect(notes.locator(".source-url")).to_have_text(reference["url"])
        self.page.locator("#reader").click()
        expect(hotspot).to_be_hidden()
        expect(self.page.locator(".slide").first.locator(":scope > .references a")).to_be_visible()

    def test_all_slides_fit_desktop_and_mobile_and_hotspots_track_image(self):
        for width, height in ((1280, 900), (390, 844), (320, 640)):
            with self.subTest(viewport=(width, height)):
                self.page.set_viewport_size({"width": width, "height": height})
                for index, data in enumerate(FIXTURE["slides"]):
                    slide = self.page.locator(".slide").nth(index)
                    if width > 768:
                        self.page.locator("#slides").focus()
                        self.page.keyboard.press("Home")
                        for _ in range(index):
                            self.page.keyboard.press("ArrowRight")
                    expect(slide).to_be_visible()
                    expect(slide.locator("h2")).to_have_text(data["title"])
                    expect(slide.locator(".description")).to_have_text(data["description"])
                    image = slide.locator("img")
                    expect(image).to_be_visible()
                    image_box = image.bounding_box()
                    figure_box = slide.locator("figure").bounding_box()
                    self.assertAlmostEqual(figure_box["width"], image_box["width"], delta=1)
                    self.assertAlmostEqual(figure_box["height"], image_box["height"], delta=1)
                    self.assertGreaterEqual(image_box["x"], 0)
                    self.assertLessEqual(image_box["x"] + image_box["width"], width + 1)
                    self.assertGreaterEqual(image_box["width"], width * 0.65)
                    for qualification in data["qualifications"]:
                        expect(slide.locator(".qualifications")).to_contain_text(qualification)
                    if width > 768 and data.get("references"):
                        region = data["references"][0]["region"]
                        box = slide.locator(".hotspot").bounding_box()
                        self.assertAlmostEqual(
                            box["x"], image_box["x"] + image_box["width"] * region["x"] / 100, delta=1
                        )
                        self.assertAlmostEqual(
                            box["width"], image_box["width"] * region["width"] / 100, delta=1
                        )
                dimensions = self.page.evaluate(
                    "() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]"
                )
                self.assertLessEqual(dimensions[0], dimensions[1] + 1)
                if width <= 768:
                    expect(self.page.locator("#reader")).to_be_disabled()
                    expect(self.page.locator("#reader")).to_have_attribute("aria-pressed", "true")

    def test_rendered_fixture_labels_stay_inside_svg_bounds(self):
        for slide in FIXTURE["slides"]:
            for field in ("svg", "static_svg"):
                if field not in slide:
                    continue
                with self.subTest(slide=slide["name"], field=field):
                    self.page.set_content(slide[field])
                    bounds = self.page.locator("svg").bounding_box()
                    for text in self.page.locator("svg text").all():
                        box = text.bounding_box()
                        self.assertGreaterEqual(box["x"], bounds["x"])
                        self.assertGreaterEqual(box["y"], bounds["y"])
                        self.assertLessEqual(box["x"] + box["width"], bounds["x"] + bounds["width"])
                        self.assertLessEqual(box["y"] + box["height"], bounds["y"] + bounds["height"])

    def test_focus_leaves_a_slide_hidden_when_exiting_mobile_reader(self):
        self.page.set_viewport_size({"width": 390, "height": 844})
        summary = self.page.locator(".slide").last.locator("summary")
        summary.focus()
        expect(summary).to_be_focused()
        self.page.set_viewport_size({"width": 1280, "height": 900})
        self.assert_current(0)
        expect(self.page.locator("#slides")).to_be_focused()

    def test_reduced_motion_static_image_or_text_fallback(self):
        self.page.emulate_media(reduced_motion="reduce")
        self.page.locator("#reader").click()
        expect(self.page.locator("#replay")).to_be_disabled()
        for index, data in enumerate(FIXTURE["slides"]):
            slide = self.page.locator(".slide").nth(index)
            expect(slide.locator(".description")).to_be_visible()
            if "static_svg" in data:
                image = slide.locator("img")
                expect(image).to_be_visible()
                self.page.wait_for_function(
                    """index => {
                        const slide = document.querySelectorAll('.slide')[index];
                        return slide.querySelector('img').currentSrc === slide.querySelector('source').srcset;
                    }""", arg=index
                )
            else:
                expect(slide.locator(".visual")).to_be_hidden()
                expect(slide.locator(".motion-notice")).to_be_visible()
        expect(self.page.locator(".slide").first.locator(":scope > .references a")).to_be_visible()

    def test_finite_animation_can_be_replayed_and_restarts_on_entry(self):
        image = self.page.locator(".slide").first.locator("img")
        self.page.wait_for_timeout(2200)
        completed = image.screenshot()
        self.page.locator("#replay").click()
        restarted = image.screenshot()
        self.assertNotEqual(completed, restarted, "Replay must restart rendered motion, not just change a URL")
        self.page.wait_for_timeout(2200)
        self.assertEqual(completed, image.screenshot(), "Animation should finish on the same readable frame")
        self.page.locator("#next").click()
        self.page.locator("#prev").click()
        self.assertNotEqual(completed, image.screenshot(), "Entering a slide must restart its animation")

    def test_opaque_srcdoc_blob_base_retains_navigation_and_skip_focus(self):
        self.page.set_content('<iframe id="embedded" sandbox="allow-scripts" width="1200" height="800"></iframe>')
        self.page.evaluate("""html => {
            window.fixtureBase = URL.createObjectURL(new Blob(['base'], {type: 'text/html'}));
            document.querySelector('iframe').srcdoc = html.replace(
                '<head>', '<head><base href="' + window.fixtureBase + '">'
            );
        }""", self.html)
        surface = self.page.frame_locator("#embedded")
        expect(surface.locator("#toolbar")).to_be_visible()
        frame = self.page.locator("#embedded").element_handle().content_frame()
        state = frame.evaluate("""() => {
            let historyError;
            try { history.replaceState({}, '', '#probe'); }
            catch (error) { historyError = error.name; }
            return {url: location.href, origin: window.origin, base: document.baseURI, historyError};
        }""")
        self.assertEqual(state["url"], "about:srcdoc")
        self.assertEqual(state["origin"], "null")
        self.assertTrue(state["base"].startswith("blob:"))
        self.assertEqual(state["historyError"], "SecurityError")
        surface.locator("#next").click()
        self.assert_current(1, surface)
        surface.locator("#skip").focus()
        self.page.keyboard.press("Enter")
        expect(surface.locator("#slides")).to_be_focused()
        self.page.keyboard.press("End")
        self.assert_current(len(FIXTURE["slides"]) - 1, surface)
        surface.locator("#reader").click()
        for slide in surface.locator(".slide").all():
            expect(slide).to_be_visible()
        self.assertEqual(frame.evaluate("location.href"), "about:srcdoc")
        self.page.evaluate("URL.revokeObjectURL(window.fixtureBase)")

    def test_script_disabled_document_is_readable(self):
        context = self.browser.new_context(java_script_enabled=False, viewport={"width": 390, "height": 844})
        try:
            page = context.new_page()
            page.goto(self.output.as_uri())
            expect(page.locator("#toolbar")).to_be_hidden()
            for index, slide in enumerate(FIXTURE["slides"]):
                section = page.locator(".slide").nth(index)
                expect(section).to_be_visible()
                expect(section.locator(".description")).to_have_text(slide["description"])
            expect(page.locator(".slide").first.locator(":scope > .references a")).to_be_visible()
        finally:
            context.close()

    def test_fullscreen_denial_is_visible_but_unrelated_errors_are_not_swallowed(self):
        self.page.evaluate("""() => {
            Object.defineProperty(document, 'fullscreenEnabled', {value: true, configurable: true});
            document.documentElement.requestFullscreen = () => Promise.reject(
                new DOMException('Denied by test viewer', 'NotAllowedError')
            );
        }""")
        self.page.locator("#fullscreen").click()
        expect(self.page.locator("#status")).to_contain_text("did not allow fullscreen")
        self.page.locator("#next").click()
        self.assert_current(1)
        self.page.evaluate("""() => {
            document.documentElement.requestFullscreen = () => Promise.reject(new RangeError('Unexpected fixture error'));
        }""")
        with self.page.expect_event("pageerror") as unexpected:
            self.page.locator("#fullscreen").click()
        self.assertIn("Unexpected fixture error", str(unexpected.value))
        self.assertEqual(len(self.errors), 1)
        self.errors.clear()


if __name__ == "__main__":
    unittest.main()
