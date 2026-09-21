# Design reference library
Consult this file when choosing one governing visual direction, translating a recognized design tradition into current artifacts, or starting from a complete token system.
## How to use this library
- Pick one governing reference for the artifact.
- Borrow its logic: hierarchy, density, spacing, contrast, geometry, image treatment, and editing discipline.
- Add at most one secondary influence for a specific need, such as editorial typography inside a technical-neutral system.
- Do not blend several recognizable styles into a mood board rendered all at once.
- Do not copy a company's identity, proprietary assets, logos, illustrations, product screenshots, or trademarked visual signatures.
- Do not claim that an observable pattern is an internal company rule.
- Translate the reference into original tokens suited to the content, audience, medium, and accessibility requirements.
- Verify fonts, color contrast, print behavior, and motion in the actual output.
## Contemporary product design references
### Stripe
**Observable pattern**
- Stripe's public marketing and documentation surfaces read as documentation-grade clarity with controlled visual richness.
- Near-neutral backgrounds carry dense technical information without feeling utilitarian.
- Accent colors appear in selective diagrams, key actions, and occasional atmospheric gradients.
- Vertical space changes with semantic importance: compact reference material, generous chapter openings.
**What makes it work**
- Dense content is not treated as a reason to reduce hierarchy.
- Headings, body, code, diagrams, notes, and actions each have a distinct typographic and spatial role.
- The gradient is a signature event rather than a universal fill.
- Fine rules, restrained shadows, and precise alignment create finish without excess decoration.
**What to borrow**
- Use a near-white base, dark ink, one cool accent, and a warm or violet secondary tint.
- Pair a readable sans with a restrained mono for technical detail.
- Use 64-96px vertical gaps for major chapters and 24-40px within documentation sections.
- Put code or data examples in slightly tinted, bordered surfaces rather than heavy cards.
- Use one major gradient or color field to establish identity, then return to neutral surfaces.
**What not to copy**
- Do not reproduce Stripe's logo, proprietary illustrations, exact gradient, diagram vocabulary, or page composition.
- Do not add multicolor gradients to an artifact merely to make it feel "fintech."
- Do not mistake high polish for high saturation.
**Starting tokens**
```css
--surface: #f7f8fa; --surface-raised: #ffffff; --ink: #202124;
--muted: #5f6673; --border: #dfe3e8; --accent: #4f63d9;
--accent-soft: #e9ecff; --code-bg: #f1f3f7; --radius-sm: 6px;
--radius-md: 10px; --space-section: 80px;
```
### Linear
**Observable pattern**
- Linear's public product surfaces read as dark-first, fast, precise, and tightly controlled.
- Contrast changes are small but deliberate across base, raised, selected, and overlay surfaces.
- Hairline borders and compact rows support high information density.
- Motion suggests speed through short, restrained transitions rather than theatrical animation.
- The palette is largely monochrome with one cool accent.
**What makes it work**
- Surface steps are close enough to feel integrated but distinct enough to navigate.
- Typography remains quiet; state, alignment, and rhythm carry much of the hierarchy.
- The interface edits aggressively: most elements have one clear role.
- Micro-motion reinforces continuity when panels, filters, or states change.
**What to borrow**
- Start with `#0B0C0E`, `#121418`, and `#191C21` as base elevation steps.
- Use 1px white-alpha borders near 7-10%.
- Keep body text near 14px with 20px line-height for dense application views.
- Use one cool accent such as `#7C8CFF`; mute contextual data to blue-gray.
- Use 140-220ms transitions and `cubic-bezier(.16,1,.3,1)`.
**What not to copy**
- Do not reproduce product-specific navigation, issue icons, naming, or interaction patterns.
- Do not darken an artifact that will mostly be printed or projected in bright rooms.
- Do not compress content unless the audience benefits from expert-level density.
**Starting tokens**
```css
--surface-base: #0b0c0e; --surface-raised: #121418; --surface-overlay: #191c21;
--text-primary: rgba(255, 255, 255, 0.92); --text-secondary: rgba(255, 255, 255, 0.66); --text-tertiary: rgba(255, 255, 255, 0.42);
--border: rgba(255, 255, 255, 0.08); --accent: #7c8cff; --radius: 8px;
```
### Apple
**Observable pattern**
- Apple's public product pages often use enormous type-size contrast, centered editorial composition, product imagery as the hero, deep whitespace, and very few colors.
- Sections make one claim at a time and allow the image or demonstration to carry the explanation.
- Supporting copy is usually short relative to the scale of the composition.
**What makes it work**
- Extreme reduction gives each claim and image room to feel important.
- Type scale, whitespace, and image quality do more work than containers or ornament.
- Centering is used for narrative statements, not indiscriminately for utility content.
- Color often comes from the product image rather than surrounding chrome.
**What to borrow**
- Use 64-112px display type on a large canvas when the statement is genuinely singular.
- Limit a hero section to one heading, one support sentence, and one dominant visual.
- Use 96-160px vertical gaps between major story beats.
- Keep the background neutral and let the subject provide chroma.
- Alternate centered statement sections with left-aligned evidence sections.
**What not to copy**
- Do not reproduce product photography, launch-page sequences, proprietary type, or hardware silhouettes.
- Do not use giant type to inflate a weak claim.
- Do not center tables, dashboards, or long report sections.
**Starting tokens**
```css
--surface: #f5f5f7; --ink: #1d1d1f; --muted: #6e6e73;
--link: #0066cc; --display-size: clamp(3.5rem, 8vw, 7rem); --display-leading: 0.98;
--content-wide: 1200px; --copy-measure: 44rem;
```
### Vercel and Geist
**Observable pattern**
- Vercel's public surfaces read as near-monochrome, geometrically precise, and technically direct.
- Mono type frequently marks code, system state, or small technical labels.
- Grids, rules, dots, and black-white contrast create structure.
- The overall editing principle is ruthless subtraction.
**What makes it work**
- Geometry and alignment substitute for decorative color.
- Small technical details are clearly differentiated without becoming visual clutter.
- Empty space and hard edges make the remaining elements feel intentional.
- One strong black or white region can anchor an otherwise quiet page.
**What to borrow**
- Use near-white `#FAFAFA`, near-black `#0A0A0A`, and gray steps around `#EAEAEA`, `#A1A1AA`, and `#52525B`.
- Use 1px rules and a 24-32px structural grid.
- Pair Geist, Inter, or system sans with Geist Mono, JetBrains Mono, or IBM Plex Mono.
- Use square or 6-8px corners for technical surfaces.
- Delete decorative labels, redundant borders, and unneeded color.
**What not to copy**
- Do not reproduce the triangle mark, product cards, deployment vocabulary, or exact black-white brand composition.
- Do not use mono for body copy.
- Do not confuse monochrome with absence of hierarchy.
**Starting tokens**
```css
--surface: #fafafa; --surface-raised: #ffffff; --ink: #0a0a0a;
--muted: #52525b; --faint: #a1a1aa; --border: #e4e4e7;
--accent: #2563eb; --radius: 6px; --grid-unit: 24px;
```
### Notion and Craft
**Observable pattern**
- Notion and Craft public-facing document surfaces read as warm-neutral, text-first, and editorial.
- Content blocks feel direct and approachable rather than heavily framed.
- Accents are low-chroma and illustrations or icons tend to support navigation and tone.
- Spacing and writing structure carry more hierarchy than surface elevation.
**What makes it work**
- The page behaves like a document before it behaves like an application.
- Warm backgrounds and dark-brown or charcoal ink reduce clinical harshness.
- Headings, lists, callouts, and tables share one readable text system.
- Containers are used selectively for callouts or embedded objects.
**What to borrow**
- Use a warm paper base such as `#FBFAF7` and ink near `#2F2B27`.
- Keep long-form measure around 640-760px.
- Use 1.55-1.7 body line-height and 24-32px paragraph rhythm.
- Use pale olive, clay, blue-gray, or ochre for callout backgrounds.
- Favor rules, indentation, and whitespace over card grids.
**What not to copy**
- Do not reproduce block controls, page icons, slash-command affordances, or proprietary illustration styles.
- Do not use emoji as the artifact's icon system.
- Do not make every paragraph a movable-looking block.
**Starting tokens**
```css
--paper: #fbfaf7; --paper-raised: #ffffff; --ink: #2f2b27;
--muted: #756e66; --border: #e7e1d8; --accent: #64748b;
--callout: #f1eee7; --radius: 8px; --measure: 44rem;
```
### Observable, Datawrapper, FT, and Economist graphics
**Observable pattern**
- These public data-visualization references foreground the question and annotation rather than decorative chart form.
- Charts use restrained palettes, direct labels, concise source notes, and visible uncertainty where relevant.
- A single emphasized series or interval often carries the story.
- Small multiples and compact tables are treated as first-class explanatory graphics.
**What makes it work**
- The chart title states the insight or question, not merely the metric name.
- Marks are edited to the minimum needed for reliable reading.
- Annotation is integrated into the plot rather than appended as a separate paragraph.
- Color follows meaning: sequence, divergence, category, or focus.
**What to borrow**
- Write a claim-led title and a factual subtitle with units, period, and population.
- Use direct labels, muted gridlines, and one focal color.
- Put source and methodology below the visual at 10-12px.
- Sort categories by value unless chronology or domain order matters.
- Use small multiples when one overloaded chart requires too many legends or line styles.
**What not to copy**
- Do not copy publication-specific fonts, house red, illustration style, chart templates, or editorial identity.
- Do not borrow a palette without checking its role and accessibility in the new data.
- Do not turn a nuanced dataset into a single dramatic annotation unsupported by the evidence.
**Starting tokens**
```css
--chart-ink: #222222; --chart-muted: #6b7280; --chart-grid: #e5e7eb;
--chart-context: #b8bec8; --chart-focus: #b42318; --chart-positive: #2f6f5e;
--chart-bg: #fffdf8; --annotation-bg: rgba(255, 253, 248, 0.92);
```
## Classical and historical references
### Swiss and International Typographic Style
**Core pattern**
- Use a rational grid, asymmetric balance, flush-left ragged-right type, objective imagery, and hierarchy through size and space.
- The Akzidenz-Grotesk and Helvetica lineage favors neutral sans forms, but the governing idea is disciplined information order rather than one typeface.
**What to borrow today**
- Build a 6- or 12-column grid before placing content.
- Align headings, captions, images, and data to a small set of vertical axes.
- Use one sans family in decisive size and weight steps.
- Keep body copy left-aligned and let the right edge remain natural.
- Use one accent color for indexing or emphasis.
- Let asymmetry create energy while the grid creates control.
**When it works**
- Technical reports, systems diagrams, public-information graphics, decks, portfolios, and artifacts that need authority without decoration.
**Failure mode**
- A red square, Helvetica, and random asymmetry are costume, not Swiss design.
- Dense content still needs reading order; a grid alone does not create hierarchy.
### Bauhaus
**Core pattern**
- Use function-led form, geometric primitives, primary colors, bold sans display, diagonals, and visible construction.
- Treat typography, shape, and image as active compositional material.
**What to borrow today**
- Reduce a concept to circles, rectangles, lines, and one strong diagonal.
- Use red, yellow, and blue only as controlled signals against neutral ground.
- Let type become a structural shape in a title slide or chapter opener.
- Use asymmetric balance and cropped forms to create motion without animation.
**When it works**
- Cultural decks, concept presentations, creative coding, educational diagrams, and artifacts that benefit from visible experimentation.
**Failure mode**
- Do not scatter primary-colored circles as decoration.
- Do not imitate historical posters when the content requires quiet credibility.
- Keep the functional relationship between every shape and the message.
### Massimo Vignelli
**Core pattern**
- Work from a small canon of typefaces, a rigorous grid, consistent formats, and semantic rather than decorative color.
- The NYC subway map demonstrates color as a durable classification system, even when the visual system must simplify geography.
**What to borrow today**
- Limit typography to one or two families with a small number of weights.
- Define formats and grids once, then enforce them across the artifact.
- Assign color to categories or routes and keep that mapping stable.
- Prefer a strong system that can absorb new content over one-off page compositions.
- Remove choices that do not improve communication.
**Failure mode**
- A tiny typeface palette does not excuse poor typography.
- Semantic color fails when categories multiply beyond reliable recognition.
- Rigor should simplify authoring and reading, not make exceptions impossible.
### Dieter Rams translated for dashboards and decks
1. **Innovative:** Use new interaction or visual methods only when they improve the task, not to signal novelty.
2. **Useful:** Every panel, chart, and slide must answer a user or audience need.
3. **Aesthetic:** Resolve alignment, type, spacing, and proportion because usability depends on visual order.
4. **Understandable:** Make state, sequence, ownership, and action evident without explanation from the author.
5. **Unobtrusive:** Let content and decisions dominate; chrome should support them.
6. **Honest:** Do not exaggerate data, certainty, capability, or progress.
7. **Long-lasting:** Prefer durable layout logic and tokens over trend effects.
8. **Thorough:** Resolve loading, empty, error, print, mobile, focus, and reduced-motion states where relevant.
9. **Environmentally considerate:** Reduce unnecessary assets, animation, ink-heavy pages, and computationally expensive decoration.
10. **As little design as possible:** Remove what does not clarify meaning, action, or identity.
### Josef Muller-Brockmann and grid systems
**Module and gutter math**
- Choose the content width, column count, and gutter, then calculate the module rather than eyeballing it.
- Formula: `column width = (container width - gutter * (columns - 1)) / columns`.
- Example: a 1200px container with 12 columns and 24px gutters yields `(1200 - 264) / 12 = 78px` columns.
- Build vertical modules from a baseline such as 8px or a body line-height such as 24px.
- Align images and charts to full module spans whenever possible.
- Break the grid only when the exception carries meaning.
**Practical presets**
- Dashboard: 12 columns, 24px gutters, 1200-1440px container.
- Report: 6 columns, 24px gutters, 800-960px content field.
- Slide: 12 columns, 24-32px gutters, 5-8% safe margin.
- Mobile: 4 columns, 16px gutters, 16-24px outer margin.
**Failure mode**
- More columns do not automatically produce sophistication.
- A grid that cannot accommodate the actual table, chart, or paragraph length is the wrong grid.
### Edward Tufte
**Core principles**
- Increase the share of ink that represents data or necessary structure.
- Remove chartjunk that competes with quantitative relationships.
- Use small multiples to compare repeated structures.
- Use sparklines to place trend context near a value.
- Layer and separate information through weight, color, space, and annotation.
- Integrate words, numbers, and images rather than splitting explanation from evidence.
**What to borrow today**
- Place the annotation beside the data point it explains.
- Use thin rules, light grids, and direct labels.
- Show context and comparison, not isolated headline numbers.
- Keep sources, units, and relevant uncertainty visible.
- Prefer a compact evidence-rich view over a decorative oversized chart.
**Failure mode**
- Maximizing data-ink is not minimizing explanation.
- Removing axes, labels, or uncertainty can make a chart look clean while making it misleading.
- Dense information still requires hierarchy and legible typography.
### Editorial and print
**Borrowable patterns**
- Use pull quotes to interrupt long reading sequences with one sharp idea.
- Use a drop cap only at a true chapter opening and only when the text style supports it.
- Use horizontal rules to mark section shifts, footnotes, or changes in voice.
- Use sidenotes for references or definitions that should remain near the claim.
- Use two or three columns for short editorial pages, not long technical procedures.
- Use captions as a secondary narrative layer rather than labels such as "Figure 1" alone.
- Use running heads, folios, and repeated section markers for navigation in long documents.
**When to use brutalist-editorial**
- Use raw, typographic, high-contrast composition for manifestos, cultural programs, experimental portfolios, or a deliberately confrontational statement.
- Keep the underlying grid exact even when type is oversized, cropped, or colliding.
- Use black, off-white, and one hard accent; let type provide most of the visual energy.
- Retain readable body sections and accessible navigation.
**Failure mode**
- Random misalignment, illegible type, and unstyled browser defaults are not automatically brutalist.
- Do not use a confrontational visual voice for compliance reports, sensitive findings, or calm operational tools.
## Ready-to-use systems
### Technical Neutral
Use for documentation, product explainers, technical reports, admin interfaces, and dense dashboards that need light-mode clarity.
```css
:root {
--font-sans: Inter, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; --font-mono: "IBM Plex Mono", "Cascadia Code", Consolas, monospace; --type-xs: 12px;
--type-sm: 14px; --type-md: 16px; --type-lg: 20px;
--type-xl: 25px; --type-2xl: 32px; --type-3xl: 40px;
--type-4xl: 52px; --neutral-0: #ffffff; --neutral-50: #fafafa;
--neutral-100: #f4f4f5; --neutral-200: #e4e4e7; --neutral-300: #d4d4d8;
--neutral-500: #71717a; --neutral-700: #3f3f46; --neutral-900: #18181b;
--neutral-950: #09090b; --accent: #3457d5; --accent-soft: #e9edff;
--space: 4px 8px 12px 16px 24px 32px 48px 64px 96px; --radius-sm: 4px; --radius-md: 8px;
--radius-lg: 12px; --border: 1px solid rgba(24, 24, 27, 0.10); --shadow-1: 0 1px 2px rgba(24, 24, 27, 0.06);
--shadow-2: 0 12px 32px rgba(24, 24, 27, 0.10), 0 2px 8px rgba(24, 24, 27, 0.05);
}
```
### Signal Dark
Use for monitoring, operations, developer tools, and high-density dashboards viewed mainly on screen.
```css
:root {
--font-sans: Geist, Inter, "Segoe UI", Arial, sans-serif; --font-mono: "JetBrains Mono", "Cascadia Code", Consolas, monospace; --type-xs: 11px;
--type-sm: 13px; --type-md: 14px; --type-lg: 17px;
--type-xl: 21px; --type-2xl: 28px; --type-3xl: 36px;
--neutral-950: #08090b; --neutral-900: #0e1014; --neutral-850: #14171c;
--neutral-800: #1b1f26; --neutral-700: #2c323d; --neutral-500: #788296;
--neutral-300: #b7bfcc; --neutral-100: #edf0f5; --accent: #7c8cff;
--accent-soft: rgba(124, 140, 255, 0.16); --success: #5fcf9a; --warning: #e2b45b;
--danger: #ef7b7b; --space: 4px 8px 12px 16px 20px 24px 32px 48px 64px; --radius-sm: 4px;
--radius-md: 7px; --radius-lg: 10px; --border: 1px solid rgba(255, 255, 255, 0.08);
--shadow-1: inset 0 1px 0 rgba(255, 255, 255, 0.05), 0 2px 8px rgba(0, 4, 16, 0.28); --shadow-2: inset 0 1px 0 rgba(255, 255, 255, 0.06), 0 20px 48px rgba(0, 4, 16, 0.42);
}
```
### Editorial Statement
Use for presentations, launch narratives, annual-report openings, essays, and visual reports where a few claims deserve dramatic scale.
```css
:root {
--font-display: "Instrument Serif", "Iowan Old Style", "Palatino Linotype", Georgia, serif; --font-body: "Source Sans 3", "Segoe UI", Arial, sans-serif; --font-mono: "IBM Plex Mono", Consolas, monospace;
--type-xs: 12px; --type-sm: 14px; --type-md: 18px;
--type-lg: 24px; --type-xl: 34px; --type-2xl: 46px;
--type-3xl: 62px; --type-4xl: 84px; --paper: #f7f3ec;
--paper-deep: #eee7dc; --ink: #211f1c; --muted: #6f675d;
--rule: #cfc5b6; --accent: #9f2f24; --accent-soft: #ead7d2;
--secondary: #315b56; --space: 4px 8px 16px 24px 32px 48px 72px 96px 144px; --radius-sm: 2px;
--radius-md: 6px; --border: 1px solid rgba(60, 48, 35, 0.18); --shadow-1: 0 2px 8px rgba(72, 58, 42, 0.08);
--shadow-2: 0 24px 64px rgba(72, 58, 42, 0.14);
}
```
### Swiss Grid
Use for structured decks, public-information graphics, architecture overviews, portfolios, and systems that need objective clarity with one decisive accent.
```css
:root {
--font-sans: Helvetica, Arial, "Nimbus Sans L", sans-serif; --font-mono: "IBM Plex Mono", "Courier New", monospace; --type-xs: 11px;
--type-sm: 14px; --type-md: 17px; --type-lg: 23px;
--type-xl: 31px; --type-2xl: 42px; --type-3xl: 56px;
--type-4xl: 75px; --white: #f7f7f5; --gray-100: #e8e8e5;
--gray-300: #b9b9b4; --gray-600: #646460; --black: #11110f;
--accent: #d7261e; --space: 4px 8px 12px 16px 24px 32px 48px 64px 96px 128px; --radius: 0;
--border: 1px solid #11110f; --shadow-1: none; --shadow-2: none;
--columns: 12; --gutter: 24px;
}
```
### Warm Document
Use for policies, research reports, printable PDFs, proposals, and long-form material that should feel considered and humane.
```css
:root {
--font-display: Charter, "Bitstream Charter", "Iowan Old Style", Georgia, serif; --font-body: "Source Sans 3", "Segoe UI", Arial, sans-serif; --font-mono: "IBM Plex Mono", Consolas, monospace;
--type-xs: 10px; --type-sm: 12px; --type-md: 16px;
--type-lg: 20px; --type-xl: 25px; --type-2xl: 32px;
--type-3xl: 41px; --paper: #fbf8f1; --paper-raised: #fffdf8;
--paper-deep: #f0eadf; --ink: #29251f; --muted: #6d655a;
--rule: #d8cfc1; --accent: #2f665c; --accent-soft: #dfeae5;
--note: #eee4cf; --space: 4px 8px 12px 16px 24px 32px 48px 64px 96px; --radius-sm: 2px;
--radius-md: 5px; --border: 1px solid #d8cfc1; --shadow-1: 0 1px 3px rgba(70, 55, 38, 0.06);
--shadow-2: 0 16px 36px rgba(70, 55, 38, 0.10);
}
```
## Type pairing shortlist
### Inter plus JetBrains Mono
- Use for product UI, technical dashboards, and dense documentation.
- Inter handles labels and prose; JetBrains Mono handles code, IDs, and numeric detail.
- Keep mono smaller or equal in optical size; its wide characters consume space quickly.
### Geist plus Geist Mono
- Use for near-monochrome technical pages, developer tools, and modern system diagrams.
- The shared construction creates consistency without removing role distinction.
- Avoid using mono for navigation or paragraphs.
### IBM Plex Sans plus IBM Plex Mono
- Use for enterprise, research, technical manuals, and data-heavy reports.
- The family supports a serious, engineered tone and broad typographic coverage.
- Use Plex Sans 400/600 and Plex Mono 400/500; avoid too many intermediate weights.
### Source Sans 3 plus Source Serif 4
- Use for reports, policy documents, research summaries, and editorial dashboards.
- Source Sans supports UI and annotation; Source Serif carries longer reading.
- Match size optically rather than using identical pixel sizes by default.
### Instrument Serif plus Inter
- Use for statement decks, launch narratives, and report chapter openings.
- Instrument Serif supplies expressive large headlines; Inter stabilizes all functional text.
- Keep the serif above roughly 32px unless careful testing proves smaller use.
### Fraunces plus Source Sans 3
- Use for culture, sustainability, education, food, and human-centered storytelling.
- Fraunces can feel warm and distinctive; Source Sans keeps body content plain.
- Use restrained optical and weight settings; too many variable-axis effects become theatrical.
### Playfair Display plus IBM Plex Sans
- Use for formal editorial covers, historical topics, and high-contrast presentations.
- Playfair provides strong display contrast; Plex Sans keeps supporting information contemporary.
- Do not set chart labels, captions, or dense tables in Playfair.
### Charter plus Source Sans 3
- Use for long-form PDFs, proposals, and printable reports.
- Charter remains readable in print; Source Sans handles headings, metadata, and tables.
- Test the exact export environment because available Charter variants differ.
## Color palette starting points
These are starting systems, not guaranteed accessibility results. Verify each foreground-background pair at its actual size, weight, and state.
### Cool technical
- Base: `#F7F8FA`
- Raised: `#FFFFFF`
- Ink: `#1B1E24`
- Muted: `#5F6673`
- Border: `#DDE2E8`
- Accent: `#3457D5`
- Accent soft: `#E7ECFF`
- Success: `#287A5B`
- Warning: `#9A6518`
- Danger: `#B33A3A`
- Use for documentation, SaaS surfaces, diagrams, and technical reports.
### Signal dark
- Base: `#090B0F`
- Raised: `#11141A`
- Overlay: `#191E27`
- Ink: `#EEF1F6`
- Muted: `#929CAD`
- Border: `#2A303B`
- Accent: `#7C8CFF`
- Accent soft: `#232A50`
- Success: `#62C99A`
- Warning: `#D8AA58`
- Danger: `#E67979`
- Use for monitoring and operational interfaces; verify muted text carefully.
### Warm editorial
- Paper: `#F8F3EA`
- Raised: `#FFFDF8`
- Ink: `#241F1A`
- Muted: `#6F655B`
- Rule: `#D7CCBD`
- Accent: `#A13A2E`
- Accent soft: `#EEDAD4`
- Secondary: `#38665E`
- Note: `#EFE4CE`
- Use for reports, essays, and narrative presentations.
### Swiss achromatic plus red
- Base: `#F6F6F3`
- Ink: `#11110F`
- Mid: `#6A6A66`
- Light: `#D9D9D4`
- Accent: `#D7261E`
- Accent dark: `#9F1C16`
- Use for strict grid systems and information graphics.
- Keep red scarce; it loses authority when it fills large areas.
### Low-chroma natural
- Base: `#F4F2EA`
- Raised: `#FCFBF7`
- Ink: `#2B302A`
- Muted: `#687066`
- Border: `#D8D9CF`
- Moss: `#65775A`
- Clay: `#A45F4B`
- Ochre: `#A67A2F`
- Mist: `#DCE4DF`
- Use for sustainability, research, education, and human-centered topics.
### Data focus
- Plot background: `#FFFDF8`
- Ink: `#242424`
- Grid: `#E5E1D9`
- Context series: `#B6BBC3`
- Focus blue: `#2864B7`
- Focus red: `#B43B35`
- Positive green: `#2F765F`
- Caution ochre: `#A36B16`
- Use one focus color per chart and reserve the others for true semantic distinctions.
### Muted categorical set
- Blue: `#4C78A8`
- Orange: `#D78740`
- Green: `#5C8D6A`
- Red: `#B65A5A`
- Violet: `#8172A8`
- Teal: `#4F8C8D`
- Gold: `#B09143`
- Gray: `#7A7F87`
- Use only when categories are genuinely peers and direct labeling is present.
- Reduce the number of active colors before adding more categories.
## Further principles
- "Less, but better." Dieter Rams. Remove until the artifact becomes clearer, not merely emptier.
- "The grid is an aid, not a guarantee." Use it to create order, then judge the composition.
- "Form follows function." Commonly associated with Louis Sullivan. Let purpose determine visual structure.
- "The medium is the message." Marshall McLuhan. Treat slide, browser, spreadsheet, print, and email constraints as design inputs.
- "Make it as simple as possible, but not simpler." Commonly attributed to Albert Einstein; use the idea cautiously, not as a provenance claim.
- Hierarchy should survive grayscale.
- Alignment is the cheapest quality signal.
- Space is a relationship, not leftover area.
- One strong exception proves the system; many exceptions reveal that there is no system.
- If everything is emphasized, nothing is emphasized.
- Use color to encode, focus, or identify; do not use it merely to occupy area.
- Typography is interface, not decoration.
- Large type demands stronger editing, not more words.
- Dense information needs stronger structure, not automatically more whitespace.
- A chart title should tell the reader what to look for.
- Annotation should state why a mark matters, not repeat its value.
- A card is a container of last resort when spacing and alignment can express the group.
- Motion should explain change, preserve context, or confirm action.
- A dark theme is recomposed, not inverted.
- Accessibility is a property of the final combination, not a token in isolation.
- A reference is successful when the output feels governed by a clear logic without looking like a copy.
