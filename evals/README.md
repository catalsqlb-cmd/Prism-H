# Audit calibration (self-calibrating detectors)

Prism's audit skills emit a verdict per run; `tools/verify_paper_audits.sh`
checks those artifacts are **complete and fresh**. This `evals/` tree checks
the orthogonal question: **are the verdicts correct?** It does so by scoring an
audit skill's verdicts against a labeled **gold set** and gating on two rates:

- **FNR** (false-negative rate) — how often the detector *misses* a real
  problem. Target **< 0.15**. This is the dangerous one: a missed unsupported
  claim or bad citation ships.
- **FPR** (false-positive rate) — how often it flags a *clean* input. Target
  **< 0.10**. Too many false alarms train the author to ignore the audit.

## Layout

```
evals/
  gold/
    citation-audit/    *.json   labeled examples for /citation-audit
    paper-claim-audit/ *.json   labeled examples for /paper-claim-audit
    proof-checker/     *.json   labeled examples for /proof-checker
  runs/                         predictions + reports (gitignored, created per run)
```

Each gold example is one JSON file:

```json
{
  "id": "cite-wrong-locator-01",
  "audit_skill": "citation-audit",
  "gold_label": "problem",
  "category": "wrong-locator",
  "input": { "claim": "...", "citation": "...", "locator": "...", "source_excerpt": "..." },
  "rationale": "The cited page does not contain the claimed statistic."
}
```

`gold_label` is `problem` (the audit SHOULD flag it) or `clean` (should pass).

## The calibration loop

1. **Run the audit skill** on each gold example's `input`. For each, record the
   resulting verdict (PASS/WARN/FAIL/NOT_APPLICABLE/BLOCKED/ERROR) keyed by `id`
   into a predictions file:

   ```
   evals/runs/<date>/citation-audit.jsonl
   {"id": "cite-wrong-locator-01", "verdict": "FAIL"}
   {"id": "cite-supported-01", "verdict": "PASS"}
   ```

2. **Score** with the canonical harness:

   ```bash
   python3 tools/audit_calibrate.py \
     --gold-dir evals/gold/citation-audit \
     --predictions evals/runs/<date>/citation-audit.jsonl \
     --json-out evals/runs/<date>/citation-audit.report.json
   ```

   Or score all three skills at once by pointing at the parents:

   ```bash
   python3 tools/audit_calibrate.py \
     --gold-dir evals/gold \
     --predictions evals/runs/<date>/   # contains <skill>.jsonl per skill
   ```

3. **Read the verdict.** Exit code `0` = all detectors within thresholds.
   Exit `1` = at least one breached FNR or FPR → **recalibrate that skill**:
   tighten/loosen its flagging criteria in `SKILL.md`, or fix the systematic
   blind spot the breached `category` rows reveal.

## Flag mapping

A verdict counts as "flagged" iff it is in `--flag-verdicts` (default
`FAIL,BLOCKED,ERROR`). Add `WARN` if you want soft warnings to count as catches:
`--flag-verdicts FAIL,BLOCKED,ERROR,WARN`.

## Growing the gold set

The seed examples are deliberately small. Every time an audit misses a real
problem in practice (or false-alarms), add that case here as a new gold example
with the right label. The gold set becomes the regression suite that keeps the
detectors honest as the skills evolve.
