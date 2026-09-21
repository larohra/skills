# Interrogation Checklist

Use these questions internally before delivering any visual artifact. For each question, require a specific answer, compare it with the good-answer signal, and correct the common failure rather than merely noting it.

## Contents

1. Intent and audience
2. Hierarchy
3. Typography
4. Color
5. Space and layout
6. Data and charts
7. Craft details
8. Distinctiveness
9. Accessibility
10. Medium fit
11. Generic-output smells
12. Hard delivery gate

## Intent and audience

### What must this artifact cause the viewer to understand, feel, decide, or do?

**Good answer:** One concrete outcome stated in plain language, such as "compare three options and approve one" or "spot operational risk within ten seconds."

**Common failure:** A vague purpose such as "share information" that gives no basis for hierarchy.

### Who is the primary audience, and what do they already know?

**Good answer:** A specific audience with a known level of context, vocabulary, attention, and authority.

**Common failure:** Designing for "everyone," which produces generic language and evenly weighted content.

### What is the viewing condition?

**Good answer:** The actual medium and distance: projected in a room, screen-shared, read on a phone, printed on Letter paper, scanned in a spreadsheet, or used interactively at a desk.

**Common failure:** Styling for a desktop screenshot when the artifact will be projected, printed, or used on a narrow screen.

### What is the artifact's register?

**Good answer:** A deliberate energy level appropriate to the stakes: sober, analytical, editorial, optimistic, urgent, technical, playful, or ceremonial.

**Common failure:** Applying the same polished startup aesthetic to a financial control sheet, conference poster, and executive incident report.

### What content is essential, supporting, or optional?

**Good answer:** A ranked content model that permits removal or deferral.

**Common failure:** Treating every supplied sentence, metric, and label as equally prominent.

## Hierarchy

### What does the eye hit first, second, and third?

**Good answer:** Three intentional elements that match the communication goal.

**Common failure:** Naming three elements only after looking closely, or relying on reading order instead of visual order.

### Does the five-second impression match the intended takeaway?

**Good answer:** An unfamiliar viewer can state the purpose and main point after a brief glance.

**Common failure:** The viewer remembers the decoration, company name, or largest chart but not the conclusion.

### Does the hierarchy survive the squint test?

**Good answer:** Blurred masses still reveal one dominant region, clear supporting groups, and a quiet detail layer.

**Common failure:** A field of equally sized cards, labels, and borders with no dominant point.

### Does the hierarchy survive grayscale?

**Good answer:** Scale, position, weight, and spacing preserve the order without hue.

**Common failure:** The primary distinction disappears when accent colors are removed.

### Is emphasis concentrated?

**Good answer:** One focal area uses the strongest scale, weight, contrast, or color; secondary emphasis is clearly weaker.

**Common failure:** Bold type, accent fills, icons, shadows, and badges all compete across the canvas.

### Can any heading or label be removed because position already explains it?

**Good answer:** Redundant labels are removed while essential orientation remains.

**Common failure:** Every container receives a title, subtitle, icon, badge, and helper line.

## Typography

### Why is this typeface appropriate to the content?

**Good answer:** Its proportions, tone, numeral quality, language coverage, or screen/print behavior supports the task.

**Common failure:** "It is modern" or "it is clean" with no relationship to the content.

### Is there a real type scale?

**Good answer:** Named roles use a small set of related sizes and weights, with optical adjustments for actual content.

**Common failure:** Each component has a locally convenient font size.

### Are line-heights tuned by size?

**Good answer:** Display type uses roughly 1.05-1.18, headings 1.1-1.35, body 1.5-1.65, and compact labels 1.25-1.45.

**Common failure:** One global line-height makes headings loose and paragraphs cramped.

### Is tracking intentional?

**Good answer:** Display type above 32px is optically tightened, often around `-0.01em` to `-0.03em`; uppercase labels use controlled positive tracking around `0.04em` to `0.08em`.

**Common failure:** Default tracking everywhere, or letter spacing used decoratively on body text.

### Is the reading measure controlled?

**Good answer:** Sustained body text sits near 60-75 characters per line, with narrower measures for sidebars or large display-led layouts.

