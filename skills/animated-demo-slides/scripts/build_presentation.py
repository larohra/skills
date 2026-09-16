#!/usr/bin/env python3
"""Build one self-contained HTML deck; see references/generator.md for the schema."""

import argparse
import base64
import binascii
import json
import math
import sys
import tempfile
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path
from urllib.parse import urlsplit


def wrap_svg_for_display(svg_content):
    """Normalize raw SVG, base64 SVG, or an SVG base64 data URI."""
    if not isinstance(svg_content, str) or not svg_content.strip():
        raise ValueError("svg must be a non-empty string")
    content = svg_content.strip()
    if not content.startswith("<"):
        content = content.removeprefix("data:image/svg+xml;base64,")
        try:
            svg_content = base64.b64decode(content, validate=True).decode("utf-8")
        except (binascii.Error, UnicodeDecodeError) as error:
            raise ValueError("svg must contain raw SVG or UTF-8 base64 SVG") from error
    try:
        root = ET.fromstring(svg_content)
    except ET.ParseError as error:
        raise ValueError(f"Invalid SVG: {error}") from error
    if root.tag not in ("svg", "{http://www.w3.org/2000/svg}svg"):
        raise ValueError("svg must have an SVG root element")
    return svg_content


def svg_to_base64_uri(svg_content):
    """Keep authored SVG isolated in an image rather than inserting active markup."""
    svg_content = wrap_svg_for_display(svg_content)
    encoded = base64.b64encode(svg_content.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def visual_size(svg_content):
    view_box = ET.fromstring(wrap_svg_for_display(svg_content)).get("viewBox")
    if view_box is None:
        return ""
    try:
        dimensions = [float(value) for value in view_box.replace(",", " ").split()]
    except ValueError as error:
        raise ValueError("SVG viewBox must contain four finite numbers") from error
    if (
        len(dimensions) != 4 or not all(math.isfinite(value) for value in dimensions)
        or dimensions[2] <= 0 or dimensions[3] <= 0
    ):
        raise ValueError("SVG viewBox must contain four finite numbers with positive width and height")
    ratio = dimensions[2] / dimensions[3]
    if not math.isfinite(ratio) or ratio <= 0:
        raise ValueError("SVG viewBox must have a finite positive aspect ratio")
    return f'style="max-width:min(100%,calc(60vh * {ratio}))"'


def require_text(value, field, allow_empty=False):
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        raise ValueError(f"{field} must be {'a' if allow_empty else 'a non-empty'} string")
    return value


def validate_references(references):
    if not isinstance(references, list):
        raise ValueError("references must be a list")
    for reference in references:
        if not isinstance(reference, dict):
            raise ValueError("Each reference must be an object")
        require_text(reference.get("label"), "reference.label")
        url = require_text(reference.get("url"), "reference.url")
        parsed = urlsplit(url)
        if (
            parsed.scheme not in ("https", "http")
            or not parsed.hostname
            or any(character.isspace() for character in url)
        ):
            raise ValueError("reference.url must be an absolute HTTP(S) URL without whitespace")
        if "region" in reference:
            region = reference["region"]
            if not isinstance(region, dict):
                raise ValueError("reference.region must be an object")
            for key in ("x", "y", "width", "height"):
                value = region.get(key)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, (int, float))
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"reference.region.{key} must be a finite number from 0 to 100")
            if (
                region["width"] <= 0 or region["height"] <= 0
                or region["x"] + region["width"] > 100
                or region["y"] + region["height"] > 100
            ):
                raise ValueError("reference.region must fit within the image's 0-100 percent bounds")
    return references


def render_references(references, include_urls=False):
    items = []
    for reference in references:
        url, label = escape(reference["url"]), escape(reference["label"])
        source = f'<span class="source-url">{url}</span>' if include_urls else ""
        items.append(
            f'<li><a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>{source}</li>'
        )
    return '<ol class="references" aria-label="References">' + "".join(items) + "</ol>"


