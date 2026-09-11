#!/usr/bin/env python3
"""
Generate an animated HTML slide presentation from a JSON slide specification.

This script takes a JSON description of slides and generates a self-contained
HTML file with embedded SVG slides and navigation controls.

Usage:
    python build_presentation.py <input.json> <output.html>

Input JSON format:
{
  "title": "Presentation Title",
  "slides": [
    {
      "name": "slide-title",
      "svg": "raw SVG content or base64 encoded",
      "description": "optional description"
    }
  ]
}
"""

import json
import base64
import sys
from pathlib import Path


def wrap_svg_for_display(svg_content):
    """Ensure SVG has proper attributes for display."""
    if not svg_content.strip().startswith('<svg'):
        return svg_content
    
    # If it doesn't have viewBox, we might need to add one
    if 'viewBox' not in svg_content and 'width' in svg_content and 'height' in svg_content:
        # SVG is already well-formed for the HTML wrapper
        pass
    
    return svg_content


def svg_to_base64_uri(svg_content):
    """Convert SVG content to data URI."""
    encoded = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{encoded}"


def generate_html(title, slides):
    """Generate the HTML presentation wrapper."""
    
    # Build slides array for JavaScript
    slides_js = "const slides = ["
    slide_list = []
    
    for slide in slides:
        svg_uri = svg_to_base64_uri(slide['svg'])
        slide_obj = {
            "name": slide.get('name', 'slide'),
            "uri": svg_uri
        }
        slide_list.append(json.dumps(slide_obj))
    
    slides_js += ", ".join(slide_list) + "];"
    
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title} — slides</title>
<style>
  :root {{ color-scheme: dark; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ height: 100%; background: #0d1117; overflow: hidden; }}
  body {{
    display: flex; align-items: center; justify-content: center;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }}
  #stage {{ width: 100vw; height: 100vh; }}
  #slide {{ width: 100vw; height: 100vh; object-fit: contain; display: block; }}

  #counter {{
    position: fixed; bottom: 16px; right: 20px;
    font-size: 14px; font-weight: 700; color: #8b949e;
    background: rgba(22,27,34,0.7); border: 1px solid #30363d;
    padding: 4px 10px; border-radius: 20px; letter-spacing: .3px;
    opacity: 0; transition: opacity .25s ease; pointer-events: none;
  }}
  #counter.show {{ opacity: 1; }}

  #help {{
    position: fixed; bottom: 16px; left: 20px;
    font-size: 13px; color: #6e7681;
    opacity: 0; transition: opacity .25s ease; pointer-events: none;
  }}
  #help.show {{ opacity: 1; }}

  .zone {{ position: fixed; top: 0; height: 100%; width: 22%; cursor: pointer; z-index: 5; }}
  .zone.prev {{ left: 0; }}
  .zone.next {{ right: 0; }}
</style>
</head>
<body>
  <div id="stage"><img id="slide" alt="" /></div>
  <div class="zone prev" title="Previous"></div>
  <div class="zone next" title="Next"></div>
  <div id="counter"></div>
  <div id="help">← / → to navigate · F fullscreen · Home/End jump</div>

<script>
  {slides_js}

  let currentSlide = 0;

  function updateSlide() {{
    if (slides.length > 0) {{
      document.getElementById('slide').src = slides[currentSlide].uri;
      const counter = document.getElementById('counter');
      counter.textContent = `${{currentSlide + 1}} / ${{slides.length}}`;
      counter.classList.add('show');
      setTimeout(() => counter.classList.remove('show'), 3000);
    }}
  }}

  function nextSlide() {{
    if (currentSlide < slides.length - 1) {{
      currentSlide++;
      updateSlide();
    }}
  }}

  function prevSlide() {{
    if (currentSlide > 0) {{
      currentSlide--;
      updateSlide();
    }}
  }}

  function jumpToSlide(index) {{
    if (index >= 0 && index < slides.length) {{
      currentSlide = index;
      updateSlide();
    }}
  }}

  // Keyboard navigation
  document.addEventListener('keydown', (e) => {{
    if (e.key === 'ArrowRight' || e.key === ' ') {{
      nextSlide();
      e.preventDefault();
    }} else if (e.key === 'ArrowLeft') {{
      prevSlide();
      e.preventDefault();
    }} else if (e.key === 'Home') {{
      jumpToSlide(0);
      e.preventDefault();
    }} else if (e.key === 'End') {{
      jumpToSlide(slides.length - 1);
      e.preventDefault();
    }} else if (e.key === 'f' || e.key === 'F') {{
      if (document.fullscreenElement) {{
        document.exitFullscreen();
      }} else {{
        document.documentElement.requestFullscreen();
      }}
      e.preventDefault();
    }}
  }});

  // Click zone navigation
  document.querySelector('.zone.prev').addEventListener('click', prevSlide);
  document.querySelector('.zone.next').addEventListener('click', nextSlide);

  // Initialize
  updateSlide();
  document.getElementById('help').classList.add('show');
</script>
</body>
</html>
"""
    
    return html


def main():
    if len(sys.argv) < 3:
        print("Usage: python build_presentation.py <input.json> <output.html>")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    
    if not input_file.exists():
        print(f"Error: Input file {input_file} not found")
        sys.exit(1)
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    title = data.get('title', 'Presentation')
    slides = data.get('slides', [])
    
    html = generate_html(title, slides)
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"Generated presentation: {output_file}")
    print(f"Total slides: {len(slides)}")


if __name__ == '__main__':
    main()
