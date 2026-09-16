# Authoring and release checklist

## Contract and preservation

Use the request as the contract when it already names the format, sharing scope, destination, and version to change. Otherwise, default to one local, self-contained HTML file and ask only about consequential unresolved choices before publishing, replacing a file, or creating extra deliverables.

For an edit, identify the current source and output by content and modification state, not merely a filename or an open browser tab. Inspect the actual file or reload the final URL before and after the change. If several candidates remain plausible, clarify which is current; do not overwrite one speculatively.

Keep the approved content in the JSON or the deck's existing generator source. Preserve that source, and regenerate only the intended target. An explicit request to update a named current artifact authorizes that change, not replacement of earlier versions. Record which files must remain unchanged and compare their bytes or hashes afterward. Do not create backup decks or alternate exports without agreement just to avoid deciding which file to edit.

The bundled generator refuses an existing output unless `--overwrite` is supplied. Even with that flag, it rejects the input file as the output, renders before replacing anything, and replaces through a temporary file. This protects an approved output from failed generation; it does not determine which version the user intended.

## Copy-first, user-directed review

Choose the lightest useful workflow. Do not insist on slide-by-slide approval for a clear one-shot request, a minor edit, or already approved copy. When the user requests slide-by-slide mode, present only the current slide's exact proposed copy:

| Field | What to agree |
| --- | --- |
| Title | A concrete claim, question, or decision |
| Labels and legend | Exact component, option, and state names |
| Summary | What the audience should understand |
| Visible qualifications | Evidence status and caveats that change interpretation |
| Notes and references | Supporting detail, source links, and provenance |

Record revisions and approval in the existing structured source or working record. Keep approved slides stable and wait for approval before moving to the next slide. Build the visuals from that copy afterward. Do not silently paraphrase approved labels to fit a box; reflow, enlarge the available area, or seek agreement on a meaningful rewrite.

Favor comprehension over raw brevity. For example, "Which processing model survives a worker restart?" is more useful than an unearned slogan. If the user intentionally requests an analogy or a distinctive voice, retain it without converting uncertain claims into guarantees.

## Plain language and meaningful visuals

These are defaults for every deck, not just for copy-review mode. Write so a reader with no access to the discussion can understand the slide. Use familiar nouns, direct verbs, concrete titles, and a short explanation when an acronym or domain term is necessary. Avoid adding jargon to sound authoritative.

For example, replace "Unlock resilient execution alignment" with "Who retries the job after a worker stops?" only when retry ownership is actually the question. Replace "Async handoff" with "The service queues the job and returns before the job finishes" when that is the intended meaning. Keep real code identifiers intact and do not silently rewrite an approved technical term.

Start each idea by considering the visual relationship:

| What needs explaining | Useful starting point |
| --- | --- |
| Components and ownership | A labeled architecture diagram |
| Order, handoffs, or retries | A sequence or flow diagram |
| A state change | A before/after view with the change highlighted |
| Alternatives and tradeoffs | Side-by-side diagrams or a compact comparison table |
| Measured behavior | A chart with units, evidence, and visible conditions |
| A physical object or visible interface | A properly authorized embedded picture |

Do not turn a paragraph into a diagram-shaped paragraph, add decorative icons, or invent measurements to fill a chart. Preserve all requested options and facts while moving detailed explanations to notes. Supply reader equivalents; keep qualifications needed for interpretation visible. A short paragraph or table is better than a forced visual when it explains the idea more directly.

Use finite animations that reveal a step, transition, or state change and end on a readable frame. Make replay possible, respect reduced motion, and ensure the static or reader view still communicates the relationship. Do not add external image-generation calls or new services as an implicit part of slide authoring.

Check: can an unfamiliar reader explain what the slide shows, its main point, and its takeaway without the authoring conversation? If not, fix the visual or wording rather than merely reducing the word count.

## Preserve the comparison

