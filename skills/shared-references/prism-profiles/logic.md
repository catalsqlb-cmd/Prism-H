# Discipline Profile: Logic (Formal & Philosophical)

## ID
`logic`

## Research Methodology

- **Primary methods**: Formal proof (natural deduction, sequent calculus, axiomatic), model-theoretic argument (soundness/completeness, (un)definability, (in)expressibility), proof-theoretic analysis (cut-elimination, normalization, consistency strength), computability/complexity results, conceptual analysis of logical notions (consequence, truth, validity, modality), formal-semantics construction
- **Two modes** (route differently):
  - **Formal logic** — results are theorems: a proof, a counter-model, a (non)conservativity or (in)completeness result. Verified like mathematics.
  - **Philosophical logic / philosophy of logic** — claims about *which* logic is correct, what logical consequence *is*, paradox diagnosis, the meaning of connectives. Verified as philosophical arguments.
- **Evidence types**: Proofs, counter-models, formal systems and their metatheory, intuitions about validity and paradox, the dialectical record of objections
- **Validation standards**: Formal correctness (every inference licensed by a stated rule; no gap), correct metatheoretic claims (soundness/completeness actually established), faithful formalization (the formal system tracks the target informal notion), responsiveness to objections (philosophical mode)
- **Claim structure**: Formal — "In system S, φ holds, proved by P / refuted by model M." Philosophical — "Logic L is the correct logic for domain D (or: consequence relation ⊨ has property X) because A; objections O fail because R."

## Sub-fields and Methods

| Sub-field | Primary Method | Verified by |
|-----------|----------------|-------------|
| Classical & non-classical logic (intuitionistic, relevant, paraconsistent, many-valued) | Proof + model theory | `proof-checker` |
| Modal / temporal / deontic / epistemic logic | Kripke semantics, completeness proofs | `proof-checker` |
| Proof theory | Cut-elimination, ordinal analysis, consistency strength | `proof-checker` |
| Model theory | Definability, categoricity, preservation theorems | `proof-checker` |
| Philosophy of logic | Conceptual analysis, argument reconstruction | `argument-stress-test` |
| Philosophical logic (vagueness, paradox, conditionals, truth) | Formalization + philosophical argument | both (formalize, then argue) |

## Literature Sources

| Priority | Database / Source | Coverage |
|----------|-------------------|----------|
| 1 | PhilPapers (Logic & Philosophy of Logic) | Philosophical logic index |
| 2 | Stanford Encyclopedia of Philosophy (SEP) | State-of-debate surveys for logical topics |
| 3 | zbMATH / MathSciNet | Formal-logic and mathematical-logic results |
| 4 | arXiv (math.LO, cs.LO) | Preprints in mathematical & computational logic |
| 5 | JSTOR | Foundational papers (e.g., JSL back catalog) |
| 6 | Google Scholar | Citation tracing |
| 7 | CNKI (中国知网) | Chinese logic journals |

## Venue Tiers

| Tier | Formal / Mathematical Logic | Philosophical Logic |
|------|-----------------------------|----------------------|
| A | Journal of Symbolic Logic, Annals of Pure and Applied Logic | Journal of Philosophical Logic, Review of Symbolic Logic, Mind |
| B | Notre Dame J. of Formal Logic, Studia Logica, Archive for Mathematical Logic | Synthese, Analysis, Erkenntnis |
| C | Logic Journal of the IGPL, Journal of Logic and Computation | Logique et Analyse, Australasian J. of Logic |
| Chinese | 逻辑学研究 (Studies in Logic), 哲学研究 (logic articles) | 哲学研究, 哲学动态 |

## Paper Structure

### Formal Result Paper
```
1. Introduction — the question and the result stated informally (1-2 pages)
2. Preliminaries — language, system S, semantics, prior results (2-3 pages)
3. Main results — theorems with full proofs (4-8 pages)
4. Corollaries / scope / limits (1-2 pages)
5. Related work and significance (1-2 pages)
6. Conclusion and open problems (1 page)
```

### Philosophy-of-Logic Paper
```
1. Introduction — the question, the thesis (1-2 pages)
2. The debate / position being challenged (2-3 pages)
3. Formal setup (if any) — the systems in play (1-3 pages)
4. The argument (3-5 pages)
5. Objections and replies (3-4 pages)
6. Conclusion (1 page)
```

### Citation Style
- Formal logic: numbered references, often AMS/journal-specific (LaTeX, theorem environments expected)
- Philosophical logic: Chicago/author-date or journal-specific; substantive footnotes expected
- Chinese journals: GB/T 7714 or journal-specific — see `../citation-cn-footnote.md`

## Review Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Formal Correctness | 30% | Are proofs gap-free and metatheoretic claims (soundness/completeness) actually established? |
| Faithful Formalization | 20% | Does the formal system genuinely capture the target informal notion? |
| Significance / Novelty | 20% | Is the result or thesis a genuine contribution? |
| Argument Quality (phil. mode) | 15% | Is the philosophical reasoning valid and objection-responsive? |
| Clarity & Rigor of Presentation | 10% | Definitions precise, notation consistent, lemmas stated cleanly? |
| Writing Quality | 5% | Is the exposition readable and well-organized? |

## Recommended Pipeline Modules

| Stage | Modules | Use |
|-------|---------|-----|
| Literature and mapping | `research-lit`, `semantic-scholar`, `alphaxiv` | Locate exact prior systems, theorems, and proof techniques |
| Framework execution | `formula-derivation`, `proof-writer` | Stabilize notation/systems; draft formal proof packages |
| Review and gates (formal) | `proof-checker`, `citation-audit` | Verify proofs gap-free before claims are promoted; verify citations |
| Review and gates (philosophical) | `argument-stress-test`, `research-review` | Stress-test philosophical arguments about logic; external review |
| Writing | `legal-writing` (humanities mode) for philosophy-of-logic prose; `paper-write` for formal-results papers | Draft the paper |

## Local Wiki Defaults

- **Query first**: If an external wiki or `research-wiki/` exists, read `wiki/index.md` and run `query_wiki.py` before web search.
- **Write-back targets**: Stable systems/theorems → `wiki/concepts/`; proof sketches and objection logs → `wiki/memos/`; source summaries → `wiki/sources/`. Never modify `raw/`.

## Discipline-Specific Rules

- **Route by mode**: A formal result is verified by `/proof-checker` (it is mathematics); a philosophy-of-logic thesis is verified by `/argument-stress-test`. Mixed papers do both — formalize, then argue.
- **No proof gaps**: Every inference must be licensed by a stated rule. A hand-waved step is a defect, exactly as in `/proof-checker`.
- **Metatheory must be earned**: Do not assert soundness/completeness/decidability without the proof; these are the most common over-claims.
- **Formalization is a claim**: That the formal system captures the informal notion is itself defeasible and must be argued, not assumed.
- **Distinguish object- and meta-language**: Conflation here is the classic source of paradox and error; keep them separate.
- **Cross-link philosophy**: For normative/conceptual disputes (which logic is correct, paradox diagnosis), defer to the `philosophy` profile's argument standards.
