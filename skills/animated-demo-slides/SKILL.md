---
name: animated-demo-slides
description: Create polished animated SVG-based slide presentations to communicate technical ideas clearly. Use this whenever engineers, PMs, or technical leads need to explain complex systems, data flows, performance concepts, architecture decisions, or any technical topic where a visual walkthrough would help non-native English speakers or audiences unfamiliar with the domain understand the key concepts. Perfect for demos, design reviews, technical interviews, and cross-functional presentations where clarity and visual impact matter.
compatibility: null
---

# Animated Demo Slides

Build animated SVG presentations that help an audience understand a system and answer a concrete question. Default to **one self-contained HTML deliverable**, with reproducible source kept alongside the work rather than extra presentation variants.

## Match the workflow to the request

Use supplied context first: audience, question or decision, requested options, approved copy, and the named current artifact. Ask only about material ambiguity. A straightforward one-shot request does not need a fixed number of slides, approval gates, or another intake interview.

- **New deck:** establish the narrative and output contract, then build.
- **Copy-first review:** when requested, or when material narrative choices remain unresolved, agree the copy before styling. In slide-by-slide mode, show the exact title, labels, summary, and key qualifications for one slide, record revisions in the source, and wait for that slide's approval before advancing.
- **Small edit:** update the named current artifact and its reproducible source. A hyperlink or wording correction does not authorize a new deck, a redesign, or reopening settled choices.

Read [authoring.md](references/authoring.md) for output/versioning decisions, copy review, taxonomy, and the bounded release checklist.

## Establish the output contract

Default to a single local HTML file. Follow already specified format, sharing, destination, and versioning choices; clarify unresolved choices before creating extra formats, public/embedded copies, or publishing. Do not automatically export PPTX or video.

Identify the actual latest source and output before changing either. Preserve previous outputs unless replacement is authorized; do not trust an old open tab or rerun a generator against a preserved version. The generator refuses existing outputs by default; `--overwrite` is for an explicitly authorized in-place update, not a shortcut around a versioning decision.

Keep contact sheets, screenshots, and temporary review files internal unless requested. Clean temporary QA files after review without deleting reproducible source or preserved outputs.

## Write for understanding and decisions

Write for someone who was not in the authoring conversation. Use concrete titles, familiar nouns, direct verbs, and short explanations of necessary acronyms or domain terms. State what the slide shows and the intended question, comparison, or decision. Avoid slogans, buzzwords, inflated abstractions, and compressed jargon added to sound smarter, while respecting creative language the user deliberately requests. Preserve meaning, accurate approved terminology, and factual qualifications rather than chasing a word-count reduction.

Inventory all requested alternatives before simplifying. Distinguish peer architectures from genuine variations; do not drop non-preferred options or change the taxonomy to fit a naming scheme. Keep a small glossary or shared slide data so SVG labels, reader text, notes, legends, and reference labels agree. Leave real source URLs and code identifiers unchanged.

Clarify ambiguous domain terms instead of accepting a misleading claim. Distinguish goals, proposals, demonstrated proofs of concept, and production guarantees. Qualify performance claims with their evidence and conditions. Put detailed provenance in notes, but keep caveats needed to interpret a comparison visible on the slide.

## Explain visually first

For each idea, first try a diagram, picture, chart, side-by-side comparison, or before/after view with short, plain labels. Choose the visual that explains the actual relationship, process, or change, not decorative icons or a quota of graphics. Original embedded SVG is a useful default; use properly authorized embedded pictures when they communicate more clearly, without adding image-service calls or dependencies. A compact table or brief prose is still valid when it explains the idea better than a drawing.

Keep detailed explanations and evidence in notes, with accessible reader equivalents and essential caveats still on the slide. Let finite, replayable animation reveal an understandable step or state change; do not use endless decorative motion. Review the result from an unfamiliar reader's perspective: can they explain the main point and takeaway from the slide itself, without the conversation?

## Build from the agreed source

Read [generator.md](references/generator.md) for the JSON schema, command, links, viewer behavior, and focused tests.

```text
python scripts/build_presentation.py deck.json deck.html
```

Keep the existing `title` / `slides` JSON structure; slides accept `name`, `svg`, and `description`. Optional slide titles, visible qualifications, notes, reference links/hotspots, and static SVG alternatives support richer decks without another output format. Use the same approved source for regeneration; do not apply broad search-and-replace across prose, URLs, and code.

Author self-contained SVG with a sensible viewBox, readable text, sufficient contrast, and a meaningful text description. Use motion to reveal relationships, not to carry essential information alone. Supply a readable `static_svg` when the diagram must remain visible with reduced motion; without one, the generator hides the animated diagram and retains the text.

Place supplied references at the diagram or row being discussed using visible native links or hotspots, with equivalent links in reader view and notes. SVG links inside an image are not interactive; use the wrapper's references instead. Preserve commit-pinned URLs and do not fetch references on deck load.

## Validate and deliver once

Use the release checklist in [authoring.md](references/authoring.md): inspect every slide, desktop/mobile layouts, rendered text geometry, keyboard/notes/focus, reader view, reduced motion, and relevant embedding states in one batched pass. Fix observed defects together and confirm once rather than repeatedly polishing new exports.

Navigation is in-memory and does not require history or hash writes. The skip control focuses the content directly, avoiding fragment resolution against an unsafe embedded base URL. Script execution varies by viewer; fullscreen, popups, and host policies are separate constraints. Never relax sandbox or tenant security to make a preview work, or treat simulated embedding as proof of a real deployment.

Verify the actual final file/URL and preserved outputs. Report only validation actually performed and any remaining limitations. HTML/SVG/CSS animation is **not automatically preserved by native PowerPoint conversion**; treat a requested conversion as a separate fidelity decision, not a free extra.

## Reflect once, contribute only with approval

After completing the requested deliverable, briefly assess whether the task revealed a broadly reusable bug, missing instruction, or regression case. This must not delay or gate delivery. Do nothing if there is no useful new lesson, the lesson is already covered or proposed, or a contribution was declined. Do not turn one user's topic, style, or preferences into universal rules.

For an actionable lesson, follow [contributing.md](references/contributing.md): identify the declared contribution repository, deduplicate, show a small sanitized proposal, and obtain explicit publication approval before creating a branch, pushing, or submitting a PR. A prior request explicitly authorizing that contribution and destination already supplies approval. Never infer the destination from an unrelated task repository, publish task data, edit the installed skill, or add runtime callbacks or persistent automation. Reflect once per completed authoring task, not per slide or iteration, and never recurse at the end of a skill-improvement contribution.
