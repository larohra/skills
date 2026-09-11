# Editing, narration, music, and highlights

## Preserve the original

Never overwrite the silent master. Produce `demo.mp4` and
`demo-enhanced.mp4`. Insert chapters by splitting and concatenating the master;
do not re-record completed browser scenes.

## Narration

On Windows, use `System.Speech.Synthesis.SpeechSynthesizer`. Microsoft Mark is a
clear technical default; Zira is a good alternative.

- Generate one WAV per segment.
- Measure every WAV with `ffprobe`.
- Schedule starts so speech does not overlap.
- Narrate capability claims, not every click.
- Keep sentences short enough for the visible scene and use
  `check_narration_gaps.py` to leave at least 0.8 seconds by default.
- Do not finalize audio before the silent rough cut and visual claim-evidence
  review are approved. If a narration claim cannot be located in a visible
  frame, revise it or repair the capture.

## Background music

Prefer subtle generated ambient music to avoid licensing issues. A low-volume
three-note sine bed with filtering/reverb is sufficient. Fade in/out and mix at
roughly 15–25% of its already-low source level.

Check final audio:

```powershell
ffmpeg -i output.mp4 -af volumedetect -f null NUL
```

A sensible target is approximately `-24 dB` mean and below `-2 dB` peak.

## Highlights

Create full-frame transparent PNGs with Pillow:

- 5–6 px rounded rectangle;
- orange or cyan accent;
- dark label card;
- short title and one-line explanation;
- arrow ending inside the target region.

Apply with FFmpeg `overlay` and `enable='between(t,start,end)'`. Inspect actual
frames before choosing coordinates.

Highlight correlation IDs, performance metrics, trace trees, session status,
identity/blueprint, evaluation/guardrail controls, and inventory rows.

## Retiming after insertion

When inserting a chapter at `T` with duration `D`, shift every later narration
start, overlay window, storyboard timestamp, and chapter marker by `D`.

## Review

- Generate a contact sheet every 10–20 seconds.
- Inspect specific frames around every overlay, plus each declared claim,
  scene midpoint, and both sides of every transition.
- Verify codecs/sample rate/duration with `ffprobe`.
- Open the enhanced MP4 in a browser/video canvas for user review.
- Read [editorial-qc.md](editorial-qc.md) for the reusable JSON-backed checks.