Inventory all requested alternatives and each one's relationship to the others before compressing the story. A queue-driven worker, a request-driven service, and a scheduled batch job are distinct alternatives in a comparison; variants of one should not absorb another just to make a tidy outline. Preserve non-preferred alternatives and explain their tradeoffs fairly.

Use a glossary or shared slide data for terms shown in diagrams, reader descriptions, notes, legends, and hotspots. Do not globally replace terms inside source URLs, commit identifiers, or code symbols.

Clarify what a domain term means before making an architectural claim. For example, permission to call an operation is different from the application's current workflow state. "Available" could mean authorized, currently enabled, deployed, or healthy. Ask a focused question when the source does not resolve the distinction; avoid presenting the ambiguous phrase as established fact.

Label proposals as proposals and demonstrations as demonstrations. A test result under a particular load is not a production service guarantee. Keep the conditions that affect a comparison visible, and put the fuller evidence trail in notes. Do not invent measurements to fill an attractive metric graphic.

## Links and viewer constraints

Place each supplied architecture/reference URL at the relevant diagram or row. Use a visible native link or a labeled hotspot with a visible reference list; make the same URL available in the mobile/reader view and notes. Preserve the exact URL, including commit pins, queries, and fragments. Link labels may use the shared glossary, but URLs and real code identifiers remain intact.

SVG displayed through an image cannot provide clickable internal links. The generator keeps that image isolation and adds native HTML anchors around it; do not rely on an invisible overlay alone. References are not fetched automatically. If the host blocks opening a link, keep the visible URL available for copying rather than trying to bypass its policy.

Do not assume all document portals execute JavaScript, or that none do. Test the relevant context where access is available:

- Ordinary top-level HTML, including a directly opened local file.
- Script-enabled embedding, including opaque-origin `about:srcdoc` with a blob base URL when relevant.
- Script-disabled reading, where the generated document exposes all slides and text without navigation controls.

The existing runtime deliberately has no URL synchronization. Preserve that simplicity. If a different template already writes URL state, let navigation update independently, synchronize only in suitable top-level contexts, and catch only `SecurityError` around the URL write. Disable further unsafe writes after that error; propagate unrelated exceptions. Do not introduce hash navigation just to add this guard.

Focus skip targets through the DOM rather than resolving a fragment against an unsafe base URL. Treat fullscreen availability, popup permission, and script execution as separate capabilities. Do not change a sandbox or tenant policy to force compatibility. A simulated embedding test is not a real tenant deployment test.

## Bounded release pass

Build the complete agreed deck, then inspect all of the following in one batched pass using available tools:

- Every slide's exact title, labels, summary, caveats, option inventory, and source links against the approved copy.
- Context-independent wording and a meaningful visual relationship, not jargon or a wall of bullets; the main point and takeaway should stand alone.
- Rendered text bounds, clipping, overlap, contrast, and useful target sizes. Measure actual rendered geometry rather than repeatedly shrinking labels or applying a fixed word-count reduction.
- Desktop and narrow/mobile layouts, long text, and reader mode. Preserve readable text instead of treating a shrunken diagram as a sufficient mobile view.
- Previous/next, first/last, Space, and boundary behavior; native controls and links through Tab/Enter; notes through their native disclosure control; skip focus and focus when changing views.
- Finite, replayable animation and reduced motion with a static diagram or an honest text fallback, including qualifications and references.
- Applicable top-level, embedded, and script-disabled states, plus explicit handling of expected fullscreen denial. Do not claim a host-specific check that was unavailable.

Collect observed defects, fix them together in the source and intended artifact, and confirm once. Additional passes should address a concrete remaining failure, not introduce new styling or exports. Contact sheets and screenshots are internal QA unless requested.

Before delivery, verify the actual final file or URL rather than a stale preview, compare preserved outputs, and clean only temporary review files you created. Keep reproducible source and approved outputs. State what ran, what did not, and any remaining fidelity or viewer limitations. Adding eval prompts is not the same as running behavioral evals.

Once the original task is complete, apply the optional contribution workflow in [contributing.md](contributing.md) once. It must not hold the deliverable hostage to another review or publication decision.
