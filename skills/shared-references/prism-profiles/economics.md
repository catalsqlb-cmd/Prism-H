# Discipline Profile: Economics / Finance

## ID
`economics`

## Research Methodology

- **Primary methods**: Econometric analysis, theoretical modeling (game theory, mechanism design), randomized controlled trials (RCT), natural experiments, difference-in-differences (DID), instrumental variables (IV), regression discontinuity (RD), structural estimation
- **Evidence types**: Panel data regression, causal identification, statistical significance tests, robustness checks, placebo tests, heterogeneity analysis, simulation results, calibration
- **Validation standards**: Causal identification strategy must be clearly stated and defended, standard errors must be correctly specified (clustered, robust, etc.), robustness to alternative specifications, falsification tests, external validity discussion
- **Claim structure**: "X causes Y, identified via strategy Z" or "Model A predicts outcome B, validated by empirical pattern C"

## Literature Sources

| Priority | Database | Coverage |
|----------|----------|----------|
| 1 | NBER Working Papers | Leading economics preprints |
| 2 | SSRN (Economics Network) | Working papers |
| 3 | EconLit / AEA | Published economics literature |
| 4 | Google Scholar | Broad coverage |
| 5 | CNKI (中国知网) | Chinese economics journals |
| 6 | IDEAS/RePEc | Working papers, citation tracking |
| 7 | JSTOR | Historical economics scholarship |

## Venue Tiers

| Tier | Venues |
|------|--------|
| Top 5 | American Economic Review (AER), Econometrica, Journal of Political Economy (JPE), Quarterly Journal of Economics (QJE), Review of Economic Studies (RES) |
| A (Field Top) | Journal of Finance, Journal of Financial Economics, Review of Financial Studies, Journal of Monetary Economics, Journal of Public Economics, Journal of Labor Economics, Journal of International Economics, Journal of Development Economics, AEJ series |
| B (Strong) | Journal of Law and Economics, Economic Journal, International Economic Review, Journal of Economic Theory, Games and Economic Behavior, RAND Journal of Economics |
| Chinese A | 经济研究, 管理世界, 中国社会科学, 经济学(季刊) |
| Chinese B | 世界经济, 金融研究, 中国工业经济, 经济科学, 南开经济研究 |

## Paper Structure

### Empirical Economics Paper
```
1. Introduction (2-3 pages) — including contribution statement and preview of results
2. Institutional Background / Context (1-2 pages)
3. Data (1-2 pages)
4. Empirical Strategy / Identification (2-3 pages)
5. Results (3-4 pages) — main results + mechanisms
6. Robustness and Extensions (2-3 pages)
7. Conclusion (1 page)
```

### Theoretical Economics Paper
```
1. Introduction (2-3 pages)
2. Related Literature (1-2 pages)
3. Model Setup (2-3 pages)
4. Equilibrium Analysis / Main Results (3-4 pages)
5. Comparative Statics / Welfare Analysis (2-3 pages)
6. Extensions / Discussion (1-2 pages)
7. Conclusion (1 page)
```

### Citation Style
- Author-date (APA variant used by most economics journals)
- `\citep{}` / `\citet{}` in LaTeX (natbib)
- Full names in text for landmark papers: "as shown by Acemoglu, Johnson, and Robinson (2001)"

## Review Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Research Question | 15% | Is the question economically important and well-motivated? |
| Identification Strategy | 30% | Is the causal identification credible? Are threats to validity addressed? |
| Data Quality | 10% | Is the data appropriate, well-documented, and sufficient? |
| Technical Execution | 20% | Are the econometric methods correctly applied? |
| Contribution to Literature | 15% | Does this advance our understanding beyond existing work? |
| Policy Relevance | 5% | Are the policy implications clearly drawn? |
| Writing Clarity | 5% | Is the paper well-organized and clearly written? |

## Discipline-Specific Rules

- **Identification is king**: The causal identification strategy must be stated clearly in the introduction and defended rigorously
- **Standard errors matter**: Always report correctly clustered standard errors; discuss why clustering level is appropriate
- **Robustness is not optional**: Every main result needs at least 3-4 robustness checks (alternative specifications, sample restrictions, placebo tests)
- **Heterogeneity analysis**: Show whether effects vary across subgroups — this is where policy implications come from
- **External validity**: Discuss whether findings generalize beyond the specific context studied
- **Tables over figures**: Economics convention: regression tables are primary evidence; figures supplement
- **Preview results in the introduction**: Economics papers typically state main findings in the introduction
- **Related work is short**: Unlike ML papers, economics papers keep literature review brief and focused on positioning
