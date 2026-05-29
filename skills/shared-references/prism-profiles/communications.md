# Discipline Profile: Communications / Electrical Engineering

## ID
`communications`

## Research Methodology

- **Primary methods**: System simulation (Monte Carlo, ray-tracing), mathematical modeling (information theory, optimization), protocol design, testbed measurement, network simulation (ns-3, MATLAB), analytical derivation, standards-based evaluation
- **Evidence types**: BER/BLER curves, throughput measurements, spectral efficiency, latency distributions, convergence proofs, simulation vs analytical comparisons, testbed measurements, complexity analysis (FLOPS, latency)
- **Validation standards**: Simulation under standardized channel models (3GPP, ITU), comparison against theoretical bounds, multi-scenario evaluation (SNR sweep, mobility, load), reproducible configurations, complexity-performance tradeoff analysis
- **Claim structure**: "Proposed scheme X achieves Y% throughput gain over baseline Z under channel model W" or "Algorithm A converges in O(N) iterations with guaranteed performance bound B"

## Literature Sources

| Priority | Database | Coverage |
|----------|----------|----------|
| 1 | IEEE Xplore | Primary source for EE/communications |
| 2 | arXiv (cs.IT, cs.NI, eess.SP) | Preprints |
| 3 | Semantic Scholar | Citation metadata, venue papers |
| 4 | ACM Digital Library | Networking (SIGCOMM, MobiCom) |
| 5 | ScienceDirect (Elsevier) | Computer Networks, Signal Processing |
| 6 | Google Scholar | Broad coverage |
| 7 | CNKI (中国知网) | Chinese EE journals |

## Venue Tiers

| Tier | Journals | Conferences |
|------|----------|-------------|
| A (Top) | IEEE JSAC, IEEE/ACM ToN, IEEE TWC, IEEE TCOM, IEEE TSP | ACM SIGCOMM, NSDI, MobiCom, CoNEXT, IEEE INFOCOM |
| B (Strong) | IEEE TVT, IEEE WCL, IEEE CL, Computer Networks | IEEE ICC, GLOBECOM, WCNC, PIMRC, MobiHoc |
| C (Broad) | Other IEEE/Elsevier/ACM venues | IEEE VTC, IEEE SPAWC |
| Chinese | 通信学报, 电子与信息学报, 电子学报 | |

## Paper Structure

### System/Algorithm Paper
```
1. Introduction (1-1.5 pages)
2. System Model (1-1.5 pages) — channel model, signal model, assumptions
3. Proposed Method/Algorithm (2-3 pages) — design, derivation, complexity analysis
4. Simulation Setup and Results (2-3 pages) — scenarios, baselines, performance curves
5. Conclusion (0.5 page)
```

### Theory Paper
```
1. Introduction (1-1.5 pages)
2. System Model and Preliminaries (1-1.5 pages)
3. Main Results (2-3 pages) — theorems, proofs
4. Numerical Examples (1-1.5 pages)
5. Conclusion (0.5 page)
```

### Citation Style
- IEEE style: numeric `[1]`, `\cite{}`

## Review Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Problem Significance | 15% | Is the communication problem practically relevant? |
| Technical Novelty | 25% | Is there a non-trivial algorithmic or theoretical contribution? |
| Analytical Rigor | 20% | Are derivations correct? Are assumptions clearly stated? |
| Simulation Quality | 20% | Are simulations under standard models? Enough scenarios? |
| Practical Feasibility | 10% | Can this be implemented in real systems? Complexity acceptable? |
| Presentation | 10% | Are system model and results clearly presented? |

## Discipline-Specific Rules

- **System model must be explicit**: Define channel model, signal model, noise model, and all assumptions upfront
- **Complexity analysis required**: Every algorithm needs computational complexity analysis
- **Standard channel models**: Use 3GPP/ITU channel models, not ad-hoc channel assumptions
- **SNR sweep is mandatory**: Show performance across a range of SNR values
- **Comparison against bounds**: Compare proposed scheme against theoretical bounds (Shannon, Cramer-Rao, etc.) when applicable
- **Separate PHY from higher layers**: Be clear about which layer your contribution operates at
- **Notation consistency**: Follow IEEE notation conventions (bold for vectors/matrices, calligraphic for sets)
