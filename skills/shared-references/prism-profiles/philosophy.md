# Discipline Profile: Philosophy (emphasis on Moral & Political Philosophy)

## ID
`philosophy`

## Research Methodology

- **Primary methods**: Conceptual analysis, reflective equilibrium (wide/narrow), thought experiments and intuition pumps, argument reconstruction and validity assessment, counterexample method, transcendental / regress arguments, genealogy, ordinary-language analysis, formal modeling where apt (deontic / modal logic, decision & game theory for ethics)
- **Normative frameworks** (moral/political): consequentialism, deontology (Kantian), virtue ethics, contractualism/contractarianism (Rawls, Scanlon), capabilities approach, natural law; for political philosophy: liberalism, republicanism, libertarianism, communitarianism, theories of justice/rights/legitimacy/authority
- **Evidence types**: Primary texts (treatises, articles), considered judgments / intuitions, counterexamples, formal proofs of validity, empirical findings *imported* as premises (experimental philosophy, social science), the dialectical record of objections and replies
- **Validation standards**: Validity and soundness of arguments, charity in reconstruction, responsiveness to the strongest objections, reflective-equilibrium coherence between principles and considered judgments, conceptual clarity and non-equivocation, originality of the thesis within the live debate
- **Claim structure**: "Thesis T about concept/value C is defended by argument A from premises P1…Pn; the leading objections O1…Om fail because R; therefore we should revise our view of C / accept normative conclusion N." Distinguish **descriptive/meta** claims (what a position is, what a concept means) from **first-order normative** claims (what we ought to do/value).

## Sub-fields and Methods

| Sub-field | Primary Method | Key Materials |
|-----------|----------------|---------------|
| Normative ethics | Reflective equilibrium, thought experiments, framework comparison | Primary ethical theory texts, canonical cases (trolley, etc.) |
| Metaethics | Conceptual/semantic analysis, argument reconstruction | Realism/anti-realism, expressivism, constructivism literature |
| Political philosophy | Theory construction, reflective equilibrium, conceptual analysis | Justice/rights/legitimacy/authority/equality/liberty literature |
| Applied ethics | Case analysis + principle application | Domain facts (bioethics, tech ethics, sports ethics) + normative frameworks |
| Logic / philosophy of logic | Formal proof + conceptual analysis | See the `logic` profile; cross-link for formal results |
| Epistemology / metaphysics / mind | Conceptual analysis, thought experiments, argument mapping | Canonical problems and the contemporary dialectic |

## Literature Sources

| Priority | Database / Source | Coverage |
|----------|-------------------|----------|
| 1 | PhilPapers | Philosophy-specific index, the canonical first stop |
| 2 | Stanford Encyclopedia of Philosophy (SEP) | Authoritative state-of-debate surveys; use to map the dialectic, cite the primary sources it points to |
| 3 | JSTOR | Historical and foundational scholarship |
| 4 | Project MUSE | Humanities journals |
| 5 | CNKI (中国知网) | Chinese philosophy journals |
| 6 | Google Scholar | Broad coverage, citation tracing |
| 7 | PhilArchive | Open-access preprints |
| 8 | Local paper library / Obsidian / Zotero | User-curated notes |

## Venue Tiers

| Tier | General / Metaethics | Ethics & Political Philosophy | Chinese |
|------|----------------------|-------------------------------|---------|
| A | Journal of Philosophy, Mind, Philosophical Review, Noûs | Ethics, Philosophy & Public Affairs | 哲学研究, 中国社会科学 |
| B | Australasian J. of Philosophy, Philosophy and Phenomenological Research, Synthese | Journal of Political Philosophy, Journal of Moral Philosophy, Utilitas, Politics Philosophy & Economics | 哲学动态, 道德与文明, 伦理学研究 |
| C | Erkenntnis, Philosophical Studies, Analysis | Journal of Applied Philosophy, Res Publica, Social Theory and Practice | 世界哲学, 现代哲学, 中国哲学史 |
| Dissertation | ProQuest, PhilArchive | — | CNKI dissertations |

