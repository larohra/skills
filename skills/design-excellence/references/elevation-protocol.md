# Elevation Protocol

Use this ordered refinement process after a functional visual artifact exists and before delivery. Every pass has an entry condition, concrete moves, and an exit test so refinement produces evidence rather than taste commentary.

## Contents

1. Calibrate the time budget
2. Pass 0 - Functional baseline
3. Pass 1 - System
4. Pass 2 - Hierarchy
5. Pass 3 - Typography
6. Pass 4 - Space
7. Pass 5 - Color and contrast
8. Pass 6 - Detail and craft
9. Pass 7 - Distinctive move
10. Pass 8 - Subtraction
11. Pass 9 - Verification
12. Final release gate

## Calibrate the time budget

Match refinement depth to lifespan, audience, and consequence. Do not use "internal" as permission to skip basic hierarchy or accessibility.

### Quick internal artifact

Examples include a one-time team chart, a working spreadsheet, a meeting diagram, or a short-lived status page.

Run every pass, but keep Passes 6 and 7 narrow. Use an existing system where available. Spend the most attention on hierarchy, spacing, number formatting, and legibility. One rendered review at representative size is sufficient if there are no responsive or print requirements.

### Reusable operational artifact

Examples include a recurring report, team dashboard, reusable spreadsheet, documentation page, or standard presentation.

Run every pass at normal depth. Define reusable tokens and styles, design edge states, test representative data extremes, and verify at least two sizes or output conditions.

### External or high-stakes deliverable

Examples include an executive deck, customer-facing report, product launch page, public infographic, investor material, conference presentation, or regulated communication.

Run every pass at full depth. Inspect every page, slide, or major state. Test multiple viewport or print conditions. Verify accessibility explicitly. Give typography, data integrity, image reproduction, and export behavior the same attention as the visible composition.

If time is constrained, simplify the artifact rather than shipping an elaborate but unresolved design. Fewer components with complete craft outperform more components with partial craft.

## Pass 0 - Functional baseline

### Entry condition

The requested medium, content, data, and primary user task are known well enough to build the artifact.

### Concrete moves

Build the simplest complete version. Confirm:

- Content is accurate, complete, and ordered correctly.
- Calculations, filters, interactions, links, and navigation work.
- Tables contain the required fields and use correct units.
- Charts answer a real analytical question and use honest scales.
- Slides or pages form a coherent narrative.
- Responsive, print, or export requirements are represented structurally.
- Empty, error, loading, overflow, and long-content states exist where relevant.

Use default or minimal styling. Do not compensate for weak structure with color, cards, illustration, or effects.

Name the artifact's primary task in one sentence. Name the primary audience in one phrase. Name the one thing the viewer must notice or understand first.

### Exit test

The artifact works, says the right thing, and can be evaluated without visual polish. If it fails here, fix function and content before proceeding.

## Pass 1 - System

### Entry condition

The baseline is functionally correct and its major content regions are stable.

### Concrete moves

Choose one governing commitment: typographic, spatial, chromatic, or compositional. Write it as a constraint, such as "editorial typography with quiet rules" or "dense operational grid with one high-visibility accent."

Define named tokens or styles before styling instances.

### Type system

Use one family for most artifacts and two only when the second has a clear role. Define roles such as:

- `display`: 40-64px screen equivalent, weight 600-750, line-height 1.05-1.18.
- `title`: 28-40px, weight 600-700, line-height 1.1-1.25.
- `heading`: 20-28px, weight 600-700, line-height 1.2-1.35.
- `body`: 15-18px, weight 400-500, line-height 1.5-1.65.
- `small`: 12-14px, weight 450-600, line-height 1.35-1.55.
- `label`: 11-13px, weight 600-700, line-height 1.2-1.4, tracking 0.02-0.08em when uppercase.

Use a consistent ratio, commonly 1.2 or 1.25, then make optical adjustments rather than inventing unrelated sizes.

### Spacing system

Use a 4px base for dense interfaces and spreadsheets or an 8px base for spacious pages and slides. A practical screen ramp is:

`2, 4, 8, 12, 16, 24, 32, 48, 64, 96`

