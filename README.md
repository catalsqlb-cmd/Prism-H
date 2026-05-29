# Prism-H 📚⚖️

**Prism for the Humanities & Social Sciences** — a discipline-aware research pipeline for Claude Code (and Codex CLI, Cursor, Trae, and other agents).

🤖 **AI agents:** read [`AGENT_GUIDE.md`](AGENT_GUIDE.md) instead — structured for LLM consumption.

![Prism Logo](docs/prism_logo.svg)

[中文版 README](README_CN.md) | English

> 🪶 **Radically lightweight — zero dependencies, zero lock-in.** Every skill is a single `SKILL.md` file in plain Markdown. No framework, no database, no Docker. Swap Claude Code for [Codex CLI](skills/skills-codex/) or another agent and the workflows still work.
>
> *💡 Prism-H is a methodology, not a platform. Take the workflow wherever you go.* 🌱

Prism-H is the humanities & social-science edition of [Prism](https://github.com/catalsqlb-cmd/Prism). It keeps the literature → research-question → evidence → review → paper lifecycle and the cross-model review loop, but drops everything tied to computational experiments (GPU runs, ML idea automation, patent drafting). What remains is tuned for **doctrinal, argumentative, qualitative, and empirical social-science scholarship**.

These skills orchestrate **cross-model collaboration**: Claude Code drives the research while an external LLM (via [Codex MCP](https://github.com/openai/codex)) acts as a critical reviewer — **speed × rigor**.

## 🎓 Supported Disciplines

PRISM auto-detection writes a `PRISM_PROFILE.md` that adapts literature sources, evidence standards, paper structure, citation style, and review dimensions per discipline:

| ID | Discipline |
|----|------------|
| `law` | Law / Legal Studies |
| `sports-law` | Sports Law / Sports Governance |
| `philosophy` | Philosophy (esp. moral & political) |
| `logic` | Logic (formal & philosophical) |
| `economics` | Economics / Finance |
| `social-sciences` | Social Sciences |
| `education` | Education Research |
| `management` | Management / Business |
| `communications` | Communications / Media Studies |
| `humanities` | Humanities (default fallback) |

## 🚀 Quick Start

**Full pipeline** — hand Prism-H a research direction and it runs the lifecycle end-to-end:

```
/prism-pipeline "athletes' right to fair process in doping adjudication"
```

`/prism-pipeline` adds the **Soul Protocol** (a short authorial interview + human checkpoints + a final voice audit). For the same stages **without** the interview layer, use:

```
/research-pipeline "athletes' right to fair process in doping adjudication"
```

**Stage by stage**, you can also call each skill directly:

```
/research-lit "topic"                 # literature review (Zotero / Obsidian / web / Semantic Scholar)
/research-refine "PROBLEM … | THESIS …"  # sharpen the research question / thesis
/statute-case-mapper "claim"          # (law) map claims → statutes / cases / CAS awards
/comparative-law "issue across X, Y"  # (law) functional comparison
/argument-stress-test "claim"         # adversarial soundness gate
/research-review "thesis"             # discipline-aware critical review
/citation-audit                       # verify the bibliography before submission
/paper-writing "RESEARCH_LOG.md"      # plan → write → compile
```

## 🔁 The Pipeline

```
PRISM detect → /research-lit → research-question formulation → develop evidence → /research-review → /paper-writing (optional)
```

- **Develop evidence** means what the discipline calls for: a legal issue map with statutes/cases/rules and a comparative matrix; an argument reconstruction with an objection/response map; a source corpus with an analytical framework; or a dataset / survey / interview / coding protocol with an analysis write-up.
- **Quality gates** (advisory by default, blocking under `strict`): `statute-case-mapper` / `comparative-law` / `argument-stress-test` / `citation-audit` for law; `proof-checker` / `formula-derivation` for formal logic; `argument-stress-test` for argumentative work; `paper-claim-audit` for empirical social science.
- **Deterministic pre-check**: `tools/text_review.py` is a model-free lint (21 rules — vague/future-dated citations, over-assertion, terminology drift, and an argument-logic series: assert-without-argue, list-without-advance, quotation-without-analysis, unsupported intensifiers). Run it before the model passes so the cross-model review spends its budget on substance, not hygiene.

## 🧩 Side Tracks

- **Funding** — `/grant-proposal` branches from a validated research question.
- **Submission response** — `/rebuttal` consumes external reviews (never invents evidence).
- **Presentation** — `/paper-slides`, `/paper-poster` consume a compiled, audited paper.
- **Collaboration** — `/overleaf-sync` is a transport layer only.
- **Memory** — `/research-wiki` and the portable [LLM-Wiki](skills/llm-wiki/) persist sources, arguments, and review outcomes.

## 🛠️ Installation

Recommended (project-local symlinks):

```bash
bash tools/install_prism.sh /path/to/your/project
```

Add a personal knowledge base at install time:

```bash
bash tools/install_prism.sh /path/to/your/project --with-wiki /path/to/wiki
```

Each skill is symlinked into `<project>/.claude/skills/<skill-name>`; a manifest at `<project>/.prism/installed-skills.txt` tracks every managed link so uninstall never touches your own skills.

## 📝 Citation Styles

Prism-H ships citation routing for the venues humanities & social-science authors actually target: footnote/endnote (脚注/尾注) for Chinese law and social-science journals, Bluebook (US law), OSCOLA (UK/EU law), APA (social sciences), and Chicago (humanities). Legal citations resolve to article/paragraph/item, full case numbers, and standard CAS-award format. See [`citation-cn-footnote.md`](skills/shared-references/citation-cn-footnote.md) and [`citation-discipline.md`](skills/shared-references/citation-discipline.md).

For English abstracts and titles, a ZH↔EN theory-term glossary ([`theory-terminology.md`](skills/shared-references/theory-terminology.md)) supplies standard renderings for the humanities theory canon plus law / sports-law / moral & political philosophy, keeping one concept → one term across the paper.

## 🔑 Key Rules

- **Profile-driven** — every stage reads `PRISM_PROFILE.md`; if missing, falls back to humanities defaults.
- **No fabricated evidence** — claims must trace to grounded sources, cases, data, or valid arguments.
- **Cross-model review** — the executor and the reviewer are different models, so the reviewer probes blind spots the executor can't see.

## 📄 License

MIT. Forked from [Prism](https://github.com/catalsqlb-cmd/Prism) and trimmed to the humanities & social sciences.
