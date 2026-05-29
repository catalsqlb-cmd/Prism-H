---
name: research-pipeline
description: "Full humanities/social-science research pipeline without the Soul Protocol layer: discipline detection → literature → research questions → evidence development → critical review → paper writing (optional). Use when user says \"全流程\", \"full pipeline\", \"从选题到投稿\", \"end-to-end research\", or wants the complete research lifecycle without the soul interview/audit."
argument-hint: [research-direction]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Skill, mcp__codex__codex, mcp__codex__codex-reply
---

# Full Research Pipeline (Humanities & Social Sciences)

End-to-end research workflow for: **$ARGUMENTS**

This is the non-interactive sibling of `/prism-pipeline`. It runs the same discipline-aware stages but omits the Soul Protocol (soul interview, soul-enriched gates, soul audit). Use `/prism-pipeline` when you want the human-checkpoint and authorial-voice layer.

## Constants

- **DISCIPLINE = auto** — When `auto`, Stage 0 runs `/prism-pipeline — mode: detect-only` to detect from input and project context and write `PRISM_PROFILE.md`. Override with an explicit ID: `law`, `sports-law`, `economics`, `social-sciences`, `humanities`, `philosophy`, `logic`, `education`, `management`, `communications`. See `shared-references/prism-routing.md`.
- **AUTO_PROCEED = false** — When `false`, pause at each stage boundary for confirmation. When `true`, auto-select and continue. If detection fails and `AUTO_PROCEED=true`, default to `humanities`.
- **AUTO_WRITE = false** — When `false`, stop after critical review and leave paper writing to an explicit `/paper-writing` call.
- **QUALITY_GATES = standard** — `off` skips evidence/citation gates; `standard` treats failures as advisory; `strict` blocks paper writing until critical failures are fixed.

## Pipeline Overview

```
PRISM detect → /research-lit → research questions → develop evidence → /research-review → /paper-writing (optional)
```

## Stage 0: Discipline Detection

Run `/prism-pipeline "$ARGUMENTS" — mode: detect-only` (or honor an explicit `DISCIPLINE`) to produce `PRISM_PROFILE.md`. All downstream skills read it for discipline-specific routing.

## Stage 1: Literature Review

```
/research-lit "$ARGUMENTS"
```

`/research-lit` reads `PRISM_PROFILE.md` and adapts source priority, venue filtering, and terminology. Humanities and law weight foundational works and primary sources (statutes, cases, canonical texts) over recent preprints.

## Stage 2: Research-Question Formulation

Formulate 3–6 candidate research questions / theses grounded in the Stage 1 literature, then validate:

```
/novelty-check [candidate questions]
/research-review [top candidates]
```

If `AUTO_PROCEED=false`, present the ranked candidates and let the user choose before continuing.

## Stage 3: Develop the Evidence Base

Build the evidence appropriate to the discipline (read `PRISM_PROFILE.md`):

- **Law / sports law**: legal issue map; statutes/cases/rules; comparative matrix
- **Philosophy / logic**: argument reconstruction; formalized inferences; objection/response map; for formal work, proof obligations
- **Economics / social sciences / education / management**: dataset assembly, empirical/identification strategy, analysis write-up; or survey/interview/coding protocols
- **Humanities / communications**: source corpus, analytical framework, close reading

Document findings in `RESEARCH_LOG.md`.

## Stage 3.5: Evidence & Citation Gates

Run unless `QUALITY_GATES=off` (advisory under `standard`, blocking under `strict`):

- **Law / sports law**: `statute-case-mapper` → `comparative-law` → `argument-stress-test` → `citation-audit` (L3)
- **Philosophy / logic (formal)**: `/proof-checker`, `/formula-derivation`
- **Philosophy / logic (argumentative) & humanities**: `argument-stress-test`
- **Empirical social science / economics / education / management**: `/paper-claim-audit`
- **All disciplines**: `/citation-audit` before submission if a bibliography exists

## Stage 4: Critical Review

```
/research-review "$ARGUMENTS — [chosen thesis]"
```

The reviewer uses the discipline's review dimensions from `PRISM_PROFILE.md`. Hand specific claims to `/argument-stress-test` for a deeper adversarial pass. Output: `review-stage/RESEARCH_REVIEW.md`.

## Stage 5: Paper Writing (optional)

Skip unless `AUTO_WRITE=true` or the user requests it.

```
/paper-writing "report-or-research-log"
```

Internally: `/paper-plan → /paper-write → /paper-compile`, with `/research-refine` for iterative polish after the evidence/citation gate is clean.

## Side Tracks

- **Funding**: `/grant-proposal` branches from a validated research question; parallel to the publish track.
- **Submission response**: `/rebuttal` consumes external reviews; never invent new evidence.
- **Presentation**: `/paper-slides`, `/paper-poster` consume a compiled, audited paper.
- **Collaboration**: `/overleaf-sync` is a transport layer only.

## Key Rules

- **Profile-driven**: every stage reads `PRISM_PROFILE.md`; if missing, fall back to `humanities` defaults.
- **No fabricated evidence**: claims must trace to grounded sources, cases, data, or valid arguments.
- **Specialist skills are optional**: if a named slash skill is unavailable, search local skill roots (`.claude/skills`, `.codex/skills`, `.agents/skills`, `Prism-H/skills`) for `*/SKILL.md` and execute the closest equivalent.
- For the human-checkpoint and authorial-voice layer, use `/prism-pipeline` instead.