Name values by role or step. Use the same ramp for gaps, padding, margins, and section rhythm. Optical exceptions may differ by 1-2px, but record why.

### Color roles

Define roles, not a bag of swatches:

- `canvas`
- `surface`
- `surface-raised`
- `border-subtle`
- `border-strong`
- `text`
- `text-muted`
- `accent`
- `accent-contrast`
- `success`
- `warning`
- `danger`
- `info`

Create state variants only where interaction requires them. Semantic colors must remain distinct in grayscale or carry a second cue.

### Grid and measure

Define outer margins, column count, gutter, alignment anchors, and maximum content width. For sustained screen reading, keep measure near 60-75 characters. For data-dense surfaces, define fixed alignment columns and where horizontal scrolling is acceptable.

Use a 12-column grid only when it helps. Four, six, eight, or a simple main-plus-aside structure may fit the content better. A grid is an alignment contract, not a default number.

### Radius and elevation

Define no more than three radii, such as `4px`, `8px`, and `16px`, or choose square corners. Define no more than three elevation levels. Prefer tonal surface changes and borders for ordinary grouping; reserve shadows for genuine overlap or lift.

### Exit test

Every repeated visible value can be traced to a token, named style, master, theme, or documented rule. The system can style a new component without inventing new values.

## Pass 2 - Hierarchy

### Entry condition

The system exists and the content regions have been styled enough to reveal their relative importance.

### Concrete moves

Rank the intended reading order:

1. Primary message, decision, or metric.
2. Supporting explanation or comparison.
3. Context, provenance, controls, or detail.

Use scale, weight, position, spacing, and contrast in that order before adding decoration. Ensure each major region has one clear entry point.

Perform the five-second test. Show or view the artifact for five seconds, then look away. State its purpose, primary takeaway, and next action. If any answer is wrong, the hierarchy is wrong.

Perform the squint test. Reduce detail by squinting, zooming out, or applying blur mentally. The dominant mass should correspond to the primary message, and secondary groups should remain visibly grouped.

Perform the grayscale test. Remove or simulate the loss of hue. Hierarchy must survive through value, scale, position, and weight.

Check that supporting labels are quieter without becoming unreadable. Check that every card or panel is not shouting at the same volume. Reduce weight before adding more weight elsewhere.

### Exit test

An unfamiliar viewer identifies the intended first, second, and third points of attention in the correct order within five seconds, and that order survives squinting and grayscale.

## Pass 3 - Typography

### Entry condition

The hierarchy is directionally correct and the type roles are defined.

### Concrete moves

Tune size, weight, line-height, tracking, measure, alignment, and numeric behavior as a system.

Use line-height by role:

- Display: 1.05-1.18.
- Large heading: 1.1-1.25.
- Small heading: 1.2-1.35.
- Body: 1.5-1.65.
- Labels and compact table text: 1.25-1.45.

Tighten tracking above 32px, commonly around `-0.01em` to `-0.03em` depending on the face. Do not tighten faces that already space display cuts aggressively. Add tracking to uppercase labels, commonly `0.04em` to `0.08em`. Avoid letter-spaced lowercase body text.

Keep body measure near 60-75 characters. Narrow to 45-60 characters for sidebars or large display-led pages. Avoid 100%-width paragraphs on wide screens.

Use tabular numerals for metrics, financial values, timestamps, ranks, and columns that must compare vertically. Align decimals and units. Use oldstyle numerals only where editorial tone matters more than rapid comparison.

Match weight to size. Small light text fails quickly; use at least regular or medium weight for small labels. Avoid fake bold, fake italics, and too many adjacent weights.

For diagrams, slides, and demos, distinguish source type size from effective rendered size. A label authored at a nominally acceptable size can become unreadable when a full canvas is fitted into a lower-resolution viewport. Before adding outlines or shadows, increase critical-label size and weight, shorten the label, or reduce surrounding density. If a light label sits on a colored status surface, darken the surface enough to preserve contrast; a narrow contrasting keyline is a fallback for display degradation, not a substitute for adequate size and contrast.

Prevent orphaned headings, single-word final lines in prominent copy, stranded captions, and headings detached from their content. Keep a heading with at least two lines of following content where the medium permits.

