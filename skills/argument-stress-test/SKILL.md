---
name: argument-stress-test
description: Doctrinal / normative legal argument quality gate — the proof-checker analog for law and humanities. Reads a legal or theoretical argument, stress-tests each normative claim for positive-law grounding, correct rule hierarchy, doctrinal coherence, systematic case selection, and policy-vs-law confusion, then emits an audit verdict. Use when user says "审论证", "论证应力测试", "stress test my argument", "check my legal reasoning", "查教义学论证", or wants rigorous verification of a doctrinal/normative argument.
argument-hint: [path-to-draft or argument-description]
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, Agent, mcp__codex__codex, mcp__codex__codex-reply
---

# Argument Stress-Test: Doctrinal / Normative Argument Quality Gate

Systematically stress-test a legal or humanities argument the way `/proof-checker`
stress-tests a mathematical proof: decompose it into discrete normative claims,
attack each on its own terms, and emit a structured audit verdict. This is the
correctness gate the STEM side gets from `/proof-checker` and `/paper-claim-audit`
— translated to doctrinal and normative reasoning, where the unit of proof is an
*argument step* anchored to positive law or to a stated normative premise, not a
numeric result.

## Context: $ARGUMENTS

## Constants

- AUDIT_DOC: `ARGUMENT_AUDIT.md` at the project / paper directory root (cumulative human-readable log)
- AUDIT_JSON: `ARGUMENT_AUDIT.json` at the same root (machine-consumable verdict)
- REVIEWER_MODEL = `gpt-5.4` via Codex MCP, reasoning effort `xhigh` (cross-model adversarial pass)
- **REVIEWER_BACKEND = `codex`** — Default: Codex MCP (xhigh). Override with `— reviewer: oracle-pro`. See `shared-references/reviewer-routing.md`. Cross-model review is **recommended but optional**; if no reviewer backend is available, run Claude-only and mark `reviewer: "self"` in the JSON.
- MAX_REVIEW_ROUNDS = 2

## When to Use

- After `/legal-writing`, `/paper-write`, or any doctrinal/normative draft exists
- Before `/research-review` or submission, as the discipline-correctness gate for law/humanities profiles
- Standalone, when the user wants a specific argument or chapter pressure-tested

This skill is **discipline-aware**. If `PRISM_PROFILE.md` exists, read it and load
the profile's *Review Dimensions* and *Discipline-Specific Rules* — for `law` /
`sports-law` / `humanities` those rules (positive-law-first, rule-hierarchy,
functional comparison, separate law from policy preference) become the stress-test
checklist. Fall back to the generic checklist below if no profile is present.

## Protocol

### Step 0: Deterministic pre-check (cheap, model-free)

Before spending a model pass on adversarial review, run the deterministic lint
over the draft to clear the mechanical defects a model shouldn't have to babysit:

```bash
python tools/text_review.py <draft.md> --severity warning
```

It flags vague/fabricated citations (`R1-*`), over-assertion and unsupported
intensifiers (`R3-01`, `L-08`), assert-without-argue and list-without-advance
runs (`L-01`, `L-02`), quotation-without-analysis (`L-03`), unproven value-laden
premises (`L-05`), and terminology inconsistency (`T-01`). These are deterministic
proxies for the soundness defects this skill probes with a model — fixing them
first means the cross-model pass spends its budget on substance, not hygiene.
Exit code is non-zero if any `error`-level issue remains. Advisory by default;
fold surviving `L-*`/`R-*` flags into the Step 1 claim table as starting suspicions.

### Step 1: Decompose the argument into claims

Read the draft. Extract every **load-bearing normative claim** — a sentence that
asserts what the law *is*, what it *requires*, or what *ought* to be done and why.
Skip background, framing, and purely descriptive sentences. For each claim record:

- `claim_id`, `claim_text` (verbatim), `location` (section / page / line)
- `claim_type`: one of `descriptive-law` (what the law is), `interpretive` (what a
  norm means), `normative` (what ought to be), `comparative`, `empirical-support`
- `stated_authority`: the statute / case / award / rule / premise the draft cites
  *in support of this claim* (or `none` if the claim floats unsupported)

### Step 2: Stress-test each claim

Run each claim through the test battery. Each test yields pass / flag with a note.

1. **Positive-law grounding** — Is every `descriptive-law` / `interpretive` claim
   anchored to a real, current, correctly-cited authority? An unanchored "the law
   requires X" is a flag. (For `humanities`: substitute "anchored to a primary
   text / source or an explicitly stated premise".)
2. **Rule hierarchy** — Does the claim respect the hierarchy of authority (state
   law > administrative regulation > association rule > league contract > event
   rule > soft law)? Citing a federation rule to override a statute is a flag.
3. **Authority status** — Is the source correctly characterized as binding /
   persuasive / arbitral / contractual / soft-law? Treating a CAS award or a
   foreign case as if it were binding domestic precedent is a flag.
4. **Law-vs-policy separation** — Does a `normative` claim do the work of legal
   argument, or is policy desirability smuggled in as if it were legal authority?
   "X is good policy, therefore the law is X" is a flag.
5. **Inferential validity** — Does the conclusion actually follow from the cited
   authority, or is there a gap / non-sequitur / overbroad reading? This is the
   direct analog of a proof gap.
6. **Systematic selection** — For claims resting on cases / awards / examples: is
   the selection systematic, or cherry-picked? Are obvious counter-authorities or
   counterexamples ignored? Unaddressed contrary authority is a flag.