def render_slide(slide, index):
    if not isinstance(slide, dict):
        raise ValueError("Each slide must be an object")
    heading = require_text(slide.get("title", slide.get("name", "Slide")), "slide.title")
    description = require_text(slide.get("description", ""), "description", allow_empty=True)
    notes = require_text(slide.get("notes", ""), "notes", allow_empty=True)
    qualifications = slide.get("qualifications", [])
    if not isinstance(qualifications, list):
        raise ValueError("qualifications must be a list")
    for qualification in qualifications:
        require_text(qualification, "qualification")
    references = validate_references(slide.get("references", []))
    svg_uri = svg_to_base64_uri(slide.get("svg"))
    size = visual_size(slide["svg"])
    image = f'<img src="{svg_uri}" alt="{escape(description or heading)}" />'
    motion_class = "animated-only"
    motion_notice = '<p class="motion-notice">Animated diagram hidden for reduced motion.</p>'
    if "static_svg" in slide:
        static_uri = svg_to_base64_uri(slide["static_svg"])
        image = (
            '<picture><source media="(prefers-reduced-motion: reduce)" '
            f'srcset="{static_uri}" />{image}</picture>'
        )
        motion_class, motion_notice = "", ""
    elif not description:
        motion_notice = (
            '<p class="motion-notice">Animated diagram hidden for reduced motion. '
            'No text description was supplied for this diagram.</p>'
        )
    hotspots = []
    for number, reference in enumerate(references, 1):
        if "region" not in reference:
            continue
        region = reference["region"]
        style = (
            f'left:{region["x"]}%;top:{region["y"]}%;'
            f'width:{region["width"]}%;height:{region["height"]}%'
        )
        hotspots.append(
            f'<a class="hotspot" style="{style}" href="{escape(reference["url"])}" '
            'target="_blank" rel="noopener noreferrer" '
            f'aria-label="Ref {number}: {escape(reference["label"])}">'
            f'<span>Ref {number}</span></a>'
        )
    caveats = ""
    if qualifications:
        caveats = '<ul class="qualifications">' + "".join(
            f"<li>{escape(text)}</li>" for text in qualifications
        ) + "</ul>"
    note_section = ""
    if notes or references:
        note_section = (
            '<details class="notes"><summary>Notes and references</summary>'
            f'<p class="copy">{escape(notes)}</p>'
            f'{render_references(references, include_urls=True) if references else ""}</details>'
        )
    return f"""
    <section class="slide" aria-labelledby="title-{index}">
      <h2 id="title-{index}">{escape(heading)}</h2>
      <figure class="visual {motion_class}" {size}>{image}{"".join(hotspots)}</figure>
      {motion_notice}
      <p class="copy description">{escape(description)}</p>
      {caveats}
      {render_references(references) if references else ""}
      {note_section}
    </section>"""


def generate_html(title, slides):
    """Render readable HTML first, then enhance it with in-memory navigation."""
    require_text(title, "title")
    if not isinstance(slides, list) or not slides:
        raise ValueError("slides must be a non-empty list")
    sections = "".join(render_slide(slide, index) for index, slide in enumerate(slides, 1))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{escape(title)} - slides</title>
