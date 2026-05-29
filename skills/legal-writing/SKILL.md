---
name: legal-writing
description: Drafts doctrinal, law-and-economics, comparative-law, and humanities (interpretive/historical) scholarship and dissertation outlines, using the discipline profile's structure templates, citation style, and the upstream authority/comparison artifacts. Use when user says "写法学论文", "draft this section", "法学写作", "写博论提纲", "dissertation outline", "起草释义论/立法论", "write this chapter", or wants discipline-correct legal/humanities prose.
argument-hint: [section/chapter to draft, or "outline" for a dissertation outline]
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, Agent, mcp__codex__codex, mcp__codex__codex-reply
---

# Legal / Humanities Writing: Discipline-Correct Drafting

Draft doctrinal and normative scholarship the way the field actually expects — not
generic "academic prose." This is the law/humanities counterpart of `/paper-write`:
it consumes the discipline profile's structure templates, citation rules, and the
upstream grounding artifacts (`STATUTE_CASE_MAP.json`, `COMPARATIVE_ANALYSIS.json`),
and produces either a full dissertation outline or drafted sections that are ready
for `/argument-stress-test` and `/citation-audit`.

## Context: $ARGUMENTS

## Constants

- DRAFT files written into the project / paper directory (e.g. `main.tex`, `chapters/*.tex`, or `.md` if the project is markdown-based)
- OUTLINE_DOC: `DISSERTATION_OUTLINE.md` (outline mode)
- Discipline config comes from `PRISM_PROFILE.md`; fall back to `law` defaults if absent.

## When to Use

- After `/statute-case-mapper` (and optionally `/comparative-law`) have grounded
  the argument — draft from the map, not from memory
- To produce a dissertation outline before any drafting
- To draft or revise a specific section/chapter
- Before `/argument-stress-test`, which then audits what you wrote

## Step 0: Load discipline config and upstream artifacts

1. Read `PRISM_PROFILE.md`. Extract: **Paper Structure** templates, **Citation
   Style**, **Review Dimensions** (the rubric you are writing *to*), and
   **Discipline-Specific Rules**.
2. Read any upstream artifacts present: `STATUTE_CASE_MAP.json` (authorities per
   claim), `COMPARATIVE_ANALYSIS.json` (functional comparison + transplant screen),
   `ARGUMENT_AUDIT.json` (prior stress-test flags to fix while drafting).
3. Pick the structure template that matches the work:
   - law: 法教义学论文 / 法经济学论文 / 比较法论文 / (sports-law: 体育法教义学·政策 / 体育法经济学)
   - humanities: 释义/分析论文 / 历史研究论文
   - dissertation: use the profile's dissertation outline shape.

## Mode A: Dissertation outline (`outline`)

Produce `DISSERTATION_OUTLINE.md`:

- Title + one-paragraph thesis (主线论点) — what is claimed and why it matters.
- Per chapter: heading, the **claim that chapter establishes**, the method
  (教义学/比较/法经济学/释义/史学), the key authorities/sources it will rest on
  (pulled from `STATUTE_CASE_MAP.json` where available), and the page budget from
  the profile template.
- An explicit **释义论 vs 立法论** split for law work: which chapters analyze
  current law (lege lata / 解释论) and which propose reform (lege ferenda / 立法论).
  Keep them from bleeding into each other.
- A dependency note: which chapters must be grounded (`/statute-case-mapper`) or
  compared (`/comparative-law`) before drafting.

## Mode B: Draft a section / chapter

1. **Write to the rubric.** The profile's Review Dimensions are the target — for
   `law`, Doctrinal Rigor (25%) and Argument Quality (25%) dominate, so the prose
   must lead with authority and reasoning, not throat-clearing.
2. **Draft from the map, cite as you go.** Every normative sentence pulls its
   authority from `STATUTE_CASE_MAP.json` with a proper pin-cite. Do not assert law
   you have not grounded — if the map says `ungrounded`, flag it inline as
   `〔待补权威〕` rather than inventing a citation.
3. **Citation format from the profile.** Chinese law → footnotes (脚注) per
   `shared-references/citation-cn-footnote.md`; US → Bluebook; UK/EU → OSCOLA;
   humanities → Chicago/MLA. Substantive footnotes are expected in law/humanities —
   use them for qualifications and scholarly dialogue, not just citations.
4. **Honor the discipline rules**: positive-law-first; 解释论/立法论 separation;
   systematic (not cherry-picked) case treatment; functional (not tourist)
   comparison; China-facing conclusion; transparent normative commitments. For
   humanities: interpretation over information, close reading as evidence, engage
   the tradition, avoid scientism and presentism.
5. **Leave audit hooks.** Tag each load-bearing claim so `/argument-stress-test`
   and `/citation-audit` can find them; do not bury claims in prose mush.

## Step N: Hand off, don't self-certify

After drafting, print what was written and the recommended next gates:

```
✍️ Legal Writing Complete  (discipline: sports-law, mode: draft §3 现行法分析)

  Drafted:        chapters/03_positive_law.tex  (~3.5 pages)
  Citations:      14 footnotes (脚注, GB/T 7714)
  Grounded from:  STATUTE_CASE_MAP.json (12 authorities)
  ⚠️ 待补权威:    1 claim flagged 〔待补权威〕 (C7 — 无对应判例)

  Next gates:
    /argument-stress-test   → audit doctrinal soundness
    /citation-audit         → verify the 14 footnotes (L3 claim-level)
```

The skill **never** declares its own draft submission-ready. Soundness is decided
by `/argument-stress-test`; citation correctness by `/citation-audit`. Writing,
grounding, and judging stay separate (same separation as the STEM pipeline).

## Local Wiki Defaults

If the profile declares an external wiki / `research-wiki/` exists, pull durable
analyses and source summaries from `wiki/memos/` and `wiki/sources/` while drafting,
and write new durable prose back there. Never modify `raw/`.

## Key Rules

- **Draft from grounding, not memory.** No normative claim without a mapped
  authority or an explicit `〔待补权威〕` flag. Inventing citations is the cardinal sin.
- **Write to the profile's rubric.** Doctrinal rigor and argument quality are the
  heaviest weights in law — earn them, don't pad with background.
- **解释论 ≠ 立法论.** Never let "what the law is" and "what it should be" blur in
  the same paragraph; the profile flags this explicitly.
- **Citation style is not optional.** Match the venue's format exactly via
  `citation-cn-footnote.md` or the relevant style.
- **Hand off to the gates.** Drafting does not certify; `/argument-stress-test` and
  `/citation-audit` do.
