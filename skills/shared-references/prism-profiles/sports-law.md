# Discipline Profile: Sports Law / Sports Governance

## ID
`sports-law`

## Research Methodology

- **Primary methods**: Doctrinal analysis, sports-governance analysis, comparative sports law, CAS / arbitration award analysis, law and economics, regulatory policy analysis, institutional analysis
- **Evidence types**: Sports statutes and regulations, judicial cases, CAS awards, league and federation rules, WADA / IOC / FIFA / UEFA / NCAA rules, event organizer documents, broadcasting and data-rights contracts, policy documents, scholarly commentary, economic and governance data
- **Validation standards**: Positive-law grounding, correct rule hierarchy, systematic case / award selection, functional comparative method, doctrinal coherence, practical feasibility for Chinese sports governance, accurate citation of sports organization rules
- **Claim structure**: "Sports governance rule X creates legal problem Y under normative framework Z; reform or interpretation W is justified by positive law, comparative governance evidence, and policy/economic rationale."

## Sub-fields and Methods

| Sub-field | Primary Method | Key Evidence |
|-----------|----------------|--------------|
| Event broadcasting rights | Doctrinal + law and economics | Sports Law, Civil Code, Copyright Law, Anti-Unfair Competition Law, league rules, broadcasting contracts |
| Event data and commercial control | Doctrinal + policy + economic analysis | Event organizer rules, data contracts, database / unfair competition cases, comparative sports-league practice |
| Athlete rights and discipline | Doctrinal + arbitration analysis | Sports Law, federation disciplinary rules, CAS awards, athlete agreements |
| Anti-doping | Regulatory + comparative analysis | WADA Code, CHINADA rules, CAS awards, administrative law materials |
| Sports organization governance | Institutional + comparative law | IOC / FIFA / federation statutes, association law, governance codes |
| Professional league regulation | Law and economics + comparative law | League constitutions, salary / transfer rules, antitrust or competition-law cases |
| Youth and reserve talent systems | Policy + administrative law | Education/sports policy, local regulations, school-sport documents |

## Literature Sources

| Priority | Database / Source | Coverage |
|----------|-------------------|----------|
| 1 | CNKI (中国知网) | Chinese sports law, sports policy, legal journals, dissertations |
| 2 | PKULaw / Westlaw China (北大法宝) | Chinese statutes, cases, judicial interpretations |
| 3 | CAS Awards Database / sports arbitration sources | CAS awards and arbitration patterns |
| 4 | IOC / WADA / FIFA / UEFA / NCAA official rules | Sports organization norms and governance documents |
| 5 | HeinOnline / Westlaw / LexisNexis | Common law sports cases and law reviews |
| 6 | SSRN / Google Scholar | Sports-law working papers and interdisciplinary work |
| 7 | SportDiscus / Web of Science | Sports science and sport management materials |
| 8 | Local paper library / Obsidian / Zotero | User-curated sports-law materials and notes |

## Venue Tiers

| Tier | Chinese Venues | International Venues |
|------|----------------|----------------------|
| A | 中国社会科学, 法学研究, 中国法学, 体育科学 | International Sports Law Journal, Marquette Sports Law Review |
| B | 中外法学, 法学家, 法商研究, 比较法研究, 环球法律评论, 体育与科学 | Journal of Legal Aspects of Sport, Entertainment and Sports Law Journal |
| C | 法学评论, 政法论坛, 体育学刊, 武汉体育学院学报, 北京体育大学学报 | Sports Law eJournal / SSRN, specialty sports governance journals |
| Dissertation | CNKI dissertations | ProQuest dissertations |

## Paper Structure

### Sports Law Doctrinal / Policy Paper
```
1. Introduction / Problem Statement (引言 / 问题的提出) — 1-2 pages
2. Sports Governance Background (体育治理背景) — 2-3 pages
3. Positive-Law and Rule-Hierarchy Analysis (现行法与规则层级分析) — 3-4 pages
4. Case / Arbitration / Practice Analysis (案例、仲裁与实践) — 2-4 pages
5. Comparative Sports Law or Institutional Comparison (比较体育法 / 制度比较) — 2-3 pages
6. Normative Evaluation and Reform Proposal (规范评价与制度建议) — 2-3 pages
7. Conclusion — 1 page
```

