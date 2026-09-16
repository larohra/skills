# Presentation generator

Run `scripts/build_presentation.py` with Python 3.9 or newer. The generator uses only the standard library; the delivered HTML has no external runtime dependencies.

```text
python scripts/build_presentation.py deck.json deck.html
python scripts/build_presentation.py deck.json deck.html --overwrite
```

The second command is only for an authorized update to that exact artifact. The first refuses existing outputs. Both reject the source file as the output, and invalid input exits with an explicit error. No PPTX, video, alternate HTML, or review screenshots are generated.

## JSON input

Existing `title`, `slides`, `name`, `svg`, and `description` inputs remain supported. `svg` accepts raw SVG, UTF-8 base64 SVG, or an SVG base64 data URI. The deck must contain at least one slide. Text is plain text, escaped for HTML; SVG stays isolated in an image.

| Field | Meaning |
| --- | --- |
| `title` | Deck title; defaults to `Presentation` if omitted |
| `slides` | Non-empty list of slide objects, in presentation order |
| `slides[].name` | Existing slide name; used as its heading if no `title` is supplied |
| `slides[].title` | Optional exact human-readable title |
| `slides[].svg` | Required self-contained SVG with a useful viewBox |
| `slides[].description` | Plain-language text equivalent of the diagram, visible in both slide and reader views |
| `slides[].qualifications` | Optional list of caveats rendered visibly, not hidden in notes |
| `slides[].notes` | Optional plain-text supporting detail, available through a native disclosure |
| `slides[].static_svg` | Optional readable, non-animated SVG selected for reduced motion |
| `slides[].references` | Optional list of native links, also rendered in notes |

Each reference has a non-empty `label` and an absolute HTTP(S) `url`. URLs are not rewritten or fetched. Links open a new tab only if the viewer permits it; notes expose the full URL for copying.

An optional `region` places a labeled link over a diagram component or row: `x`, `y`, `width`, and `height` are percentages of the displayed image, measured from its top-left. Values must be finite and the positive-sized rectangle must fit within 0-100 percent bounds. Keep enough space for the visible `Ref` label and inspect the rendered geometry. The matching numbered link remains visible below the diagram; reader mode hides the hotspot, not the equivalent link.

```json
{
  "title": "Choosing a processing model",
  "slides": [
    {
      "name": "queue-worker",
      "title": "Who retries a failed job?",
      "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 800 450\"><rect width=\"800\" height=\"450\" fill=\"#161b22\"/><text x=\"80\" y=\"140\" fill=\"#e6edf3\" font-size=\"32\">Queue worker</text></svg>",
      "description": "A queue worker receives a job and records the result. The retry owner must be specified.",
      "qualifications": ["This is a proposed design, not a demonstrated recovery guarantee."],
      "notes": "Compare retry ownership with the other requested processing models.",
      "references": [
        {
          "label": "Queue worker design",
          "url": "https://example.org/designs/queue-worker#retry",
          "region": {"x": 8, "y": 15, "width": 45, "height": 30}
        }
      ]
    }
  ]
}
```

The example is an input fragment, not a prescribed slide count or a substitute for the requested option inventory.

## Runtime behavior

The generated HTML contains all slide headings, descriptions, qualifications, notes, and references before JavaScript runs. With scripts disabled it is a readable, scrolling document. With scripts enabled, desktop uses a single-slide view with native previous/next buttons, animation replay, a reader toggle, keyboard shortcuts, and a fullscreen control. Narrow viewports automatically show all slides as a reader; keyboard navigation does not intercept native scrolling there.

Arrow keys, Space, Home, and End navigate when focus is outside interactive controls. Tab, Enter, Space on buttons or notes, editable fields, links, and modified key combinations retain native behavior. The skip button focuses the main content directly. No slide state is written to history, location, or a URL fragment, including inside an opaque-origin `about:srcdoc` document with a blob base URL.

Author finite SVG animations ending on a readable state. Entering a slide or using Replay restarts its image resource; it does not navigate the document or change its URL. Replay is disabled in reader view and for reduced motion. The generator does not convert an authored infinite loop into a meaningful finite sequence.

Expected fullscreen restrictions display a message without breaking navigation. Unexpected exceptions are not swallowed. Fullscreen and opening new tabs remain subject to browser and host policy; the generator cannot grant either permission.

For reduced motion, a supplied `static_svg` is selected through a media query. Without it, the animated image and its hotspots are hidden, while descriptions, qualifications, and reference links remain visible. Missing text alternatives are reported visibly rather than pretending to reconstruct the diagram. Parent-page CSS cannot reliably stop animations inside an SVG image, so supply an actually static alternative rather than assuming a host CSS rule freezes it. Static alternatives should use the same coordinate system if they share reference regions.

The generator does not infer labels, check claims, rewrite SVG text, or validate that a supplied static SVG is truly static. Keep those in the reproducible authoring source and inspect the rendered result. Avoid external fonts/assets in authored SVG; the wrapper does not download or bundle them for you. SVG animation and browser layout are not automatically preserved in a native PowerPoint conversion.

## Focused validation

From the repository root:

```text
python -B -m unittest discover -s skills/animated-demo-slides/tests -p test_build_presentation.py
```

The standard-library tests cover supported input formats, exact text/link rendering, preservation, and CLI errors. For actual browser interaction and geometry checks, use the optional Playwright test module:

```text
python -m pip install playwright
python -m playwright install chromium
python -B -m unittest discover -s skills/animated-demo-slides/tests -p test_presentation_browser.py
```

The browser module uses a Playwright-managed browser by default. An optional `SLIDES_BROWSER_CHANNEL` environment variable selects an already installed, Playwright-supported browser channel without embedding a machine-specific executable path. These are test tools, not dependencies of delivered decks.

Browser tests batch all fixture slides and desktop/mobile geometry, navigation, native notes/focus, references, reader mode, reduced motion, script-disabled reading, and a sandboxed `srcdoc`/blob-base simulation. They do not prove compatibility with a particular document portal or tenant. Behavioral prompts in `evals/evals.json` are a separate evaluation layer; report their results only when an agent evaluation was actually run.
