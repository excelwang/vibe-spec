---
name: vibespec
description: Spec-driven development workflow. Distills raw ideas into traceable L0-L3 specifications, validates existing specs, bootstraps minimal implementation and test skeletons, and reviews or reflects spec changes. Use when user says "vibespec", "vibe spec", "vibe-spec", "refine specs", wants to capture a new idea, validate specifications, bootstrap implementation, review specs, or distill code observations back into specs.
---

# Vibespec Skill

Manage the refinement of raw thoughts into traceable specifications.

## Routing Principles

- Before classifying layers or auditing spec structure, load `references/layer_system.md`.
- Keep detailed workflow steps in `references/`; only load the file needed for the active command.
- Use bundled scripts for deterministic operations instead of re-deriving their logic in prompt text.

## Triggers

### `vibespec`
- Present the available workflows: `ingest`, `bootstrap impl`, `test`, `bug`, `reflect`, `distill`, `review`, and `idea`.

### `vibespec ingest`
- If `specs/` is missing, load `references/ingest_workflows.md` and run `BootstrapWorkflow`.
- If `ideas/` contains pending files, load `references/ingest_workflows.md` and run `IdeaToSpecWorkflow`.
- Otherwise, load `references/review_workflows.md` and run `SpecValidationWorkflow`.

### `vibespec bootstrap impl`
- Load `references/ingest_workflows.md`, `references/layer_system.md`, and `references/testing_protocol.md`.
- Run `ImplementationBootstrapWorkflow`.
- Use `python3 scripts/bootstrap_impl.py --lang <profile>` after validating `specs/`.
- If implementation already exists, stop and direct the user to the appropriate specs workflow: `vibespec test`, `vibespec review`, `vibespec bug`, or `vibespec distill`.

### `vibespec reflect`
- Analyze recent conversation history for new requirements or architectural changes.
- Convert them into candidate ideas only after user approval.

### `vibespec idea <content>`
- Save `<content>` as a new idea file using `assets/IDEA_TEMPLATE.md`.

### `vibespec review [SPEC_ID]`
- Load `references/review_workflows.md` and `references/review_and_quality.md`.
- Run `SpecAuditWorkflow` for the selected item or layer root.

### `vibespec bug [description]` / `vibespec bug review`
- Load `references/review_workflows.md`.
- Run `BugRCAWorkflow`.

### `vibespec distill`
- Load `references/layer_system.md`.
- Run `DistillWorkflow` to extract missing or unreasonable design details from code and propose spec improvements for human review.

### `vibespec test`
- Load `references/ingest_workflows.md` and `references/testing_protocol.md`.
- If `src/` is missing or empty, stop and direct the user to `vibespec bootstrap impl`.
- Run `CertificationWorkflow`.

## Scripts

- `python3 scripts/validate.py specs/` — structural validation and L1 coverage auditing.
- `python3 scripts/bootstrap_impl.py --lang <profile>` — generate the minimal implementation, black-box skeleton tests, white-box skeleton tests, and `scripts/test-workflow.sh` for a `specs/`-only repo.

Run `python3 scripts/validate.py specs/` immediately after spec edits.

## References

- `references/layer_system.md`: L0-L3 classification rules and traceability model.
- `references/ingest_workflows.md`: bootstrap, idea-to-spec, and certification workflows.
- `references/review_workflows.md`: manual review, bug RCA, and validation-only audits.
- `references/review_and_quality.md`: self-audit and quality review protocol.
- `references/testing_protocol.md`: black-box and white-box testing rules.
- `references/CONCEPTS.md`: plain-language concept explanations.

## Global Constraints

- Use templates from `assets/` when generating files.
- Check `VISION.SCOPE` before refining requirements.
- Preserve strict L0 -> L1 -> L2 -> L3 traceability.
- Present only validated spec changes for human review.
- Re-read relevant specs whenever the user provides new context.
