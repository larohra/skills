---
name: design-excellence
description: Use this whenever creating, editing, or reviewing any visual output, including presentations, decks, slides, dashboards, reports, HTML pages, HTML artifacts, web apps, landing pages, spreadsheets, charts, PDFs, diagrams, infographics, posters, email templates, styled READMEs or documentation, UI mockups, themes, and other designed artifacts, and whenever the user asks to "make it look better," polish it, redesign it, improve the visual design, make it less generic, make it feel premium, or elevate an existing first draft; apply a silent design-director refinement process that turns a functional result into a coherent, distinctive, accessible, hand-crafted final artifact.
compatibility: null
---

# Design Excellence

Treat visual quality as part of correctness. Build the artifact, verify that it works, then elevate it before the user sees it. Do not ship the first functional pass.

This skill overlays the native workflow for the requested medium. Use the presentation, spreadsheet, document, PDF, web, diagram, or other authoring skill to produce the artifact, then apply this skill's design system, interrogation, refinement, and verification requirements.

## Recognize the trigger

Apply this skill whenever the output will be looked at, scanned, presented, printed, shared, or used through a visual interface. The user does not need to say "design." A deck, dashboard, spreadsheet, PDF, HTML page, chart, report, diagram, poster, mockup, or styled document already triggers the workflow.

Also apply it to an existing artifact when the user asks to polish, refine, restyle, redesign, professionalize, simplify, modernize, make less generic, or make more visually compelling.

Do not limit the skill to decorative work. Information hierarchy, density, legibility, data clarity, interaction states, responsive behavior, and print behavior are design decisions.

## Build, then elevate

First produce a functional baseline with correct content, structure, calculations, interactions, links, and output format. Keep early styling minimal so weak structure is not disguised by polish.

Then run the ordered refinement in [elevation-protocol.md](references/elevation-protocol.md). Open it whenever creating or materially redesigning a visual artifact. Use every pass at a depth proportional to the artifact's stakes, but never omit the final rendered inspection and subtraction pass.

The operating loop is:

1. Build the correct thing.
2. Establish a design system.
3. Interrogate every visible choice.
4. Add one distinctive move.
5. Subtract what is not earning its place.
6. Render, inspect, correct, and deliver.

Do not expose intermediate drafts merely to demonstrate progress unless the user asks for them. The user sees the elevated result, not the unrefined baseline.

## Work silently by default

Perform the design interrogation internally. Deliver the polished artifact and a brief plain-language note identifying what it is. Do not narrate font selection, spacing iterations, palette exploration, or discarded alternatives unless the user asks to see the design thinking.

Surface rationale only when the user asks, for example "walk me through the design choices" or "show your design thinking," or when a choice requires a real external decision. Real external decisions include an existing brand system, missing required content or data, a mandated audience or medium, and an accessibility requirement that changes the result.

Do not ask permission to be good. Do not ask the user to choose among arbitrary fonts, colors, radii, chart palettes, or layout variants as a substitute for making a defensible choice. Infer the appropriate register from the content and audience, make the decision, and execute it consistently.

## Choose one governing commitment

Give each artifact one governing idea: a typographic voice, a spatial system, a chromatic stance, a strong grid, or another coherent visual premise. Let secondary choices support it quietly.

Concentrate boldness. One strong gesture beats five competing gestures. If the accent color is vivid, keep shape and motion restrained. If typography is expressive, simplify the palette. If the composition is asymmetrical, make spacing and alignment exceptionally disciplined.

Use [design-philosophy.md](references/design-philosophy.md) when the artifact needs judgment about restraint, appropriateness, distinctiveness, or how strongly to follow a reference style. It defines the principles behind the decisions without prescribing a single look.

## Establish the system before styling components

Define the visual system before styling individual cards, slides, cells, panels, or sections. Record it in source tokens, theme values, styles, masters, or a compact internal specification appropriate to the medium.

At minimum, commit to:

- A type system with one or two font families, named text roles, deliberate weights, and a scale rather than unrelated sizes.
- A spacing system based on a repeatable unit, usually a 4px or 8px base for screens and an equivalent modular unit for print.
- Color roles for canvas, surface, raised surface, border, primary text, muted text, accent, and semantic states.
- A grid, column logic, alignment rule, outer margin, and maximum readable measure.
- A radius and elevation ramp, including the deliberate choice to use neither where flat structure is stronger.

Prefer semantic tokens such as `space-3`, `text-muted`, `surface-raised`, and `radius-sm` over local magic numbers. Repeated values must come from the system. Exceptions require an optical reason, not convenience.

Consult [reference-library.md](references/reference-library.md) when selecting type scales, color recipes, spacing systems, or an exemplar family. Borrow observable principles from Stripe, Linear, Apple, Vercel, Bauhaus, Swiss design, editorial print, or Tufte; do not imitate a brand surface or claim insider knowledge about how a company designs.

## Interrogate the artifact

Question every visible decision after the functional baseline exists. Ask what the eye sees first, whether the hierarchy matches the user's goal, whether the type carries the right voice, whether space is doing enough work, whether color has a role, and whether any effect exists only because it was easy to add.

Use [interrogation-checklist.md](references/interrogation-checklist.md) before delivery. Answer its questions internally and correct weak answers. Do not turn the checklist into user-facing commentary unless requested.

Run these fast perception tests:

- **Five-second test:** after five seconds, can an unfamiliar viewer state the artifact's purpose and primary takeaway?
- **Squint test:** when detail blurs, do the intended first, second, and third levels remain obvious?
- **Grayscale test:** does hierarchy survive without hue?
- **Delete-it-and-see test:** if an effect, color, line, icon, or label disappears, is meaning or orientation lost? If not, remove it.

## Use specific techniques, not generic decoration

Select techniques for the effect needed: hierarchy, depth, rhythm, emphasis, density, motion, or data clarity. Do not begin with a fashionable effect and search for somewhere to apply it.

Open [technique-catalog.md](references/technique-catalog.md) when the baseline is correct and the artifact needs concrete values or one distinctive move. Use its techniques selectively. Apply exactly one memorable gesture unless the format clearly demands a coordinated sequence.

Distinctiveness can come from composition, crop, scale contrast, a controlled rule system, an editorial data treatment, or intentional asymmetry. It does not require gradients, glass effects, oversized shadows, novelty fonts, or constant motion.

## Adapt to the medium

The same design principles apply across media, but the failure modes and verification methods change.

### HTML and web artifacts

Design all meaningful states, not only the ideal desktop screenshot. Include responsive behavior, keyboard focus, hover and active states where relevant, loading and empty states, long-content behavior, and reduced motion. Keep body measure near 60-75 characters. Use fluid layout deliberately; do not stretch readable text to the viewport width.

Use real semantic structure. Effects must not obscure interaction affordances. Motion should explain state change, preserve orientation, or direct attention; decorative motion must be brief and removable.

### Slide decks

Make each slide communicate one idea and give it an obvious reading order. Prefer visual explanation over paragraphs. Use large type that survives the actual room or screen-share context, generous safe margins, repeated alignment anchors, and restrained transitions.

Avoid default title-and-bullets layouts, miniature dashboards, and dense body copy. A deck is paced in time; vary composition while preserving a stable system. Render every slide and inspect the sequence, not just individual canvases.

### Spreadsheets

Treat structure, number formats, frozen regions, widths, alignment, hierarchy, and error states as design. Use typography, spacing, rules, and restrained fills to separate inputs, calculations, and outputs. Do not paint every cell.

Use tabular numerals for comparable values. Align decimals and units. Keep semantic colors consistent and provide non-color cues. Charts must inherit the workbook's type, color, and hierarchy system rather than retaining application defaults.

### PDF and print