<style>
  :root {{ color-scheme: dark; }}
  * {{ box-sizing: border-box; }}
  [hidden] {{ display: none !important; }}
  html {{ background: #0d1117; color: #e6edf3; }}
  body {{
    margin: 0; line-height: 1.5;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }}
  main {{ max-width: 80rem; margin-inline: auto; padding: 1.5rem; }}
  h1 {{ font-size: 1rem; color: #b1bac4; font-weight: 500; }}
  h2 {{ font-size: clamp(1.5rem, 3vw, 2.25rem); line-height: 1.2; margin: 0 0 1rem; }}
  .slide {{ padding-block: 1rem 2rem; overflow-wrap: anywhere; }}
  .visual {{ position: relative; width: 100%; max-width: 100%; margin: 1rem auto; }}
  .visual img {{ display: block; width: 100%; height: auto; }}
  .copy {{ white-space: pre-wrap; max-width: 75ch; }}
  .copy:empty {{ display: none; }}
  .qualifications {{ padding-inline-start: 1.5rem; }}
  a {{ color: #79c0ff; text-underline-offset: .2em; }}
  a:hover {{ color: #c4e4ff; }}
  button, summary {{ cursor: pointer; font: inherit; }}
  button {{
    min-height: 2.75rem; padding: .5rem .9rem; border: 1px solid #8b949e;
    border-radius: .4rem; color: inherit; background: #161b22;
  }}
  button:hover:not(:disabled) {{ background: #30363d; }}
  button:disabled {{ cursor: default; color: #8b949e; }}
  :focus-visible {{ outline: 3px solid #79c0ff; outline-offset: 3px; }}
  #skip {{ position: fixed; top: .5rem; left: .5rem; transform: translateY(-200%); z-index: 10; }}
  #skip:focus {{ transform: none; }}
  #toolbar {{
    position: sticky; bottom: 0; display: flex; flex-wrap: wrap; gap: .5rem;
    align-items: center; justify-content: center; padding: .75rem;
    background: #0d1117; border-top: 1px solid #30363d; z-index: 5;
  }}
  #counter {{ min-width: 6ch; text-align: center; }}
  #help, #status {{ flex-basis: 100%; text-align: center; font-size: .875rem; color: #b1bac4; }}
  #status:empty {{ display: none; }}
  .references {{ padding-inline-start: 1.5rem; }}
  .references a {{ display: inline-block; padding-block: .35rem; }}
  .source-url {{ display: block; overflow-wrap: anywhere; color: #b1bac4; }}
  .notes {{ margin-top: 1.5rem; }}
  .notes summary {{ padding-block: .5rem; }}
  .hotspot {{
    position: absolute; border: 2px solid #79c0ff; display: flex; align-items: flex-end;
    text-decoration: none;
  }}
  .hotspot span {{ background: #0d1117; padding: .1rem .35rem; font-size: 1rem; }}
  .motion-notice {{ display: none; }}
  .reader .slide + .slide {{ border-top: 1px solid #30363d; padding-top: 2rem; }}
  .reader .hotspot {{ display: none; }}
  @media (max-width: 48rem) {{
    main {{ padding: 1rem; }}
    #toolbar {{ position: static; }}
    #prev, #next {{ display: none; }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .animated-only {{ display: none; }}
    .motion-notice {{ display: block; }}
    *, *::before, *::after {{ scroll-behavior: auto !important; animation: none !important; transition: none !important; }}
  }}
  @media print {{
    #toolbar, #skip, .hotspot {{ display: none !important; }}
    .slide[hidden] {{ display: block !important; }}
    .slide {{ break-after: page; }}
  }}
</style>
</head>
<body class="reader">
  <button id="skip" type="button" hidden>Skip to slides</button>
  <main id="slides" tabindex="-1">
    <h1>{escape(title)}</h1>{sections}
  </main>
  <nav id="toolbar" aria-label="Presentation controls" hidden>
    <button id="prev" type="button" aria-label="Previous slide">Previous</button>
    <span id="counter" role="status" aria-live="polite" aria-atomic="true"></span>
    <button id="next" type="button" aria-label="Next slide">Next</button>
    <button id="replay" type="button">Replay animation</button>
    <button id="reader" type="button" aria-pressed="false">Reader view</button>
    <button id="fullscreen" type="button">Fullscreen</button>
    <span id="help">Arrow keys / Space: navigate; Home / End: jump; F: fullscreen. Tab: controls and links.</span>
    <span id="status" role="status"></span>
  </nav>

<script>
  const slides = Array.from(document.querySelectorAll('.slide'));
  const stage = document.getElementById('slides');
  const previous = document.getElementById('prev');
  const next = document.getElementById('next');
  const replay = document.getElementById('replay');
  const reader = document.getElementById('reader');
  const fullscreen = document.getElementById('fullscreen');
  const status = document.getElementById('status');
  const narrow = window.matchMedia('(max-width: 48rem)');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let currentSlide = 0;
  let readerRequested = false;
  let replayId = 0;

  function isReader() {{
    return readerRequested || narrow.matches;
  }}

  function updateSlide() {{
    const reading = isReader();
    slides.forEach((slide, index) => {{
      slide.hidden = !reading && index !== currentSlide;
    }});
    document.body.classList.toggle('reader', reading);
    previous.disabled = reading || currentSlide === 0;
    next.disabled = reading || currentSlide === slides.length - 1;
    replay.disabled = reading || reducedMotion.matches;
    reader.disabled = narrow.matches;
    reader.setAttribute('aria-pressed', String(reading));
    reader.textContent = reading ? 'Slide view' : 'Reader view';
    document.getElementById('counter').textContent = reading
      ? `${{slides.length}} slides` : `${{currentSlide + 1}} / ${{slides.length}}`;
    document.getElementById('help').textContent = reading
      ? 'Reader view: scroll through all slides. Tab: notes, controls and links.'
      : 'Arrow keys / Space: navigate; Home / End: jump; F: fullscreen. Tab: controls and links.';
    if (slides.some(slide => slide.hidden && slide.contains(document.activeElement))) {{
      stage.focus();
    }}
  }}

  function replayAnimation() {{
    if (isReader() || reducedMotion.matches) return;
    const image = slides[currentSlide].querySelector('img');
    const original = image.dataset.originalSrc || image.getAttribute('src');
    image.dataset.originalSrc = original;
    // Fresh image bytes restart its SVG timeline without changing the authored graphics or document URL.
    image.src = 'data:image/svg+xml;base64,' +
      btoa(atob(original.split(',')[1]) + `<!-- replay ${{++replayId}} -->`);
  }}

  function jumpToSlide(index) {{
    if (!isReader() && index >= 0 && index < slides.length) {{
      currentSlide = index;
      updateSlide();
      replayAnimation();
      stage.scrollIntoView({{block: 'start'}});
    }}
  }}

  async function toggleFullscreen() {{
    if (!document.fullscreenEnabled || !document.documentElement.requestFullscreen) {{
      status.textContent = 'Fullscreen is unavailable in this viewer. Slide navigation still works.';
      return;
    }}
    try {{
      if (document.fullscreenElement) {{
        await document.exitFullscreen();
      }} else {{
        await document.documentElement.requestFullscreen();
      }}
      status.textContent = '';
    }} catch (error) {{
      if (error instanceof TypeError ||
          (error instanceof DOMException && ['NotAllowedError', 'SecurityError', 'NotSupportedError'].includes(error.name))) {{
        status.textContent = 'This viewer did not allow fullscreen. Slide navigation still works.';
      }} else {{
        throw error;
      }}
    }}
  }}

  document.addEventListener('keydown', (event) => {{
    if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    if (event.target instanceof Element &&
        (event.target.closest('a, button, input, textarea, select, summary') || event.target.isContentEditable)) return;
    if (event.key.toLowerCase() === 'f') {{
      event.preventDefault();
      toggleFullscreen();
      return;
    }}
    if (isReader()) return;
    const destinations = {{
      ArrowRight: currentSlide + 1, ' ': currentSlide + 1,
      ArrowLeft: currentSlide - 1, Home: 0, End: slides.length - 1
    }};
    if (Object.hasOwn(destinations, event.key)) {{
      event.preventDefault();
      jumpToSlide(destinations[event.key]);
    }}
  }});

  previous.addEventListener('click', () => jumpToSlide(currentSlide - 1));
  next.addEventListener('click', () => jumpToSlide(currentSlide + 1));
  replay.addEventListener('click', replayAnimation);
  reader.addEventListener('click', () => {{
    readerRequested = !readerRequested;
    updateSlide();
    replayAnimation();
  }});
  fullscreen.addEventListener('click', toggleFullscreen);
  narrow.addEventListener('change', () => {{ updateSlide(); replayAnimation(); }});
  reducedMotion.addEventListener('change', updateSlide);
  // Move focus directly: fragment URLs may resolve against an embedding viewer's blob base.
  document.getElementById('skip').addEventListener('click', () => {{
    stage.focus();
    stage.scrollIntoView({{block: 'start'}});
  }});
  document.getElementById('skip').hidden = false;
  document.getElementById('toolbar').hidden = false;
  updateSlide();
  replayAnimation();
</script>
</body>
</html>
"""


def build_presentation(input_file, output_file, overwrite=False):
    input_file, output_file = Path(input_file), Path(output_file)
    if (
        input_file.resolve() == output_file.resolve()
        or (output_file.exists() and input_file.samefile(output_file))
    ):
        raise ValueError("Input and output must be different files")
    if output_file.is_symlink():
        raise ValueError("Choose an explicit output file, not a symbolic link")
    if output_file.exists() and not overwrite:
        raise FileExistsError("Output already exists; use --overwrite only for an authorized replacement")
    data = json.loads(input_file.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("The input JSON must be an object")
    slides = data.get("slides", [])
    html = generate_html(data.get("title", "Presentation"), slides)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    if overwrite:
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=output_file.parent, suffix=".tmp", delete=False
            ) as stream:
                temporary = Path(stream.name)
                stream.write(html)
            temporary.replace(output_file)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    else:
        with output_file.open("x", encoding="utf-8") as stream:
            stream.write(html)
    return len(slides)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--overwrite", action="store_true", help="Replace the explicitly approved output")
    args = parser.parse_args()
    try:
        count = build_presentation(args.input, args.output, args.overwrite)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(f"Generated presentation: {args.output}")
    print(f"Total slides: {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