**Common failure:** Paragraphs stretch across the full viewport or slide.

### Are weights doing distinct jobs?

**Good answer:** Regular carries reading, medium or semibold marks structure, and bold is reserved for strong emphasis.

**Common failure:** Everything is semibold, or too many near-identical weights create visual noise.

### Are numbers designed for comparison?

**Good answer:** Tabular numerals, aligned decimals, consistent precision, explicit units, and task-appropriate abbreviation.

**Common failure:** Proportional figures wobble in columns, units repeat inconsistently, or meaningless decimals imply false precision.

### Do line breaks and page breaks look authored?

**Good answer:** No orphaned headings, stranded captions, single-word hero lines, or headings separated from their content.

**Common failure:** Automatic wrapping is accepted wherever it lands.

## Color

### What role does each color perform?

**Good answer:** Every color maps to canvas, surface, border, text, muted text, accent, data emphasis, or semantic state.

**Common failure:** Colors were added because the artifact felt empty.

### Is there one primary accent?

**Good answer:** One accent concentrates attention on the primary action, conclusion, or data series.

**Common failure:** Several equally saturated colors distribute attention everywhere.

### Does the palette work by value as well as hue?

**Good answer:** Foreground and background steps remain distinguishable in grayscale.

**Common failure:** Two colors differ in hue but collapse to the same luminance.

### Does text meet contrast requirements?

**Good answer:** Normal text reaches at least 4.5:1, large text reaches at least 3:1, and meaningful interface graphics and focus indicators reach at least 3:1.

**Common failure:** Muted text is lowered until it looks elegant but becomes difficult to read.

### Are semantic colors consistent and redundant?

**Good answer:** Success, warning, danger, and information meanings are stable and paired with text, shape, icon, pattern, or position.

**Common failure:** Red, green, and amber change meaning between sections or act as the only signal.

### Is the background choice helping?

**Good answer:** The canvas supports reading comfort, reproduction, and the intended register.

**Common failure:** Pure black on pure white by habit, or a tinted background that contaminates charts and images.

## Space and layout

### What is the grid?

**Good answer:** A clear column, gutter, margin, and alignment system chosen for the content.

**Common failure:** Components are dragged until they appear approximately balanced.

### What is the spacing scale?

**Good answer:** Repeated gaps come from a named 4px or 8px-based ramp, with rare optical exceptions.

**Common failure:** A field of unrelated values such as 13px, 17px, 21px, and 29px.

### Does proximity express grouping before boxes do?

**Good answer:** Related items sit close, conceptual groups have larger separation, and containers are used only where a boundary is meaningful.

**Common failure:** Every section becomes a card because spacing alone was not considered.

### Are outer margins generous enough?

**Good answer:** The artifact has a visible frame appropriate to its medium and reading distance.

**Common failure:** Content presses against slide, page, viewport, or print edges.

### Are alignment anchors repeated?

**Good answer:** Titles, body text, plot areas, table columns, and controls share visible edges and baselines.

**Common failure:** Each component is internally aligned but unrelated to neighboring components.

### Is asymmetry intentional?

**Good answer:** Unequal columns or offsets create emphasis while preserving stable anchors.

**Common failure:** Accidental drift is defended as dynamic composition.

### Does the layout survive sparse and dense content?

**Good answer:** Empty regions still feel deliberate, while long content wraps, scrolls, paginates, or truncates according to a rule.

**Common failure:** The ideal sample looks balanced but realistic data breaks the design.

## Data and charts

### What exact question does the chart answer?

**Good answer:** A comparison, trend, composition, distribution, relationship, or progress question stated in one sentence.

**Common failure:** A chart exists because the data was available.

### Is the chart form appropriate?

**Good answer:** The encoding matches the analytical task and permits accurate comparison.

**Common failure:** Donuts for many categories, area charts for precise comparison, or 3D effects that distort values.

### Is the scale honest?

**Good answer:** Baselines, intervals, truncation, and normalization are disclosed and chosen for interpretation rather than drama.

**Common failure:** A truncated bar axis exaggerates change or dual axes manufacture correlation.

### Is the answer emphasized rather than every series?