Design for the physical or fixed page. Control trim, margins, running elements, page breaks, widows, orphans, image resolution, and black density. Check the artifact at actual size and in a thumbnail view. Make links, footnotes, captions, and page references legible after export.

Account for grayscale printing and avoid edge-dependent content outside safe margins. A screen preview is not sufficient evidence of a successful print artifact.

### Data and charts

Choose the chart from the analytical question, not from visual novelty. Label directly when possible, reduce legend travel, order data meaningfully, and remove non-data ink that does not improve interpretation. Preserve honest scales and show uncertainty, targets, or comparison baselines when they matter.

Use color to emphasize the answer, not to assign a different hue to every series. Format numbers consistently, include units, and use tabular numerals in dense comparisons. A chart must remain interpretable without relying on color alone.

### Diagrams and infographics

Use direction, grouping, and alignment to make the relationship legible before decoration. Keep connector semantics consistent. Match icon weight to type weight and avoid mixing illustration languages.

Do not use icons as substitutes for labels when the meaning is not universal. Test the diagram at the size at which it will actually be consumed.

## Treat accessibility as the floor

Accessibility and legibility are non-negotiable constraints, not optional cleanup.

For screen content, target at least 4.5:1 contrast for normal text and 3:1 for large text and meaningful interface graphics. Do not use muted text below readable contrast merely to make the page feel refined. Keep body text generally at 16px or larger on the web, presentation body text large enough for the room, and print body text appropriate to the typeface and reproduction method.

Provide visible focus states, logical keyboard order, semantic headings, text alternatives where needed, and sufficiently large targets. Respect reduced-motion preferences. Do not encode status, series, priority, or error using color alone; add labels, shapes, patterns, position, or icons.

Accessibility can sharpen the design. Resolve conflicts through hierarchy, wording, spacing, and stronger role separation rather than by quietly lowering the accessibility bar.

## Exercise restraint

Use no more than two font families unless the content itself requires another script or specialist face. Use one primary accent color plus semantic status colors. Keep radius choices to a small named ramp, usually two or three values. Use one shadow family, if any.

Do not stack gradients, glows, glass panels, thick borders, oversized radii, multiple icon styles, and decorative motion in the same artifact. Avoid drop shadows on every container. Prefer spacing and tonal separation before borders; prefer borders before shadows when the goal is simple grouping.

Centering is a special-purpose composition, not a default alignment. Use left alignment for sustained reading in left-to-right languages. Avoid evenly weighting every section; hierarchy requires contrast.

## Verify the rendered result

Inspect the actual artifact, not only its source. Use browser screenshots for HTML, rendered slides for decks, exported pages for PDF and print, and application or file previews for spreadsheets. Check representative narrow and wide layouts, dense and sparse content, and at least one edge case.

Confirm that:

- The first, second, and third points of attention are intentional.
- Type roles, spacing, colors, radii, borders, and elevation consistently use the system.
- The distinctive move strengthens the idea rather than competing with it.
- No default chart, table, bullet, or control styling remains accidentally.
- Content is not clipped, crowded, stretched, or stranded by page and viewport changes.
- Contrast, focus, reduced motion, reading order, and non-color cues meet the accessibility floor.
- At least one unnecessary effect, color, weight, border, or label was removed during refinement.

If any answer is uncertain, continue refining. "Looks good" is not an exit test.

## Tell the user only what helps

Deliver the final artifact and identify it in plain language. Mention material constraints or limitations that remain. Do not provide a diary of the elevation process, a list of rejected fonts, or self-congratulatory claims about polish.

If the user asks for rationale, explain the governing commitment, the hierarchy, the system, the distinctive move, and the major accessibility decisions. Keep the explanation tied to what the artifact needs to accomplish.

## Know when to break the rules

Do not flatten a deliberate creative direction into safe corporate polish. If the user asks for eccentric, maximal, raw, playful, retro, brutalist, ornamental, or otherwise unusual work, preserve that intent and apply the same rigor to its internal system, legibility, and craft. Break conventions deliberately, consistently, and in service of the content.
