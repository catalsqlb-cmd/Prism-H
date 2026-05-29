# Prism-H Agent Guide

> **For AI agents reading this repo.** If you are a human, see [README.md](README.md).

Prism-H is a **discipline-aware** research harness for the humanities & social sciences: composable Markdown skills that orchestrate the full research lifecycle — law, philosophy, logic, economics, social sciences, education, management, communications, and the humanities — through cross-model adversarial collaboration. It omits computational-experiment, ML-idea-automation, and patent skills.

## How to Invoke Skills

**Claude Code / Cursor / Trae:**
```
/skill-name "arguments" — key: value, key2: value2
```

**Codex CLI:**
```
/skill-name "arguments" — key: value
```
Codex skills are in `skills/skills-codex/`.

## Common Parameters

Every skill accepts:
```
— effort: lite | balanced | max | beast      # work intensity (default: balanced)
— human checkpoint: true | false             # pause for approval (default: false)
— AUTO_PROCEED: true | false                 # auto-continue at gates (default: true)
```

Workflow-specific:
```
— discipline: auto | law | philosophy | economics | ...  # discipline (default: auto-detect)
— difficulty: medium | hard | nightmare                  # reviewer adversarial level
— venue: 法学研究 | AER | APSR | Mind | ...               # target venue (discipline-aware)
— sources: web, zotero, obsidian, semantic-scholar, exa   # literature sources
```

Parameters pass through workflow chains automatically.

## Workflow Index

### Full Pipeline
```
/prism-pipeline "direction"    → PRISM → lit → question → evidence → review → paper  (+ Soul Protocol)
/research-pipeline "direction" → same stages without the Soul Protocol layer
```

### PRISM — Discipline Detection (Stage 0)

PRISM (Pipeline for Research with Intelligent Subject Mapping) auto-detects the research discipline and loads a methodology profile. Override with `— discipline: law`.

| Discipline ID | Field | Methodology | Key Venues |
|--------------|-------|-------------|------------|
| `law` | Law / Legal Studies | Doctrinal + comparative + empirical | 法学研究, 中国法学, Harvard Law Review |
| `sports-law` | Sports Law / Governance | Doctrinal + CAS jurisprudence + comparative | 体育科学, Int'l Sports Law Journal |
| `philosophy` | Philosophy (moral/political) | Conceptual analysis + argument | Ethics, Phil & Public Affairs, 哲学研究 |
| `logic` | Logic (formal/philosophical) | Formal proof + conceptual analysis | JSL, Review of Symbolic Logic |
| `economics` | Economics / Finance | Causal inference + modeling | AER, QJE, Econometrica |
| `social-sciences` | Social Sciences | Survey + qualitative + mixed | ASR, APSR, 社会学研究 |
| `education` | Education Research | Action research + quasi-experiments | AERJ, 教育研究 |
| `management` | Management / Business | Theory-testing + case study | AMJ, SMJ, 管理世界 |
| `communications` | Communications / Media | Textual + empirical + theory | Journal of Communication, 新闻与传播研究 |
| `humanities` | Humanities | Interpretive + historical | Critical Inquiry, 历史研究, PMLA |

Profile files: `skills/shared-references/prism-profiles/{id}.md`

### Pipeline Stages

| Stage | Invoke | Input | Output | When to use |
|-------|--------|-------|--------|-------------|
| 1: Literature | `/research-lit "direction"` | research direction | LIT_REVIEW.md | Starting new research |
| 2: Question | `/research-refine "PROBLEM … \| THESIS …"` | direction + literature | FINAL_PROPOSAL.md | Sharpen the research question / thesis |
| 3: Evidence | `/statute-case-mapper`, `/comparative-law`, `/argument-stress-test`, source work | thesis | RESEARCH_LOG.md, *_MAP.json | Develop the evidence base |
| 4: Review | `/research-review "scope"` | draft + evidence | RESEARCH_REVIEW.md | Critical review |
| 5: Paper | `/paper-writing "RESEARCH_LOG.md"` | research log | paper/main.pdf | Ready to write |
| Side: Rebuttal | `/rebuttal "paper/ + reviews"` | paper + reviews | PASTE_READY.txt | Reviews received |

### Standalone Skills