7. **Comparative validity** — For `comparative` claims: functional equivalents
   compared, or superficial jurisdiction labels? See `/comparative-law`.
8. **Internal coherence** — Does this claim contradict another claim in the same
   draft?

### Step 3: Cross-model adversarial pass (recommended)

If a reviewer backend is available, send the decomposed claims + the draft to the
reviewer (`mcp__codex__codex`, fresh thread, `xhigh`) framed as a hostile opposing
counsel / examiner: "find the weakest claim, the unsupported leap, the ignored
counter-authority." Merge reviewer-found issues into the claim table. Save the
trace per `shared-references/review-tracing.md`. Up to `MAX_REVIEW_ROUNDS`.

If no reviewer is available, skip and set `reviewer: "self"`.

### Step 4: Per-claim verdict and roll-up

Assign each claim a verdict:

- `SOUND` — anchored, valid, no flags
- `WEAK` — supported but with a fixable gap (thin authority, soft inferential leap)
- `UNSUPPORTED` — load-bearing claim with no adequate authority / premise
- `INVALID` — conclusion does not follow, or misreads / misattributes authority
- `POLICY-AS-LAW` — normative preference presented as legal authority
- `UNVERIFIABLE` — cannot assess without a source the draft does not provide

Roll up to an overall verdict:

- `PASS` — all claims SOUND (WEAK allowed only if cosmetic)
- `WARN` — one or more WEAK, no UNSUPPORTED/INVALID/POLICY-AS-LAW
- `FAIL` — any UNSUPPORTED, INVALID, or POLICY-AS-LAW on a load-bearing claim
- `NOT_APPLICABLE` — draft contains no normative/doctrinal claims
- `BLOCKED` — sources needed for verification are not provided and cannot be fetched
- `ERROR` — skill could not run to completion

### Step 5: Emit artifacts

Always write both `ARGUMENT_AUDIT.json` and append to `ARGUMENT_AUDIT.md`,
regardless of caller or outcome. Silent skip is forbidden (per
`shared-references/integration-contract.md`).

`ARGUMENT_AUDIT.json` schema:

```json
{
  "skill": "argument-stress-test",
  "date": "2026-05-29",
  "target": "paper/main.tex",
  "discipline": "sports-law",
  "reviewer": "codex:gpt-5.4",
  "overall_verdict": "WARN",
  "counts": {"SOUND": 14, "WEAK": 3, "UNSUPPORTED": 0, "INVALID": 0, "POLICY-AS-LAW": 0, "UNVERIFIABLE": 1},
  "claims": [
    {
      "claim_id": "C1",
      "claim_text": "赛事转播权可作为一种独立的财产权益受反不正当竞争法保护。",
      "location": "§3.2",
      "claim_type": "interpretive",
      "claim_verdict": "WEAK",
      "stated_authority": "《反不正当竞争法》第2条",
      "tests_flagged": ["positive-law-grounding"],
      "note": "依赖一般条款而未援引更具体的请求权基础或主流判例，论证偏薄。",
      "fix_hint": "补充'新浪诉凤凰网'等数据/转播相关判例与学说支撑，或明确请求权基础。"
    }
  ]
}
```

### Step 6: Print summary

```
📋 Argument Stress-Test Complete  (discipline: sports-law)

  Claims tested:     18
  ✅ SOUND:          14
  ⚠️ WEAK:            3
  ❌ UNSUPPORTED:     0
  ❌ INVALID:         0
  ❌ POLICY-AS-LAW:   0
  ❓ UNVERIFIABLE:    1

  Overall: ⚠️ WARN  — 3 claims need stronger authority before submission.

  See ARGUMENT_AUDIT.md for the per-claim breakdown and fix hints.
```

## Advisory, Never Silently Blocking

Same posture as the other audits: `PASS` → continue; `WARN` → flag for fix;
`FAIL` → alert and do not mark the draft submission-ready. The skill never edits
the draft itself — it reports. Fixing is the author's (or `/legal-writing`'s) job.

## Self-calibration

This audit's detector quality is measured against gold-labeled arguments.
Gold sets live in `evals/gold/argument-stress-test/` (examples labeled
`problem` / `clean` with a `category`). To calibrate:

```
python3 tools/audit_calibrate.py \
  --gold-dir evals/gold/argument-stress-test/ \
  --predictions evals/runs/<date>/argument-stress-test.jsonl \
  --flag-verdicts FAIL,UNSUPPORTED,INVALID,POLICY-AS-LAW \
  --max-fnr 0.15 --max-fpr 0.10
```

Exit 1 means the detector drifted (too many missed problems or false alarms) and
the protocol needs tightening. This is a dev-time gate, not a per-paper gate.

## Key Rules

- **One claim, one verdict.** Never roll WEAK and FAIL into a vague "needs work."
- **Anchored, not vibes.** Every flag cites which test failed and why; every fix
  hint names a concrete authority or move, not "strengthen this."
- **Positive law before preference.** The single most common law failure is
  `POLICY-AS-LAW`; treat it as seriously as a proof gap.
- **Cross-model when possible.** Self-review misses the leaps the author is
  blind to. Use the reviewer backend if it exists.
- **Always emit the artifact.** Even `NOT_APPLICABLE` and `BLOCKED` are written
  to JSON, so downstream gates and `/research-review` can see the result.
