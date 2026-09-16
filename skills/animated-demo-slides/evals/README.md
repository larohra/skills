# Behavioral evals

`evals.json` contains neutral authoring scenarios and assertions, not recorded results. Run them through an agent evaluation separately from the deterministic generator and browser tests. Do not report a scenario as passed merely because its JSON parses or a related unit test passes.

Use an isolated evaluation workspace, not a real user's deck, installed skill, or unrelated task repository. For the small in-place edit scenario (id 7), stage `fixtures/reference-deck.json` as `reference-deck.json`, build `current.html` with the bundled generator, and copy that generated file once to `preserved.html` before starting the agent. Record the preserved file's bytes or hash. The copy is an internal test fixture, not another user deliverable. Compare it after the agent's edit.

The embedding scenario uses a neutral fixture and a local simulated viewer; a passing simulation does not establish real tenant compatibility. The contribution scenarios should use recorded/simulated tool outcomes or a dry-run evaluation harness, not real publication. A hypothetical approval in an eval prompt is not authorization to publish into a live repository.

Check the conversational behavior as well as generated files: exact copy approval, unnecessary questions, taxonomy preservation, context-independent wording, meaningful visuals, and contribution approval/deduplication/privacy/no-recursion require observing the agent's actual actions.