Apply optical alignment. Align the visible edge of glyphs and icons, not only their bounding boxes. Allow punctuation or large quotation marks to hang slightly when it improves the text edge.

Use sentence case by default. Use uppercase for brief labels, not paragraphs or long navigation.

### Exit test

Text remains comfortable at actual use size, line breaks look intentional, numeric comparisons scan cleanly, and no type role requires a one-off size or spacing patch to function.

## Pass 4 - Space

### Entry condition

Typography is stable enough that text geometry will not substantially change.

### Concrete moves

Use spacing as the primary hierarchy tool. Increase space between conceptual groups and reduce space within a group. Do not use boxes where proximity is enough.

Audit every gap against the spacing scale. Replace accidental values. Look especially for near-duplicates such as 15px beside 16px or 22px beside 24px.

Set outer margins generously enough to frame the artifact:

- Compact web tools: commonly 16-24px on small screens and 24-48px on large screens.
- Editorial or marketing pages: commonly 24px small-screen margins and 64-120px large-screen margins.
- Slides: commonly 5-8% of canvas width as a safe outer margin.
- Print: choose margins from trim size, binding, and reading distance, not screen conventions.

Build vertical rhythm around repeated intervals. Major section separation should be visibly larger than component separation, often 1.5-2 times the internal gap.

Align to common anchors. Fix almost-aligned edges, baselines, chart plot areas, table columns, and icon-text pairs. Distinguish deliberate asymmetry from accidental drift.

Check dense and sparse cases. Empty space should look intentional when content is short; long content should not collapse the hierarchy.

### Exit test

The artifact can be understood through grouping before reading labels. Every gap appears to belong to a small system, and no inconsistent spacing calls attention to itself.

## Pass 5 - Color and contrast

### Entry condition

Hierarchy and grouping work in grayscale.

### Concrete moves

Assign color by role. Use one primary accent for focus, action, or the central data series. Do not distribute accent color evenly; concentration creates emphasis.

Keep neutral steps visibly distinct. Adjacent surfaces should differ enough to establish structure without creating stripes. Borders should be quieter than text and stronger than imperceptible decoration.

Target at least 4.5:1 contrast for normal text and 3:1 for large text. Target at least 3:1 for meaningful interface graphics, focus indicators, and component boundaries when those boundaries are needed to identify controls.

Use semantic colors consistently. Success, warning, danger, and information states must not reuse the accent merely for convenience. Pair state colors with labels, icons, patterns, or position.

Check dark themes independently. Do not invert a light palette mechanically. Reduce the area and intensity of luminous accents, avoid pure white for large text fields, and use elevation through lighter surfaces rather than darker shadows.

Avoid pure `#000000` on pure `#ffffff` by default for large reading surfaces when a near-black and slightly tinted canvas provide equivalent clarity with less glare. Use pure extremes when the medium, brand, or reproduction process benefits from them.

### Exit test

Every color has a named role, all essential contrast checks pass, the artifact remains understandable without hue, and the accent clearly indicates what deserves attention.

## Pass 6 - Detail and craft

### Entry condition

The system, hierarchy, typography, spacing, and color are stable.

### Concrete moves

Inspect at 100% and at thumbnail size.

Choose borders or shadows according to meaning. Use borders for separation on the same plane. Use shadows for overlap, lift, or temporary layers. Do not use both on every surface.

Match icon size and stroke weight to adjacent type. A 16px icon commonly pairs with 13-16px text; a 20-24px icon suits larger controls or headings. Use one icon family. Align icons optically, often 1px above or below geometric center.

Keep corner radii consistent. Nested containers should use related radii; inner radius commonly equals outer radius minus padding, within optical reason.

Choose table treatment deliberately:

- Use subtle horizontal rules for scan-heavy tables.
- Use zebra striping only when rows are long or dense enough to lose place.
- Avoid vertical rules unless column separation is otherwise ambiguous.
- Give headers stronger type and spacing before adding heavy fills.

Format numbers for the task. Use consistent precision, thousands separators, currency placement, percentages, negative values, dates, time zones, and abbreviations. Do not show meaningless decimals.

Write microcopy that explains action and state. Replace vague labels such as "Submit" or "More" when a more specific verb fits. Design empty states to explain why the state is empty and what to do next.

