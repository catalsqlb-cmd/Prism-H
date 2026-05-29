# PRISM-H Routing Protocol

*Pipeline for Research with Intelligent Subject Mapping — Humanities & Social Sciences edition*

Use this reference when a skill needs to adapt its behavior based on the detected research discipline. Prism-H covers law, the social sciences, and the humanities; it does not run computational experiments, GPU training, or ML idea automation.

## When to Read

- At the start of `/prism-pipeline` or `/research-pipeline` (Stage 0)
- When `/research-lit`, `/research-refine`, `/paper-plan`, or `/paper-write` starts
- Before evidence gates, submission audits, funding branches, or post-submission artifacts
- When linking a project to an external Markdown/Obsidian wiki
- When a skill needs discipline-specific configuration

## How PRISM Detection Works

1. Stage 0 of `/prism-pipeline` (or `/research-pipeline`) analyzes user input and project context
2. It writes `PRISM_PROFILE.md` to the project root
3. Downstream skills read `PRISM_PROFILE.md` to load discipline-specific configuration

## How to Consume the Profile

Every discipline-aware skill should check for `PRISM_PROFILE.md` at startup:

```
1. Check if PRISM_PROFILE.md exists in project root
2. If YES → read it and extract:
   - discipline ID
   - methodology profile (evidence types, validation standards)
   - literature sources (database priority)
   - venue tiers
   - paper structure template
   - review dimensions (with weights)
   - discipline-specific rules
   - recommended pipeline modules (optional specialist skills)
   - local wiki link (root, mode, query command, write policy)
3. If NO → fall back to humanities defaults (general qualitative scholarship)
```

## Skill-Specific Routing

### /research-lit
- **Route literature sources**: Use the discipline's database priority list. Humanities/law value monographs, statutes, cases, and foundational works over recent preprints
- **Adjust venue filtering**: Filter sources by the discipline's venue tiers
- **Adapt search queries**: Use discipline-appropriate terminology
- **Time window**: Humanities and law weight older foundational works heavily; do not down-rank by recency alone
- **Source enrichment**: Use `semantic-scholar` or `exa-search` only when the profile or user asks for those sources

### /research-refine
- **Swap review dimensions**: Replace any generic dimensions with the discipline's review dimensions
- **Adjust review prompt**: Set the reviewer persona to the appropriate discipline (e.g., "senior legal scholar", "moral philosophy referee")
- **Methodology principles**: Apply discipline-specific methodology rules (e.g., "always ground in positive law" for law)
- **Validation design**: Design validation appropriate to the discipline (doctrinal/case analysis, conceptual analysis, qualitative or empirical social-science methods)

### /paper-plan
- **Paper structure**: Use the discipline's paper structure template
- **Page budgets**: Adjust section page allocations per discipline conventions
- **Citation style**: **中文法学/社科期刊: 读取 `citation-cn-footnote.md`**; Bluebook for US law, APA for social sciences, OSCOLA for UK/EU law, Chicago for humanities
- **Section naming**: Use discipline-appropriate section names (e.g., "Institutional Background", "Doctrinal Framework")

### /paper-write
- **Writing conventions**: Apply discipline-specific writing rules
- **Citation format**: For Chinese law/social science venues, use footnote (脚注) or endnote (尾注) format per `citation-cn-footnote.md`; for international venues, use BibTeX/BibLaTeX per `citation-discipline.md`
- **Evidence presentation**: Prose narrative, tables, or figures vary by discipline
- **Venue formatting**: Load the venue-specific template; Chinese venues output Chinese content
- **Legal citation specifics**: 法律法规引精确到条/款/项; 案例引用含完整案号; CAS裁决用标准格式; 重复引用用简写规则 — 详见 `citation-cn-footnote.md`

### /research-wiki
- **Lifecycle memory**: Persist sources, ideas, arguments, and review outcomes when `ENABLE_RESEARCH_WIKI=true` or an active wiki exists
- **Argument tracking**: After `/argument-stress-test`, record each claim's verdict (SOUND / WEAK / UNSUPPORTED / INVALID / POLICY-AS-LAW / UNVERIFIABLE)
- **Re-ideation**: Feed weak or unsupported claims and evidence gaps back into `/research-refine`

### External local wiki
- Read `shared-references/local-wiki-link.md` when `LOCAL_WIKI_ROOT` is set or auto-detectable.
- Use external wiki pages as prior user knowledge before broad web search.
- Prefer the wiki's own query script when available (for example `scripts/query_wiki.py --wiki <root>/wiki --query "<topic>"`).
- Write back only stable pages, memos, source summaries, or backlinks when `LOCAL_WIKI_MODE=read-write`; never write to `raw/`.
- Keep Prism `research-wiki/` graph updates separate from external Obsidian/Markdown wiki updates unless a bridge memo explicitly links them.