**Good answer:** The important series or interval receives the accent while context remains neutral.

**Common failure:** Default categorical palettes give every series equal saturation.

### Can labels be direct?

**Good answer:** Series, endpoints, targets, and notable events are labeled near the marks, reducing legend travel.

**Common failure:** The viewer repeatedly scans between plot and legend.

### Are units, time ranges, sources, and uncertainty visible?

**Good answer:** Interpretation-critical context is adjacent to the chart, with detail in a note when appropriate.

**Common failure:** A polished plot with unclear units, date range, aggregation, or provenance.

### Is non-data ink earning its place?

**Good answer:** Gridlines, borders, backgrounds, ticks, and annotations support reading.

**Common failure:** Heavy plot frames, dense gridlines, gradients, shadows, and decorative illustrations compete with the data.

### Does the chart remain interpretable without color?

**Good answer:** Direct labels, line styles, shapes, position, or patterns provide redundant distinction.

**Common failure:** Similar lines can be identified only by hue.

## Craft details

### Do borders and shadows describe different planes?

**Good answer:** Borders separate peers; shadows indicate genuine overlap or elevation.

**Common failure:** Every card has both a border and a soft shadow.

### Are corner radii consistent?

**Good answer:** A small radius ramp governs containers, controls, and nested surfaces.

**Common failure:** Buttons, cards, images, and tags each use unrelated radii.

### Do icons match the typography?

**Good answer:** One icon family uses a stroke, fill, size, and optical alignment compatible with adjacent type.

**Common failure:** Mixed outline, filled, emoji, and clip-art symbols.

### Are tables explicitly designed?

**Good answer:** Headers, alignment, number formats, row rhythm, rules, hover or selection states, and overflow behavior support scanning.

**Common failure:** Raw gridlines, default cell padding, and centered values.

### Are empty, loading, error, and long-content states designed?

**Good answer:** Each state preserves layout, explains what happened, and offers the relevant next action.

**Common failure:** Only the ideal populated state was styled.

### Is microcopy specific?

**Good answer:** Labels use direct nouns and verbs, states explain consequences, and units are clear.

**Common failure:** "More," "Submit," "Data," or "Something went wrong" appears without useful context.

### Are optical edges corrected?

**Good answer:** Icons, punctuation, circular shapes, and display text align by appearance rather than bounding box alone.

**Common failure:** Mathematically centered elements look visibly low, high, or inset.

### Is image treatment consistent?

**Good answer:** Crops, aspect ratios, color handling, corner treatment, and captions follow one rule.

**Common failure:** Images arrive with mixed ratios and arbitrary crops that break rhythm.

## Distinctiveness

### What is the one governing idea?

**Good answer:** A concise commitment such as "quiet editorial authority," "dense operational clarity," or "bold scale with monochrome support."

**Common failure:** A list of unrelated adjectives such as modern, clean, premium, dynamic, and friendly.

### What is the single distinctive move?

**Good answer:** One technique tied to the content, such as a scale break, asymmetrical grid, annotation system, chromatic field, direct-label chart, or controlled reveal.

**Common failure:** Distinctiveness is attempted through several decorative effects at once.

### Would anyone guess this came from a template?

**Good answer:** The composition, type, data treatment, and edge cases respond specifically to the supplied content.

**Common failure:** The content could be swapped for another topic without changing the design.

### Is there evidence of optical judgment?

**Good answer:** Line breaks, alignments, crop positions, density, and exceptions were adjusted after rendering.

**Common failure:** Token consistency is mistaken for finished craft.

### Is the memorable part the right part?

**Good answer:** The viewer remembers the idea, conclusion, or action because the visual gesture reinforces it.

**Common failure:** The viewer remembers a gradient, animation, or novelty typeface unrelated to the message.

## Accessibility

### Can the artifact be understood without color?

**Good answer:** Text, shape, position, pattern, or iconography duplicates color-coded meaning.

**Common failure:** Status, series, or priority is carried only by red, amber, green, or brand hues.

### Is all text readable at actual use size?

**Good answer:** The artifact is checked at projected distance, screen zoom, phone width, spreadsheet scale, or printed size as appropriate.