## Paper Structure

### Normative / Argumentative Paper (the default)
```
1. Introduction — the question, the thesis, why it matters (1-2 pages)
2. The Dialectic — the live debate and the position being challenged (2-3 pages)
3. The Argument — premises and the inference to the thesis (3-5 pages)
4. Objections and Replies — the strongest objections, answered (3-4 pages)
5. Implications / wider significance (1-2 pages)
6. Conclusion (1 page)
```

### Applied / Moral-Political Analysis Paper
```
1. Introduction — the practical problem and normative question (1-2 pages)
2. The relevant facts / institutional background (1-2 pages)
3. Normative framework(s) and why this one (2-3 pages)
4. Application — what the framework implies for the case (3-4 pages)
5. Competing frameworks / objections and replies (2-3 pages)
6. Conclusion and practical upshot (1 page)
```

### Citation Style
- Chicago Manual of Style (Notes and Bibliography) — most common in philosophy
- Author–date (Chicago/APA) accepted by many analytic journals; match the target journal
- Chinese journals: GB/T 7714 or journal-specific footnote style — see `../citation-cn-footnote.md`
- Substantive footnotes are expected: qualifications, secondary objections, and scholarly dialogue belong there.

## Review Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Thesis Originality | 20% | Is the thesis a genuine, identifiable contribution to a live debate? |
| Argument Validity & Soundness | 25% | Do the conclusions follow? Are the premises defensible and non-question-begging? |
| Engagement with Objections | 20% | Are the *strongest* objections confronted, not strawmen? |
| Conceptual Clarity | 15% | Are key concepts defined and used without equivocation? |
| Reflective-Equilibrium Coherence | 10% | Do principles and considered judgments cohere; are bullets bitten openly? |
| Writing Quality | 10% | Is the prose precise, well-structured, and economical? |

## Recommended Pipeline Modules

| Stage | Modules | Use |
|-------|---------|-----|
| Literature and mapping | `research-lit`, `semantic-scholar`, `research-refine` | Map the dialectic via PhilPapers/SEP; locate the position being challenged |
| Framework execution | `paper-plan`, `comparative-law` (as functional framework comparison), `formula-derivation`/`proof-checker` (only for formal sub-arguments) | Plan the argument; compare normative frameworks functionally; verify any formal step |
| Review and gates | `argument-stress-test`, `citation-audit`, `research-review` | Stress-test validity / objection-coverage / concept clarity; verify citations (L3); external review |
| Writing | `legal-writing` (humanities mode) | Draft argumentative / applied-ethics papers and dissertation outlines |

## Local Wiki Defaults

- **Query first**: If an external wiki or `research-wiki/` exists, read `wiki/index.md` and run `query_wiki.py` before web search.
- **Write-back targets**: Durable argument maps and objection logs → `wiki/memos/`; primary-text summaries → `wiki/sources/`; stable concepts/positions → their matching folders.
- **Maintenance**: If `AGENTS.md`/`CLAUDE.md` exists, follow it. Never modify `raw/`.

## Discipline-Specific Rules

- **Validity before rhetoric**: Every load-bearing argument must be reconstructable as premises → conclusion; `/argument-stress-test` treats an invalid inference like a proof gap.
- **Charity and the strongest objection**: Reconstruct opposing views at their best; answering a strawman is a failure, not a win.
- **Reflective equilibrium, transparently**: When a principle clashes with a considered judgment, say which you revise and why — do not hide the bullet you bite.
- **Define your terms**: Equivocation is the most common defeater; fix the sense of each key concept and hold it fixed.
- **Separate meta from first-order**: Keep "what this position *is* / what the concept *means*" distinct from "what we *ought* to do" — the audit tags these as different claim types.
- **Intuitions are evidence, not proof**: Thought-experiment verdicts are defeasible data points; do not treat a single intuition as decisive.
- **Import empirical premises honestly**: If an argument leans on empirical claims (x-phi, social science), they must meet that field's evidentiary standard and be cited.
- **Normative commitments are explicit**: State your framework and value commitments; philosophy is openly normative.
