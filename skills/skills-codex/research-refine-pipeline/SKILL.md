---
name: "research-refine-pipeline"
description: "Run an end-to-end workflow that chains `research-refine` and an evidence-development plan. Use when the user wants a one-shot pipeline from vague research direction to focused final proposal plus a detailed evidence-development roadmap, or asks to \"\u4e32\u8d77\u6765\", build a pipeline, do it end-to-end, or generate both the thesis and the evidence plan together."
---

# Research Refine Pipeline: End-to-End Thesis and Evidence Planning

Refine and concretize: **$ARGUMENTS**

## Overview

Use this skill when the user does not want to stop at a refined thesis. The goal is to produce a coherent package that includes:

- a problem-anchored, elegant final proposal
- the review history explaining why the thesis is focused
- a detailed evidence-development roadmap tied to the paper's claims
- a compact pipeline summary that says what to do next

This skill composes two existing workflows:

1. `research-refine` for thesis refinement
2. an evidence-development plan for claim-driven validation (sources, cases, statutes, arguments)

For stage-specific detail, read these sibling skills only when needed:

- `../research-refine/SKILL.md`
- `../research-review/SKILL.md`

## Core Rule

Do not build a large evidence base on top of an unstable thesis. First stabilize the thesis. Then develop the evidence that supports the stable thesis.

## Default Outputs

- `refine-logs/FINAL_PROPOSAL.md`
- `refine-logs/REVIEW_SUMMARY.md`
- `refine-logs/REFINEMENT_REPORT.md`
- `refine-logs/EXPERIMENT_PLAN.md`
- `refine-logs/EXPERIMENT_TRACKER.md`
- `refine-logs/PIPELINE_SUMMARY.md`

## Workflow

### Phase 0: Triage the Starting Point

- Extract the problem, rough approach, constraints, resources, and target venue.
- Check whether `refine-logs/FINAL_PROPOSAL.md` already exists and still matches the current request.
- If the proposal is missing, stale, or materially different from the current request, run the full `research-refine` stage.
- If the proposal is already strong and aligned, reuse it and jump to experiment planning.
- If in doubt, prefer re-running `research-refine` rather than planning experiments for the wrong method.

### Phase 1: Method Refinement Stage

Run the `research-refine` workflow and keep its V3 philosophy intact:

- preserve the Problem Anchor
- prefer the smallest adequate mechanism
- keep one dominant contribution
- modernize only when it improves the paper

Exit this stage only when these are explicit:

- the final method thesis
- the dominant contribution
- the complexity intentionally rejected
- the key claims and must-run ablations
- the remaining risks, if any

If the verdict is still `REVISE`, continue into experiment planning only if the remaining weaknesses are clearly documented.

### Phase 2: Planning Gate

Before the experiment stage, write a short gate check:

- What is the final method thesis?
- What is the dominant contribution?
- What complexity was intentionally rejected?
- Which reviewer concerns still matter for validation?
- Is a frontier primitive central, optional, or absent?

If these answers are not crisp, tighten the final proposal first.

### Phase 3: Experiment Planning Stage

Run the `experiment-plan` workflow grounded in:

- `refine-logs/FINAL_PROPOSAL.md`
- `refine-logs/REVIEW_SUMMARY.md`
- `refine-logs/REFINEMENT_REPORT.md`

Ensure the experiment plan covers:

- the main anchor result
- novelty isolation
- a simplicity or deletion check
- a frontier necessity check if applicable
- run order, budget, and decision gates

### Phase 4: Integration Summary

Write `refine-logs/PIPELINE_SUMMARY.md`:

```markdown
# Pipeline Summary

**Problem**: [problem]
**Final Method Thesis**: [one sentence]
**Final Verdict**: [READY / REVISE / RETHINK]
**Date**: [today]

## Final Deliverables
- Proposal: `refine-logs/FINAL_PROPOSAL.md`
- Review summary: `refine-logs/REVIEW_SUMMARY.md`
- Experiment plan: `refine-logs/EXPERIMENT_PLAN.md`
- Experiment tracker: `refine-logs/EXPERIMENT_TRACKER.md`

## Contribution Snapshot
- Dominant contribution:
- Optional supporting contribution:
- Explicitly rejected complexity:

## Must-Prove Claims
- [Claim 1]
- [Claim 2]

## First Runs to Launch
1. [Run]
2. [Run]
3. [Run]

## Main Risks
- [Risk]:
- [Mitigation]:

## Next Action
- Proceed to develop the evidence (`/statute-case-mapper`, `/comparative-law`, `/argument-stress-test`, or source/corpus work)
```

### Phase 5: Present a Brief Summary to the User

```
Pipeline complete.

Thesis output:
- refine-logs/FINAL_PROPOSAL.md

Evidence-plan output:
- refine-logs/EVIDENCE_PLAN.md
- refine-logs/EVIDENCE_TRACKER.md

Pipeline summary:
- refine-logs/PIPELINE_SUMMARY.md

Best next step:
- develop the evidence (statute-case-mapper / comparative-law / argument-stress-test / source work)
```

## Output Protocols

> Follow these shared protocols for all output files:
> - **[Output Versioning Protocol](../../shared-references/output-versioning.md)** — write timestamped file first, then copy to fixed name
> - **[Output Manifest Protocol](../../shared-references/output-manifest.md)** — log every output to MANIFEST.md
> - **[Output Language Protocol](../../shared-references/output-language.md)** — respect the project's language setting

## Key Rules

- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.

- Do not let the evidence plan override the Problem Anchor.
- Do not widen the paper story after thesis refinement unless a missing validation block is truly necessary.
- Reuse the same claims across `FINAL_PROPOSAL.md`, `EVIDENCE_PLAN.md`, and `PIPELINE_SUMMARY.md`.
- Keep the main paper story compact.
- If the thesis is intentionally simple, defend that simplicity in the evidence plan rather than adding new components.
- Prefer the staged skills when the user only needs one stage; use this skill for the integrated flow.

## Composing with Other Skills

```
/research-refine-pipeline -> one-shot thesis + evidence planning
/research-refine   -> thesis refinement only
develop evidence   -> statute-case-mapper / comparative-law / argument-stress-test / source work
/research-review   -> critical review
```