**Common failure:** Readability is judged while zoomed in during authoring.

### Are focus and keyboard states visible and logical?

**Good answer:** Interactive HTML has a clear focus indicator, predictable order, and no keyboard traps.

**Common failure:** Focus outlines are removed to preserve visual cleanliness.

### Is motion optional and purposeful?

**Good answer:** Motion explains change or orientation, remains brief, and respects reduced-motion preferences.

**Common failure:** Continuous ambient motion or parallax is used as a polish signal.

### Is document structure semantic?

**Good answer:** Headings, landmarks, tables, lists, reading order, and alternatives reflect meaning.

**Common failure:** Visual positioning creates an attractive surface with an incoherent reading order.

### Are touch and pointer targets usable?

**Good answer:** Targets are sufficiently large and separated for the intended device, generally around 44px where touch is primary.

**Common failure:** Tiny icon-only actions are packed closely to save space.

### Are accessibility notes treated as design inputs?

**Good answer:** Contrast, type size, wording, and interaction are resolved inside the visual system.

**Common failure:** Accessibility is added late as labels or overrides that feel detached from the design.

## Medium fit

### Does the artifact exploit the strengths of its medium?

**Good answer:** Slides use pacing, web uses interaction and reflow, spreadsheets support scanning and editing, print controls sequence and page craft, and charts prioritize comparison.

**Common failure:** A document is pasted into slides, a slide is embedded as a web page, or a screenshot is treated as a dashboard.

### Has the actual output been rendered?

**Good answer:** The HTML, slide deck, workbook, PDF, or image is viewed in the application or renderer where it will be consumed.

**Common failure:** Source code, object coordinates, or a generation log is accepted as proof.

### Are export-specific failures checked?

**Good answer:** Font substitution, clipping, page breaks, image resolution, transparency, animation loss, and link behavior are tested where relevant.

**Common failure:** The source looks correct but the delivered format changes it.

### Does responsive or print behavior have explicit rules?

**Good answer:** Components reflow, wrap, scroll, paginate, or hide according to deliberate priorities.

**Common failure:** Everything simply shrinks.

### Is density appropriate to attention span and interaction?

**Good answer:** A monitoring dashboard can be dense but scannable; a keynote slide can be sparse and immediate; a reference PDF can sustain detail.

**Common failure:** One density standard is applied to every medium.

## Generic-output smells

Treat any of these as evidence that the elevation pass is incomplete unless the choice is explicitly justified:

- A default system font stack with no reason tied to performance, platform convention, or content.
- Pure `#000000` on pure `#ffffff` used by habit rather than intent.
- Every heading, card, metric, and label carrying similar visual weight.
- Centered text, controls, and sections throughout a reading-heavy artifact.
- Default chart palettes, legends, gridlines, and application typography.
- Drop shadows on every card or panel.
- Emoji used as interface or presentation iconography.
- Body text running at 100% container width on a wide screen.
- Gaps that are almost but not actually consistent.
- Gradients applied to backgrounds, buttons, text, charts, and borders at once.
- Tables with default gridlines, padding, alignment, and number formats.
- Default bullet lists dominating slide layouts.
- Uniform card grids used where the content has a clear priority.
- Excessive rounded rectangles surrounding every content group.
- Decorative blobs, waves, glows, or mesh backgrounds unrelated to meaning.
- Multiple saturated accent colors competing for attention.
- Tiny muted gray text used as a sophistication signal.
- Random icon families or mixed outline and filled icons.
- Over-animation, perpetual movement, or staggered entrances on every element.
- Placeholder-style headings such as "Overview," "Insights," and "Key Metrics" when more specific language is available.

## Hard delivery gate

If any question below is unanswered, the artifact is not ready:

- What must the viewer understand or do?
- What do they see first, second, and third?
- What is the governing design commitment?
- Which system controls type, spacing, color, grid, radius, and elevation?
- Does the hierarchy survive the five-second, squint, and grayscale tests?
- Does all essential text and interaction meet the accessibility floor?
- What is the one distinctive move, and why does it belong?
- What was removed during subtraction?
- Was the actual final output inspected in its intended medium?