| Skill | Invoke | What it does |
|-------|--------|-------------|
| `/prism-pipeline "topic"` | PRISM full pipeline | Discipline-aware end-to-end lifecycle + Soul Protocol |
| `/research-lit "topic"` | Literature survey | Finds sources, builds landscape (Zotero/Obsidian/web/S2/Exa) |
| `/semantic-scholar "query"` | Published-venue search | Journal/book papers with citation counts and venue metadata |
| `/research-refine "…"` | Thesis refinement | Cross-model review loop that sharpens the question/thesis |
| `/novelty-check "thesis"` | Novelty verification | Checks against existing scholarship |
| `/statute-case-mapper "claim"` | (Law) evidence map | Maps claims → statutes / cases / CAS awards |
| `/comparative-law "issue"` | (Law) comparison | Functional comparison across jurisdictions |
| `/argument-stress-test "claim"` | Soundness gate | Adversarial check of inferential validity / doctrinal soundness |
| `/proof-checker`, `/proof-writer`, `/formula-derivation` | (Logic) formal work | Draft and verify formal proof obligations |
| `/research-review "draft"` | External review | GPT-5.4 xhigh discipline-aware critique |
| `/paper-claim-audit "paper/"` | Empirical claim audit | Fresh reviewer cross-checks claims vs cited sources/data |
| `/citation-audit "paper/"` | Bibliography audit | Verifies existence + metadata + context for every cite |
| `/legal-writing`, `/paper-plan`, `/paper-write`, `/paper-compile` | Drafting | Outline → LaTeX/prose → PDF |
| `/research-wiki init` | Knowledge base | Persistent project memory |
| `/grant-proposal "question"` | Funding branch | Narrative-arc grant application |
| `/overleaf-sync setup\|pull\|push\|status` | Overleaf bridge | Two-way sync; token stays in OS keychain |

## Artifact Contracts

Skills communicate through plain-text files:

| Artifact | Created by | Consumed by |
|----------|-----------|-------------|
| `PRISM_PROFILE.md` | prism-pipeline (detect) | research-lit, research-refine, paper-plan, paper-write |
| `LIT_REVIEW.md` | research-lit | research-refine, grant-proposal |
| `FINAL_PROPOSAL.md` | research-refine | evidence skills, research-review, grant-proposal |
| `RESEARCH_LOG.md` | evidence development | research-review, paper-writing |
| `STATUTE_CASE_MAP.json` | statute-case-mapper | argument-stress-test, paper-write |
| `COMPARATIVE_ANALYSIS.json` | comparative-law | paper-write |
| `ARGUMENT_AUDIT.json` | argument-stress-test | research-review, research-wiki |
| `paper/main.tex` | paper-write | paper-compile |
| `paper/main.pdf` | paper-compile | research-refine (polish), paper-slides/poster |
| `PAPER_CLAIM_AUDIT.md/.json` | paper-claim-audit | paper-writing claim gate |
| `CITATION_AUDIT.md/.json` | citation-audit | paper-writing submission gate |
| `research-wiki/` | research-wiki | research-refine, research-lit |

## Cross-Model Protocol

- **Executor** (Claude/Codex): surveys literature, develops evidence, drafts papers
- **Reviewer** (GPT-5.4/Gemini/GLM): critiques, scores, demands revisions
- **Rule**: executor and reviewer must be different model families
- **Reviewer independence**: pass file paths only, never summaries or interpretations
- **No fabricated evidence**: claims must trace to grounded sources, cases, data, or valid arguments

## Shared References

Read these before invoking review-related skills:
- `skills/shared-references/reviewer-independence.md` — cross-model review protocol
- `skills/shared-references/effort-contract.md` — effort level specifications
- `skills/shared-references/citation-discipline.md` — international citation rules
- `skills/shared-references/citation-cn-footnote.md` — Chinese footnote/endnote rules
- `skills/shared-references/writing-principles.md` — writing standards
- `skills/shared-references/venue-checklists.md` — venue formatting
- `skills/shared-references/prism-routing.md` — discipline detection and routing protocol
- `skills/shared-references/prism-profiles/` — per-discipline methodology profiles (10 disciplines)

## Research Wiki (Optional)

If `research-wiki/` exists in the project:
- `/research-lit` auto-ingests discovered sources
- `/research-refine` reads the wiki before formulation, writes candidate questions back after
- `/argument-stress-test` updates claim status
- Weak or unsupported claims become anti-repetition memory

Initialize with `/research-wiki init`.

## Effort Levels

| Level | Tokens | What changes |
|-------|:------:|-------------|
| `lite` | 0.4x | Fewer sources, questions, rounds |
| `balanced` | 1x | Current default behavior |
| `max` | 2.5x | More sources, deeper review |
| `beast` | 5-8x | Every knob to maximum |

Codex reasoning is **always xhigh** regardless of effort.

## Source of Truth

- Each skill's behavior: read its `skills/<name>/SKILL.md`
- System-wide rules: read `skills/shared-references/*.md`
- This guide is a routing index, not the specification