Inspect line endings, punctuation, capitalization, icon labels, chart labels, footnotes, legends, and source notes. Small inconsistencies are highly visible once the large system is quiet.

### Exit test

No component appears to come from an unrelated template, edge states are designed, numbers and labels are consistent, and close inspection reveals intentional alignment rather than accidental offsets.

## Pass 7 - Distinctive move

### Entry condition

The artifact is coherent, legible, and complete but may still feel generic.

### Concrete moves

Select exactly one memorable gesture from `technique-catalog.md` that reinforces the content. Examples include:

- A decisive scale break for the primary metric.
- An editorial side note or marginal annotation system.
- A controlled asymmetrical grid.
- A single chromatic field that frames the main idea.
- Direct labels integrated into a chart.
- A repeated rule or crop that creates rhythm.
- A purposeful reveal that explains a process.

Apply the move to one focal region or as one repeated rule. Do not add a second competing gesture.

Check appropriateness. A finance dashboard may use a crisp comparative data treatment; a launch page may support a more theatrical composition. Distinctive does not mean loud.

### Exit test

The artifact has one identifiable visual idea that a viewer could describe, and removing it would make the communication less effective or less specific to the content.

## Pass 8 - Subtraction

### Entry condition

All intended content and the distinctive move are present.

### Concrete moves

Remove at least one visible choice that is not earning its place. This pass is mandatory.

Run the delete-it-and-see test on:

- Every shadow.
- Every border.
- Every background tint.
- Every accent-colored element.
- Every icon.
- Every label repeated by position or context.
- Every font weight.
- Every decorative shape.
- Every animation.
- Every card container.

Delete one candidate and compare. If meaning, hierarchy, orientation, or affordance does not weaken, keep it deleted.

Merge adjacent containers where spacing can establish grouping. Reduce multiple emphasis methods to one. Remove repeated headings when the section is self-evident. Shorten explanatory copy after the visual structure carries its share.

### Exit test

At least one effect, color, weight, border, label, container, or animation has been removed, and every remaining visible choice can defend its role.

## Pass 9 - Verification

### Entry condition

The refined artifact is complete in its intended output format.

### Concrete moves

Inspect the rendered artifact rather than trusting source.

For HTML and web:

- Capture representative wide and narrow screenshots.
- Test keyboard navigation, visible focus, hover, active, empty, loading, and error states.
- Test reduced motion.
- Check long text, long numbers, zoom, and responsive reflow.

For slides:

- Render every slide.
- Inspect thumbnails for pacing and system consistency.
- Inspect actual presentation size for readability.
- Inspect projected or demo decks at a realistic lower-bound viewport, such as 1366×768 in fit-to-window mode, without authoring zoom.
- Check overflow, safe margins, image quality, and transition restraint.

For spreadsheets:

- Open or render the workbook.
- Check frozen panes, widths, row heights, number formats, print area, filters, and formulas.
- Test a sparse case and a dense case.
- Inspect charts for default styles and clipped labels.

For PDF and print:

- Inspect exported pages at thumbnail and 100%.
- Check page breaks, widows, orphans, bleeds, margins, image resolution, links, and grayscale behavior.
- Verify fonts embedded or reproduced correctly.

For charts and diagrams:

- Check labels at final size.
- Check critical labels after the full diagram has been scaled into its intended viewport; vector output alone does not guarantee legibility.
- Verify scale integrity, units, source notes, direct labeling, and non-color differentiation.
- Confirm connectors, arrows, and reading direction remain clear.

Cross-check the artifact against `interrogation-checklist.md`. Repeat any failed pass rather than patching symptoms locally.

### Exit test

The actual output works in its intended environment, passes accessibility and medium checks, survives edge cases, and has no unresolved checklist gate.

## Final release gate

Do not deliver until every answer is yes:

- Is the content correct and complete?
- Is the intended first impression obvious within five seconds?
- Does hierarchy survive squinting and grayscale?
- Are repeated choices governed by a system?
- Is typography readable at actual size?
- Is color role-based and accessible?
- Is one distinctive move present and appropriate?
- Was at least one unnecessary element removed?
- Was the final rendered artifact inspected in its intended medium?