### Evidence gates
- **Law / sports law**: `statute-case-mapper` grounds claims in 实证法/案例/CAS; `comparative-law` runs functional comparison; `argument-stress-test` is the doctrinal soundness gate; `citation-audit` (L3) verifies legal citations
- **Philosophy / logic (formal)**: `formula-derivation` stabilizes notation and assumptions; `proof-writer` drafts proof packages; `proof-checker` verifies formal proof obligations
- **Philosophy / logic (argumentative) & humanities**: `argument-stress-test` checks inferential validity and engagement with objections
- **Social sciences / economics (empirical)**: `paper-claim-audit` checks manuscript claims against the cited sources and reported data; `citation-audit` verifies references
- **All disciplines**: `/citation-audit` runs before submission if a bibliography exists

### Side tracks
- **Funding**: `/grant-proposal` branches from a validated idea or refined proposal. It should not replace evidence gates for papers.
- **Submission response**: `/rebuttal` consumes external reviews and verified evidence. Never invent new evidence during rebuttal.
- **Presentation**: `/paper-slides` and `/paper-poster` consume a compiled, audited paper.
- **Collaboration**: `/overleaf-sync` is only a transport layer; pull before editing and push only after conflict review.

## Recommended Module Matrix

Profiles may include a `Recommended Pipeline Modules` section. Treat it as routing hints, not hard dependencies.

## Local Module Resolution

When a recommended module is not installed as a slash skill, locate it as a local skill reference:

1. Search these roots in order: `.claude/skills`, `.codex/skills`, `.agents/skills`, `Prism-H/skills`.
2. Match by directory name or frontmatter `name`.
3. Read only the matched `SKILL.md` and any directly referenced files needed for the current stage.
4. Execute the equivalent workflow manually, then record that the module was used as a local reference rather than as an installed slash skill.

| Discipline | Literature / mapping | Execution / evidence | Review / submission |
|------------|----------------------|----------------------|---------------------|
| `law` | `research-lit`, `semantic-scholar`, `research-refine` | `statute-case-mapper`, `comparative-law`, `paper-plan` | `argument-stress-test`, `citation-audit`, `research-review` |
| `sports-law` | `research-lit`, `semantic-scholar`, `exa-search` | `statute-case-mapper`, `comparative-law`, `paper-plan` | `argument-stress-test`, `citation-audit`, `research-review` |
| `humanities` | `research-lit`, `semantic-scholar`, `research-refine` | `comparative-law` (text/framework comparison), `paper-plan`, `paper-write` | `argument-stress-test`, `citation-audit`, `research-review` |
| `philosophy` | `research-lit`, `semantic-scholar`, `research-refine` | `paper-plan`, `comparative-law` (framework comparison), `proof-checker` (formal steps) | `argument-stress-test`, `citation-audit`, `research-review` |
| `logic` | `research-lit`, `semantic-scholar`, `research-refine` | `formula-derivation`, `proof-writer` | `proof-checker` (formal), `argument-stress-test` (philosophical), `citation-audit` |
| `economics` | `research-lit`, `semantic-scholar`, `exa-search` | `paper-plan`, empirical analysis write-up, `paper-write` | `paper-claim-audit`, `citation-audit`, `research-review` |
| `social-sciences` | `research-lit`, `semantic-scholar`, `exa-search` | survey/interview/coding protocol, `paper-plan` | `paper-claim-audit`, `citation-audit`, ethics/methods review |
| `management` | `research-lit`, `semantic-scholar`, `exa-search` | `paper-plan`, case/empirical write-up | `paper-claim-audit`, `citation-audit`, `research-review` |
| `education` | `research-lit`, `semantic-scholar`, `exa-search` | survey/intervention protocol, `paper-plan` | `paper-claim-audit`, `citation-audit`, ethics/methods review |
| `communications` | `comm-lit-review`, `semantic-scholar`, `exa-search` | `paper-plan`, empirical/textual analysis | `paper-claim-audit`, `citation-audit`, `research-review` |

## Interdisciplinary Research

When `PRISM_PROFILE.md` lists a secondary discipline:

1. **Use primary discipline for structure and methodology**
2. **Supplement with secondary discipline's evidence standards** (e.g., a law paper with economic analysis must meet the social-science standard for its empirical part)
3. **Venue selection**: Check if the target venue accepts interdisciplinary work
4. **Literature sources**: Merge both disciplines' database lists

## Supported Discipline IDs

| ID | Name |
|----|------|
| `law` | Law / Legal Studies |
| `sports-law` | Sports Law / Sports Governance |
| `economics` | Economics / Finance |
| `social-sciences` | Social Sciences |
| `humanities` | Humanities |
| `philosophy` | Philosophy (esp. moral & political) |
| `logic` | Logic (formal & philosophical) |
| `education` | Education Research |
| `management` | Management / Business |
| `communications` | Communications / Media Studies |

## Adding New Disciplines

To add a new discipline:

1. Create `shared-references/prism-profiles/{id}.md` following the existing profile format
2. Add the discipline ID and trigger keywords to `prism-pipeline/SKILL.md`
3. Add the ID to this routing table if it needs specialist modules or a non-standard evidence gate
4. No other changes needed — downstream skills auto-discover profiles via `PRISM_PROFILE.md`
