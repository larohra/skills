# Visual technique catalog
Consult this file when an artifact works but needs a specific visual move to improve hierarchy, depth, rhythm, attention, typography, color, composition, data display, motion, or finish.
## Establishing hierarchy
### Clear size jumps
- Make adjacent hierarchy levels differ by at least 1.33x when size carries the distinction: 18px body to 24px heading, or 36px heading to 48px display.
- Use a larger jump for the primary claim: 16px body, 24px section title, 48-64px artifact title. Failure mode: 18px, 20px, and 22px create hierarchy that is technically different but visually muddy.
### Weight contrast
- Use meaningful weight steps: 400 body, 600 labels and subheads, 700 display or critical totals.
- Pair weight with size or color when the text levels must read instantly.
- Avoid 500 versus 600 as the only distinction; rendering differences are often too subtle. Failure mode: everything at 600 makes the page feel loud and removes the ability to emphasize.
### Text color tiers
- Define primary, secondary, and tertiary text as roles, not one-off colors.
- On a light surface, start near `#18181B`, `#52525B`, and `#71717A`; verify contrast in the actual size and weight.
- On a dark surface, start with white at 92%, 68%, and 44% opacity.
- Reserve tertiary text for metadata, timestamps, and optional guidance, never required instructions.
```css
:root {
--text-primary: #18181b; --text-secondary: #52525b; --text-tertiary: #71717a;
}
[data-theme="dark"] {
--text-primary: rgba(255, 255, 255, 0.92); --text-secondary: rgba(255, 255, 255, 0.68); --text-tertiary: rgba(255, 255, 255, 0.44);
}
```
### Spatial isolation
- Give the most important element more empty space than its neighbors: 32-48px around a key metric inside a card that otherwise uses 16-24px gaps.
- Isolate a primary decision or takeaway in its own column, band, or page region. Failure mode: placing the important element in a crowded card and compensating with brighter color.
### Eyebrow plus headline
- Put a 11-13px uppercase or semibold category label 8-12px above a 32-64px headline.
- Use `letter-spacing: 0.06em` to `0.1em` for the eyebrow; keep the headline normal case.
- Let the eyebrow name the category and the headline make the claim. Failure mode: repeating the same phrase twice or using an eyebrow above every card.
### Rule above heading
- Add a 1px rule 12-20px above a section title to mark a new chapter without a box.
- Use a full-width rule for reports and a 24-48px short rule for editorial compositions.
- Keep the rule low contrast, or use the accent only for the most important section. Failure mode: rules above every minor heading produce visual picket fencing.
### Indentation and hanging indents
- Indent subordinate rows by 16-24px rather than shrinking all their text.
- Use hanging indents for numbered steps, references, and icon-label lists so multiline text aligns with the first line.
- Set list markers in a fixed 24-32px column. Failure mode: nested indentation deeper than three levels consumes the content width and hides structure.
```css
.step {
  display: grid;
  grid-template-columns: 2rem 1fr;
  column-gap: 0.75rem;
  align-items: start;
}
```
### Hierarchy through case
- Use sentence case for nearly everything.
- Reserve uppercase for short labels under roughly 20 characters.
- Keep acronyms as required by the domain, but do not turn headings into all-caps banners. Failure mode: uppercase paragraphs slow reading and look like generated UI chrome.
## Creating depth without clutter
### Hairline borders before shadows
- Separate adjacent light surfaces with `1px solid rgba(24,24,27,.10)`.
- On dark surfaces, start with `1px solid rgba(255,255,255,.08)`.
- Use borders for structure and shadows for elevation; do not use both at full strength. Failure mode: dark 1px borders around every card create a spreadsheet-like cage.
### Layered surface roles
- Define three surfaces: base, raised, and overlay.
- Light example: `#F7F7F5`, `#FFFFFF`, `#FFFFFF` plus shadow.
- Dark example: `#0B0C0E`, `#121418`, `#191C21`.
- Move one step per elevation level; large jumps look like unrelated themes.
### Realistic shadow ramps
- Use multi-layer shadows with a tight contact shadow and a broad ambient shadow.
- Keep shadows neutral or lightly tinted toward the background hue.
- Scale blur and offset with elevation; do not simply increase opacity.
```css
:root {
--shadow-1:
    0 1px 2px rgba(20, 20, 24, 0.08),
    0 1px 1px rgba(20, 20, 24, 0.04);
--shadow-2:
    0 8px 24px rgba(20, 20, 24, 0.10),
    0 2px 6px rgba(20, 20, 24, 0.06);
--shadow-3:
    0 24px 64px rgba(20, 20, 24, 0.16),
    0 6px 18px rgba(20, 20, 24, 0.08);
}
```
- Failure mode: one heavy `0 10px 30px rgba(0,0,0,.3)` shadow on every surface.
### Inner highlight on dark UI
- Add `inset 0 1px 0 rgba(255,255,255,.06)` to raised dark surfaces.
- Combine it with a low-alpha outer border to define the top edge.
- Use it on panels and controls, not on every row. Failure mode: opacity above roughly 0.1 creates a beveled, game-interface look.
### Backdrop blur
- Use `backdrop-filter: blur(12px)` only when content actually passes behind a persistent overlay.
- Pair blur with a sufficiently opaque fill such as `rgba(15,16,19,.78)`.
- Provide a solid fallback; never rely on blur for text contrast. Failure mode: translucent cards floating over a static background add cost without communicating depth.
### Z-order discipline
- Establish a short elevation scale such as 0 content, 10 sticky, 20 dropdown, 30 modal, 40 toast.
- Keep decorative layers below interactive content and set `pointer-events: none`.
- Document exceptions rather than escalating to arbitrary values like 99999. Failure mode: stacking contexts created by transforms make overlays disappear unpredictably.
## Rhythm and spacing
### Modular spacing scale
- Use a 4px base: `4, 8, 12, 16, 24, 32, 48, 64, 96, 128`.
- Use 4-12px inside compact controls, 16-32px inside components, and 48-128px between major regions.
- Skip a step when changing semantic level. Failure mode: arbitrary values such as 17px and 29px make alignments drift.
### Vertical rhythm
- Choose a default body line-height, then align major gaps to multiples near that rhythm.
- For 16px body at 24px line-height, use 24px paragraph gaps, 48px section gaps, and 72-96px chapter gaps.
- Let images and charts break the baseline deliberately, then rejoin it below. Failure mode: equal 24px gaps everywhere flatten section boundaries.
### Proximity grouping
- Keep elements within a group closer to each other than to neighboring groups.
- Start with 8px label-to-value, 16px item-to-item, and 32px group-to-group.
- Remove a container if spacing alone communicates the grouping. Failure mode: cards become the default response to every grouping problem.
### Heading space asymmetry
- Put more space above a heading than below it.
- A practical pattern is 48px above and 16px below for sections, or 32px above and 12px below for subsections.
- At a page or slide top, remove the unnecessary top gap. Failure mode: equal space above and below makes headings float between sections.
### Optical centering
- Move text and icons 1-3px when their visual mass looks off despite mathematical centering.
- Raise play triangles and chevrons slightly; lower all-caps labels if the cap height feels top-heavy.
- Judge at final size, not only at 400% zoom. Failure mode: large manual offsets hide an incorrect icon viewBox or line-height.
### Outer margin versus inner gaps
- Make outer page margins visibly larger than component gaps.
- For desktop, try 64-96px outer margins with 24-32px grid gutters.
- For slides, keep a consistent safe margin near 5-8% of canvas width. Failure mode: 24px at the viewport edge and 32px between cards makes the canvas feel cramped.
### Negative space as content
- Leave one intentionally quiet region around the main claim, image, or decision.
- Use empty columns or an unfilled lower third to create anticipation and focus. Failure mode: filling every gap with metadata, badges, icons, or decoration.
## Directing attention and emphasis
### Single accent under 10 percent
- Use one accent color across less than roughly 10% of the visible surface area.
- Spend it on the primary action, selected state, key data series, or one takeaway.
- Let neutral contrast do the remaining work. Failure mode: accent backgrounds, icons, links, headings, and chart series all compete.
### Accent on neutral
- Build the artifact in neutrals first, then introduce the accent.
- Check that the focal point remains clear in grayscale before relying on hue.
- Use a paler accent tint for backgrounds and the saturated accent for small marks. Failure mode: several saturated brand-adjacent colors turn the layout into a palette sample.
### Saturation and value contrast
- Increase either saturation or light-dark value for emphasis; rarely maximize both.
- On dark UI, a pale high-value accent often reads cleaner than a neon saturated one.
- On light reports, a deep low-value accent supports small text and rules. Failure mode: fluorescent color on white causes vibration and weakens adjacent text.
### Size-of-one
- Make exactly one number, image, or sentence much larger than everything around it.
- Use this for the governing metric or artifact thesis: 64-120px type in slides, 40-72px in reports.
- Keep its supporting label short and nearby. Failure mode: several oversized metrics create a dashboard of competing billboards.
### Asymmetric placement
- Place the main element around one-third or two-thirds of the canvas instead of dead center.
- Balance it with whitespace, a smaller annotation, or a secondary visual mass.
- Keep alignment edges precise even when the composition is asymmetric. Failure mode: arbitrary off-centering reads as an alignment error.
### Isolated element
- Separate one control, card, or annotation from a cluster by at least one spacing-scale jump.
- Use isolation for the exception, recommendation, or decision point. Failure mode: isolate multiple elements and the page loses a clear group.
### Motion on entry
- Reveal the key visual after the frame and title are established.
- Use opacity plus 8-24px translation, not scale from zero.
- Keep the final state stable and readable. Failure mode: every element animates independently and delays comprehension.
### Highlight bands
- Place a pale horizontal band behind one sentence, row, or interval.
- Use 6-12px vertical padding and let the band extend slightly beyond the text block.
- In charts, use a low-alpha band to mark a time window or target range. Failure mode: marker-yellow bands behind several paragraphs resemble search results.
### Arrows and connectors
- Use connectors to encode direction or dependency, not decoration.
- Prefer orthogonal routes in systems diagrams and smooth curves in narrative flows.
- Keep line width 1.5-2px, arrowheads proportional, and labels offset from the line. Failure mode: crossing lines, unlabeled bidirectional arrows, or arrowheads larger than nodes.
## Typographic craft
### One family, many roles
- Use one capable family such as Inter, Geist, IBM Plex Sans, or Source Sans 3 with 400, 600, and 700 weights.
- Add mono only for code, identifiers, and aligned data.
- This is the safest option for dense interfaces and dashboards. Failure mode: synthetic italics or unavailable weights cause inconsistent rendering.
### Geometric display plus humanist body
- Use a geometric or neo-grotesk face for short display text and a humanist sans for reading.
- Example: Geist for headings and Source Sans 3 for body.
- Keep x-height and overall width compatible. Failure mode: combining two similar sans faces without a clear role difference.
### Serif display plus neutral sans
- Use Instrument Serif, Fraunces, or Playfair Display for large editorial headlines.
- Pair with Inter, IBM Plex Sans, or Source Sans 3 for body and labels.
- Keep the serif mostly above 32px; verify small-size legibility before extending it. Failure mode: ornate display serif in tables, navigation, or tiny chart labels.
### Monospace for data
- Use JetBrains Mono or IBM Plex Mono for code, timestamps, IDs, and selected numeric readouts.
- Enable tabular numerals; do not set long prose in mono.
- Limit mono to roughly 10-20% of the typography. Failure mode: mono everywhere produces developer-tool cosplay rather than clarity.
### Type scales
- Use 1.2 minor third for dense UI: 12, 14, 17, 20, 24, 29, 35.
- Use 1.25 major third for general artifacts: 12, 15, 19, 24, 30, 38, 48, 60.
- Use 1.333 perfect fourth for editorial and slides: 14, 19, 25, 34, 45, 60, 80.
- Round values intentionally for the medium; preserve visible ratios, not mathematical purity.
### Tracking
- Tighten display text above 32px by `-0.01em` to `-0.03em`.
- Leave body near the font default.
- Loosen small uppercase labels by `0.05em` to `0.1em`. Failure mode: negative tracking on small text closes counters and harms scanning.
### Line-height
- Use 1.45-1.65 for 14-18px body text.
- Use 1.25-1.4 for 20-30px headings.
- Use 0.95-1.1 for display text above 40px.
- Adjust multiline all-caps labels separately; their apparent leading differs.
### Measure
- Keep continuous prose near 60-75 characters per line.
- Use 45-60 characters for slide copy and sidebars.
- Allow code and dense tables to exceed this only when horizontal structure matters. Failure mode: full-width paragraphs on a wide canvas make readers lose their place.
### Numerals
- Use lining numerals in headings and metrics.
- Use tabular numerals in tables, scorecards, timers, and changing counters.
- Align decimals when precision matters; otherwise right-align numeric columns.
```css
.metric,
td.numeric {
  font-variant-numeric: lining-nums tabular-nums;
}
```
### Hanging punctuation
- Let opening quotation marks hang slightly outside the text column in editorial layouts.
- Use a negative text indent such as `text-indent: -0.35em` only for known quote marks. Failure mode: applying hanging punctuation to arbitrary paragraphs shifts their alignment.
### Widows, orphans, and wrapping
- Reword or resize to avoid one-word final lines in prominent headings.
- Use `text-wrap: balance` for headings and `text-wrap: pretty` for body where supported.
- Control print breaks with `orphans`, `widows`, and `break-inside`.
```css
h1, h2, h3 { text-wrap: balance; }
p { text-wrap: pretty; }
@media print {
  p { orphans: 3; widows: 3; }
  figure, table { break-inside: avoid; }
}
```
## Color systems
### Role-based tokens
- Name colors by function: `surface-base`, `surface-raised`, `text-primary`, `border-subtle`, `accent`, `danger`.
- Keep component code ignorant of literal color names.
- Define hover, active, disabled, and focus roles at the system level. Failure mode: `blue-500` used for both links and status creates accidental coupling.
### Hue-cast neutrals
- Build grays with a slight warm, cool, or brand-adjacent cast.
- Warm light ramp example: `#FAFAF9`, `#F5F5F2`, `#E7E5E1`, `#A8A29E`, `#57534E`, `#1C1917`.
- Cool dark ramp example: `#090B10`, `#10131A`, `#181C25`, `#303746`, `#8791A5`, `#E8ECF4`. Failure mode: mixing warm backgrounds with blue-gray borders and neutral-black text without intent.
### Near-black and near-white
- Prefer `#0A0A0B` or `#111113` over pure black for large dark surfaces.
- Prefer `#FAFAF9` or `#FCFCFB` over pure white for report backgrounds.
- Keep pure white for small highlights and pure black for rare maximum-contrast marks. Failure mode: absolute black and white across large areas look harsh and reveal default styling.
### Tinted shadows
- Tint shadow RGB values toward the surface hue.
- On warm paper, use `rgba(72,58,42,.12)` rather than neutral black.
- On cool dark UI, use `rgba(0,4,16,.36)`. Failure mode: colorful shadows become visible effects instead of depth cues.
### Harmonized semantic colors
- Keep success, warning, danger, and info near a shared chroma level.
- Pair each with a pale background and deep text tone, not one saturated fill.
- Verify text and icon contrast in every state; do not rely on hue alone. Failure mode: traffic-light primaries clash with a muted artifact.
### Dark mode is a separate composition
- Raise dark surfaces with lighter fills and borders, not merely inverted shadows.
- Reduce large-area accent saturation; increase text value contrast carefully.
- Re-evaluate imagery, charts, focus rings, and disabled states independently. Failure mode: automated inversion produces glowing colors and muddy media.
### Accessible accent selection
- Choose separate accent values for text, fills, and subtle backgrounds.
- A bright accent that works as a button fill may fail as text on white.
- Add underline, icon, shape, or label to semantic states; never encode status by color alone.
- Verify with the actual font size, weight, and background.
### OKLCH ramps
- Use OKLCH to adjust lightness while keeping hue and perceived chroma more consistent.
- Reduce chroma at both very light and very dark ends to avoid neon edges.
- Convert and test in target browsers or export tooling.
```css
:root {
--accent-50: oklch(97% 0.025 255); --accent-200: oklch(88% 0.075 255); --accent-500: oklch(62% 0.18 255);
--accent-700: oklch(46% 0.14 255);
}
```
## Layout and composition
### Twelve-column grid
- Use 12 columns for responsive product pages and dashboards because halves, thirds, and quarters divide cleanly.
- Start with 24px gutters and a 1200-1320px max width on desktop.
- Collapse intentionally to six, four, or one column; do not merely squeeze twelve columns. Failure mode: all cards span equal column counts and create monotonous tiling.
### Asymmetric split
- Use 7/5, 8/4, or 5/3 proportions for narrative plus evidence.
- Give the larger region to the content with greater visual complexity, not automatically to text.
- Align the split to the wider grid. Failure mode: a 50/50 split when one side has far less content leaves accidental emptiness.
### Thirds and golden placement
- Position the key object near a thirds intersection for a stable but active composition.
- Use roughly 62/38 when a dominant and supporting region need stronger contrast.
- Treat these as starting points, then adjust for content mass. Failure mode: forcing every layout into a formula regardless of text length or image shape.
### Content max widths
- Dense application shell: 1200-1440px.
- Marketing or mixed content page: 1120-1280px.
- Report body: 720-880px.
- Long-form text column: 600-760px.
- Slide safe content: roughly 84-90% of canvas width.
### Deliberate grid break
- Let one image, metric, or quote cross a column boundary or bleed to the edge.
- Keep its anchor aligned to at least one established grid line.
- Use one major grid break per view. Failure mode: several misaligned elements look accidental rather than expressive.
### Alignment
- Align text baselines, card edges, chart plot areas, and table columns before adding decoration.
- Prefer a small number of strong vertical axes.
- Make exceptions visible and intentional. Failure mode: centered labels inside left-aligned cards produce small but cumulative disorder.
### Bento grids without monotony
- Vary spans by information importance: one 2x2 anchor, several 1x1 supports, one wide narrative card.
- Keep shared internal padding and baseline alignment.
- Remove cards that contain only a title and one short sentence. Failure mode: a dashboard made entirely of equal rounded rectangles.
### Full-bleed and contained alternation
- Alternate contained reading sections with one full-bleed image, color band, or chart.
- Use the bleed to mark a chapter or emotional shift.
- Return to the same contained grid afterward. Failure mode: every section uses a different width and the artifact loses continuity.
### Sticky and anchored elements
- Keep a table header, chapter index, or current-stage marker visible when it reduces navigation cost.
- Offset sticky elements for existing app chrome and give them an opaque or blurred backing.
- Avoid sticky panels that consume more than roughly one-third of a short viewport. Failure mode: multiple sticky regions trap the content in a narrow slot.
## Data and charts
### Remove chartjunk
- Remove 3D effects, heavy frames, decorative gradients, redundant labels, and unnecessary gridlines.
- Keep only marks required to read the comparison or trend.
- Preserve units, source, time range, and uncertainty where relevant. Failure mode: subtraction that removes context needed to interpret the claim.
### Direct labeling
- Label series at the line end, bar end, or nearest open space.
- Match label color to the series and include the final value when useful.
- Use a legend only when direct labels would collide or repeat excessively. Failure mode: labels crossing lines or depending on color alone.
### Sorted bars
- Sort bars by value for ranking, or by a meaningful domain order such as time or process stage.
- Highlight the focal bar and mute the rest.
- Keep labels horizontal when possible. Failure mode: alphabetical order hides the story unless lookup is the task.
### Honest axes
- Start bar charts at zero because length encodes magnitude.
- Line charts may use a bounded range when the range is explicit and the change is the subject.
- Label breaks and reference baselines visibly. Failure mode: truncated bars exaggerate small differences.
### Muted gridlines
- Use zero to four gridlines at low contrast, typically 6-12% black on light or 8-14% white on dark.
- Remove vertical gridlines unless they support time lookup.
- Keep the baseline slightly stronger if it matters. Failure mode: gridlines darker than the data marks.
### Sequential ramps
- Use one hue from pale to dark for ordered magnitude.
- Keep adjacent steps distinguishable and reserve the darkest tone for the highest value or focal class.
- Add numeric labels when exact comparison matters. Failure mode: rainbow ramps imply categories and create false boundaries.
### Highlight one series
- Render contextual series in muted gray or low-alpha color and one focal series in accent.
- Increase focal line width from 1.5px to 2.5-3px.
- Label the reason for emphasis. Failure mode: every series receives a saturated categorical color.
### Annotation layer
- Add one to three callouts that explain the insight, inflection, outlier, or policy threshold.
- Connect with a light leader line and place the annotation outside dense marks.
- State what happened, not merely the value. Failure mode: annotations repeat every data label and cover the plot.
### Number formatting
- Use thousands separators and consistent precision within a comparison.
- Put shared units in the title or column header once: `Revenue ($M)`.
- Use compact notation only when it improves scanning and does not hide meaningful differences. Failure mode: mixed `$1.2M`, `$950,000`, and `1,100k` in one view.
### Sparklines
- Use 40-120px sparklines beside a current value to show recent direction.
- Omit axes but keep a shared scale when comparing rows.
- Mark exceptional points or the latest point only. Failure mode: each sparkline uses its own scale and invites false comparison.
### Small multiples
- Repeat the same chart frame for categories, regions, or scenarios.
- Lock scales and ordering across panels.
- Use a shared annotation or highlight rule. Failure mode: changing scales or encodings between panels defeats comparison.
### Table craft
- Left-align text; right-align numbers; align decimals when precision matters.
- Use tabular figures, 12-16px cell padding, and subtle row rules.
- Prefer grouped bands or section rules over zebra striping.
- Make headers sticky in long interactive tables and repeat them in print. Failure mode: centered numbers, heavy cell boxes, and unformatted raw values.
## Motion and interaction for HTML
### Easing
- Use `cubic-bezier(.16,1,.3,1)` for confident entrances and deceleration.
- Use standard ease-out for small state changes.
- Avoid spring effects unless physical playfulness is central to the artifact.
### Duration
- Use 120-240ms for controls, hover, and panel changes.
- Use 300-600ms for narrative entrances and chart reveals.
- Keep related elements within one temporal phrase. Failure mode: 800ms UI transitions make the interface feel slow.
### Stagger
- Stagger related items by 30-70ms.
- Cap the total sequence near 500-700ms for a normal viewport.
- Reveal in reading or causal order. Failure mode: long card-by-card cascades punish repeat viewing.
### Transform and opacity
- Animate `transform` and `opacity` for smooth compositor-friendly motion.
- Use 8-24px translation or a subtle 0.98-to-1 scale.
- Keep layout-affecting properties static during routine interaction.
```css
.reveal {
  opacity: 0;
  transform: translateY(16px);
  animation: enter 480ms cubic-bezier(.16, 1, .3, 1) forwards;
}
@keyframes enter {
  to { opacity: 1; transform: translateY(0); }
}
```
### Hover with more than color
- Combine a small border, shadow, underline, icon, or 1-2px lift with a color change.
- Keep hover movement subtle enough that neighboring layout does not shift.
- Provide equivalent focus and active states. Failure mode: hover-only information is unavailable to touch and keyboard users.
### Focus-visible
- Use a 2-3px focus ring offset by 2px.
- Choose a ring color that remains visible on both base and raised surfaces.
- Never remove the browser outline without a tested replacement.
```css
:focus-visible {
  outline: 3px solid #4f7cff;
  outline-offset: 2px;
}
```
### Reduced motion
- Remove nonessential animation under `prefers-reduced-motion`.
- Preserve final state, hierarchy, and all information.
- Shorten necessary state transitions rather than hiding feedback.
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: 1ms !important;
  }
}
```
## Medium-specific moves
### Slides
- Use a full-bleed statement slide for a chapter shift: one claim, one image or number, no supporting grid.
- Keep one governing idea per slide; move evidence into the next slide rather than shrinking everything.
- Use consistent safe margins around 5-8% of slide width.
- Replace default bullets with a sequence, comparison, diagram, or labeled stack.
- Build in causal or reading order and finish on a complete static frame. Failure mode: every slide uses the same title-plus-three-cards template.
### Spreadsheets
- Freeze the header row and the first identifier column when either scrolls out of view.
- Use a restrained header band, clear filter state, and consistent number formats by column.
- Band semantic groups with spacing, rules, or low-chroma fills instead of alternating every row.
- Use data bars for magnitude, color scales for continuous intensity, and icon sets only for truly discrete states.
- Hide helper columns used by formulas or charts, but label and document them in the workbook structure.
- Use named ranges for important assumptions and print areas for intended output pages.
- Example status formula: `=IF([@Variance]>0.1,"Review",IF([@Variance]<-0.1,"Below","On plan"))`. Failure mode: conditional formatting turns every cell red, amber, or green with no neutral state.
### PDF and print
- Set a baseline grid and align body copy, captions, and sidenotes where practical.
- Use inside margins 6-12mm larger than outside margins for bound documents.
- Define running heads, page numbers, and chapter openings consistently.
- Keep critical colors CMYK-safe or test the actual export profile.
- Avoid hairlines below the output device's reliable minimum; 0.5pt is safer than ultra-thin screen rules.
- Control page breaks for headings, figures, tables, widows, and orphans. Failure mode: screen-perfect pale gray text disappears in office printing.
### Email
- Use a table layout, inline styles, and a main width near 600px.
- Use system and web-safe fallbacks; treat custom fonts as optional enhancement.
- Keep buttons at least 44px high and provide visible linked text.
- Test without background images and with images blocked. Failure mode: relying on CSS grid, external stylesheets, or hover to communicate required content.
## Texture and finish
### Noise and grain
- Add monochrome noise at 2-4% opacity over large flat backgrounds.
- Use a small repeated raster or SVG turbulence with `pointer-events: none`.
- Keep text and charts above the texture. Failure mode: visible grain over body copy reduces legibility and export quality.
### Gradient meshes
- Place soft mesh gradients behind content as atmosphere, not inside text.
- Use two to four low-chroma color fields and large blur radii.
- Preserve a calm, high-contrast reading area. Failure mode: saturated blobs become the artifact's subject.
### Duotone imagery
- Convert inconsistent imagery into a shared dark/light pair.
- Preserve facial detail and subject recognition; test midtone separation.
- Use the accent as one duotone endpoint only when it does not overpower text. Failure mode: applying duotone to charts, diagrams, or screenshots that need literal color.
### Masked and clipped shapes
- Crop imagery into a purposeful circle, arch, angled panel, or oversized type mask.
- Keep the crop aligned to the composition and preserve the subject's focal point. Failure mode: several unrelated mask shapes create scrapbook styling.
### Dot and line grids
- Use 1px dots or lines at 4-8% opacity with 16-32px spacing.
- Fade the pattern near text or behind raised surfaces.
- Use it to imply technical space, coordinates, or construction. Failure mode: high-contrast grids cause moire and compete with data.
### Border gradients
- Use a gradient border on one focal panel or interactive object.
- Keep the interior solid and the border near 1px.
- Prefer subtle luminance variation over a rainbow spectrum. Failure mode: gradient borders on every card recreate generic AI dashboard styling.
## Anti-patterns
- Uniform drop shadows on every surface: depth loses meaning and the page looks assembled from presets.
- Gradient text everywhere: reserve it, if used at all, for one short display phrase with a solid-color fallback.
- Glassmorphism on every surface: blur and transparency should indicate overlay or layering, not decorate ordinary cards.
- Emoji as iconography: use a coherent icon set, simple SVG marks, or text labels.
- Default chart palettes: choose an encoding that matches order, category, emphasis, and accessibility needs.
- Centered everything: center short statements deliberately; left-align reading, controls, tables, and most data labels.
- Three or more font families: use one family with roles, or one display family plus one workhorse family.
- Rainbow categorical colors: reduce categories, group related items, and highlight the series that matters.
- The same 8px radius everywhere: vary by scale and role, including square edges where precision helps.
- Unstyled tables: align by data type, format values, reduce rules, and make grouping visible.
- Purple-blue gradient hero: use it only when the content and chosen visual direction genuinely require it, not as the default signal for technology.
- Excessive radius on images: preserve edge-to-edge photography, diagrams, and screenshots when clipping adds no meaning.
- Card grids as the answer to every layout: use spacing, rules, columns, and full-bleed regions before adding another container.
- Decorative icons beside every heading: icons should identify, navigate, or encode state, not fill empty space.
- Low-contrast gray body text: muted does not mean barely visible; verify required text in its final context.
- Tiny labels around oversized empty cards: increase information density or remove the card.
- Repeated badges and pills: use pills for compact state, filter, or token semantics, not ordinary labels.
- Mixed corner languages: align radii, border thickness, icon stroke, and surface treatment to one coherent system.
- Arbitrary gradients behind charts: keep the plotting area quiet so data remains dominant.
- Fake metrics and decorative charts: show real data with provenance or use a clearly labeled structural placeholder during authoring only.