### Sports Law and Economics Paper
```
1. Introduction / Problem Statement — 1-2 pages
2. Institutional Background — 2-3 pages
3. Legal Framework and Literature Review — 2-3 pages
4. Economic / Governance Model or Empirical Strategy — 3-4 pages
5. Application to Sports Governance Practice — 3-4 pages
6. Policy Implications and Legal Reform — 2-3 pages
7. Conclusion — 1 page
```

### Citation Style
- Chinese legal journals: footnote style (脚注), GB/T 7714, or target journal style — **详见 `../citation-cn-footnote.md`**
- 体育科学等体育类期刊: 尾注（参考文献表），顺序编码制 GB/T 7714-2015 — 详见 `citation-cn-footnote.md` 期刊速查
- CAS 裁决、IOC/FIFA/WADA 规则: 专用引用格式见 `citation-cn-footnote.md` 体育治理规则引用 & CAS仲裁裁决引用
- International sports law: Bluebook / OSCOLA / journal-specific style
- Mixed policy / management work: APA author-date if the venue requires it
- **中文论文默认**: 法学类期刊用脚注，体育学类期刊用尾注；具体格式以目标期刊投稿须知为准

## Review Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Problem Significance | 15% | Is the sports-law problem theoretically meaningful and practically important? |
| Positive-Law Grounding | 20% | Are statutes, regulations, and sports organization rules correctly identified and hierarchized? |
| Sports Governance Fit | 15% | Does the argument understand how sports bodies, leagues, clubs, athletes, and event organizers actually operate? |
| Argument Quality | 20% | Is the normative reasoning coherent, precise, and not merely policy preference? |
| Case / Award Coverage | 10% | Are cases, CAS awards, and disciplinary decisions selected systematically rather than cherry-picked? |
| Comparative Depth | 10% | Does comparative analysis use functional equivalents and avoid superficial jurisdiction lists? |
| Citation Integrity | 5% | Are legal, arbitral, and organization-rule citations accurate and claim-matched? |
| Writing Quality | 5% | Is the paper structured, disciplined, and clear? |

## Recommended Pipeline Modules

| Stage | Modules | Use |
|-------|---------|-----|
| Literature and mapping | `research-lit`, `semantic-scholar`, `exa-search`, `research-refine` | Build the legal/source landscape; query CNKI/北大法宝/CAS sources and synthesize |
| Framework execution | `statute-case-mapper`, `comparative-law`, `paper-plan` | Map claims→实证法/案例/CAS, run functional comparison, plan the argument |
| Review and gates | `argument-stress-test`, `citation-audit`, `research-review` | Stress-test doctrinal soundness, verify legal citations (L3), get external review |
| Writing and defense | `legal-writing`, `rebuttal` | Draft legal scholarship & dissertation outlines (`legal-writing outline`); answer defense/reviewer comments |

## Local Wiki Defaults

- **External wiki root**: declared by the user (env `PRISM_WIKI_ROOT`, a `Local Wiki`/`知识库` entry in `CLAUDE.md`, or a command override). See `../local-wiki-link.md`. Prism ships no built-in personal path.
- **Query first**: Before web search, read `wiki/index.md` and run `scripts/query_wiki.py` for the topic.
- **Write-back targets**: Durable analyses go to `wiki/memos/`; source summaries to `wiki/sources/`; stable concepts/cases/statutes to their matching folders.
- **Maintenance rules**: If `AGENTS.md` exists, follow it before writing. In this wiki, `raw/` is source material and must not be modified.

## Discipline-Specific Rules

- **Positive law first**: Every normative claim must be anchored to statutes, cases, judicial interpretations, or sports organization rules.
- **Track rule hierarchy**: Distinguish state law, administrative regulations, association rules, league contracts, event rules, and private ordering.
- **Separate legal argument from governance preference**: Policy desirability is not enough without legal authority and institutional feasibility.
- **Treat CAS and federation materials carefully**: Identify whether a source is binding, persuasive, arbitral, contractual, or soft law.
- **Use functional comparison**: Compare institutional roles and enforcement mechanisms, not just foreign labels.
- **China-facing conclusion**: For Chinese scholarship, explain how the proposal fits China's sports law, sports governance, and judicial/administrative practice.
- **Citation integrity is mandatory**: Legal and sports-governance sources must be real, current, and matched to the exact proposition being supported.
