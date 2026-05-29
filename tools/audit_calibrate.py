#!/usr/bin/env python3
"""audit_calibrate.py — measure an audit detector's FNR/FPR against a gold set.

Prism's audit skills (proof-checker, paper-claim-audit, citation-audit) emit a
verdict per run, and `verify_paper_audits.sh` checks those artifacts are
*complete and fresh* — but nothing checks whether the verdicts are *correct*.
This harness closes that loop: run an audit skill over a labeled gold set, then
score the verdicts to estimate how often the detector misses a real problem
(false-negative rate) or flags a clean input (false-positive rate).

If FNR or FPR exceeds threshold, the detector needs recalibration (tighten or
loosen the skill's flagging criteria, or fix a systematic blind spot).

## Files

Gold example (one JSON per file under `evals/gold/<audit-skill>/`):
    {
      "id": "cite-wrong-locator-01",
      "audit_skill": "citation-audit",
      "gold_label": "problem" | "clean",
      "category": "wrong-locator",          # free-form grouping
      "input": { ... material the skill audits ... },
      "rationale": "why this is a problem / clean"
    }

Predictions (JSONL; one line per scored example):
    {"id": "cite-wrong-locator-01", "verdict": "FAIL"}

Produce predictions by running the audit skill on each gold example's `input`
and recording the resulting verdict keyed by `id`.

## Scoring

A verdict counts as "flagged" (detector thinks there's a problem) iff it is in
FLAG_VERDICTS (default: FAIL, BLOCKED, ERROR). PASS / NOT_APPLICABLE / WARN are
"clean". `--flag-verdicts` overrides the set (e.g. include WARN).

    gold=problem, flagged      → TP
    gold=problem, not flagged  → FN   (missed a real problem)
    gold=clean,   flagged      → FP   (false alarm)
    gold=clean,   not flagged  → TN

    FNR = FN / (TP + FN)        # miss rate — the dangerous one
    FPR = FP / (FP + TN)        # false-alarm rate — the annoying one

## Usage

    python3 audit_calibrate.py \
        --gold-dir evals/gold/citation-audit \
        --predictions evals/runs/2026-05-29/citation-audit.jsonl \
        [--max-fnr 0.15] [--max-fpr 0.10] \
        [--flag-verdicts FAIL,BLOCKED,ERROR] \
        [--json-out evals/runs/2026-05-29/citation-audit.report.json]

Pass a parent dir to --gold-dir to score every `<skill>/` subdir at once; give
--predictions a directory of `<skill>.jsonl` files in that case.

## Exit codes
    0  all scored detectors within thresholds
    1  at least one detector exceeds FNR or FPR threshold
    2  bad arguments / unscorable (e.g. no predictions matched)
"""

import argparse
import json
import os
import sys

DEFAULT_FLAG_VERDICTS = {"FAIL", "BLOCKED", "ERROR"}
ALL_VERDICTS = {"PASS", "WARN", "FAIL", "NOT_APPLICABLE", "BLOCKED", "ERROR"}


def load_gold(gold_dir):
    """Return {skill: [gold_example, ...]} for a skill dir or a parent of skill dirs."""
    gold_dir = os.path.abspath(os.path.expanduser(gold_dir))
    if not os.path.isdir(gold_dir):
        die(f"gold dir not found: {gold_dir}")

    def load_skill_dir(d, skill_hint):
        out = []
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".json"):
                continue
            path = os.path.join(d, fn)
            try:
                with open(path, encoding="utf-8") as fh:
                    ex = json.load(fh)
            except (OSError, ValueError) as e:
                die(f"cannot parse gold example {path}: {e}")
            for k in ("id", "gold_label"):
                if k not in ex:
                    die(f"gold example {path} missing required field '{k}'")
            if ex["gold_label"] not in ("problem", "clean"):
                die(f"gold example {path} gold_label must be problem|clean")
            ex.setdefault("audit_skill", skill_hint)
            out.append(ex)
        return out

    # Does gold_dir directly contain *.json gold files?
    has_json = any(f.endswith(".json") for f in os.listdir(gold_dir))
    if has_json:
        skill = os.path.basename(gold_dir.rstrip("/"))
        return {skill: load_skill_dir(gold_dir, skill)}

    # Otherwise treat subdirs as per-skill gold sets.
    result = {}
    for sub in sorted(os.listdir(gold_dir)):
        subpath = os.path.join(gold_dir, sub)
        if os.path.isdir(subpath):
            exs = load_skill_dir(subpath, sub)
            if exs:
                result[sub] = exs
    if not result:
        die(f"no gold examples found under {gold_dir}")
    return result


def load_predictions(pred_path, skills):
    """Return {skill: {id: verdict}}. pred_path is a JSONL file or a dir of <skill>.jsonl."""
    pred_path = os.path.abspath(os.path.expanduser(pred_path))

    def load_jsonl(path):
        m = {}
        with open(path, encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except ValueError as e:
                    die(f"{path}:{n}: invalid JSON line: {e}")
                if "id" not in rec or "verdict" not in rec:
                    die(f"{path}:{n}: prediction needs 'id' and 'verdict'")
                v = rec["verdict"]
                if v not in ALL_VERDICTS:
                    die(f"{path}:{n}: unknown verdict '{v}'")
                m[rec["id"]] = v
        return m

    if os.path.isdir(pred_path):
        out = {}
        for skill in skills:
            f = os.path.join(pred_path, f"{skill}.jsonl")
            out[skill] = load_jsonl(f) if os.path.isfile(f) else {}
        return out
    if not os.path.isfile(pred_path):
        die(f"predictions not found: {pred_path}")
    if len(skills) != 1:
        die("a single predictions file requires a single-skill gold dir; "
            "pass a directory of <skill>.jsonl for multi-skill scoring")
    return {skills[0]: load_jsonl(pred_path)}


def score_skill(examples, preds, flag_verdicts):
    tp = fn = fp = tn = 0
    unscored = []
    rows = []
    for ex in examples:
        eid = ex["id"]
        if eid not in preds:
            unscored.append(eid)
            continue
        verdict = preds[eid]
        flagged = verdict in flag_verdicts
        gold_problem = ex["gold_label"] == "problem"
        if gold_problem and flagged:
            outcome = "TP"; tp += 1
        elif gold_problem and not flagged:
            outcome = "FN"; fn += 1
        elif not gold_problem and flagged:
            outcome = "FP"; fp += 1
        else:
            outcome = "TN"; tn += 1
        rows.append({"id": eid, "gold": ex["gold_label"], "verdict": verdict,
                     "outcome": outcome, "category": ex.get("category", "")})

    fnr = fn / (tp + fn) if (tp + fn) else None
    fpr = fp / (fp + tn) if (fp + tn) else None
    return {
        "counts": {"TP": tp, "FN": fn, "FP": fp, "TN": tn},
        "fnr": fnr, "fpr": fpr,
        "n_scored": tp + fn + fp + tn,
        "unscored": unscored,
        "rows": rows,
    }


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


def fmt(x):
    return "n/a" if x is None else f"{x:.3f}"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Score audit verdicts against a gold set (FNR/FPR).")
    ap.add_argument("--gold-dir", required=True, help="gold dir for one skill, or a parent of <skill>/ dirs")
    ap.add_argument("--predictions", required=True, help="predictions .jsonl (single skill) or dir of <skill>.jsonl")
    ap.add_argument("--max-fnr", type=float, default=0.15, help="max acceptable false-negative rate (default 0.15)")
    ap.add_argument("--max-fpr", type=float, default=0.10, help="max acceptable false-positive rate (default 0.10)")
    ap.add_argument("--flag-verdicts", default=",".join(sorted(DEFAULT_FLAG_VERDICTS)),
                    help="comma list of verdicts treated as 'flagged' (default FAIL,BLOCKED,ERROR)")
    ap.add_argument("--json-out", help="write the full report JSON here")
    args = ap.parse_args(argv)

    flag_verdicts = {v.strip().upper() for v in args.flag_verdicts.split(",") if v.strip()}
    bad = flag_verdicts - ALL_VERDICTS
    if bad:
        die(f"unknown verdict(s) in --flag-verdicts: {sorted(bad)}")

    gold = load_gold(args.gold_dir)
    preds = load_predictions(args.predictions, list(gold.keys()))

    report = {
        "thresholds": {"max_fnr": args.max_fnr, "max_fpr": args.max_fpr},
        "flag_verdicts": sorted(flag_verdicts),
        "skills": {},
    }
    any_breach = False
    any_scored = False

    print(f"Audit calibration (flag = {','.join(sorted(flag_verdicts))}; "
          f"max FNR {args.max_fnr}, max FPR {args.max_fpr})\n")
    for skill, examples in gold.items():
        res = score_skill(examples, preds.get(skill, {}), flag_verdicts)
        breach_reasons = []
        if res["fnr"] is not None and res["fnr"] > args.max_fnr:
            breach_reasons.append(f"FNR {res['fnr']:.3f} > {args.max_fnr}")
        if res["fpr"] is not None and res["fpr"] > args.max_fpr:
            breach_reasons.append(f"FPR {res['fpr']:.3f} > {args.max_fpr}")
        res["breach"] = bool(breach_reasons)
        res["breach_reasons"] = breach_reasons
        report["skills"][skill] = res

        if res["n_scored"]:
            any_scored = True
        if breach_reasons:
            any_breach = True

        c = res["counts"]
        status = "✗ RECALIBRATE" if breach_reasons else ("✓ ok" if res["n_scored"] else "· no data")
        print(f"  {skill}: {status}")
        print(f"    scored={res['n_scored']}  TP={c['TP']} FN={c['FN']} FP={c['FP']} TN={c['TN']}"
              f"  FNR={fmt(res['fnr'])} FPR={fmt(res['fpr'])}")
        if res["unscored"]:
            print(f"    ⚠ {len(res['unscored'])} gold example(s) without predictions: "
                  f"{', '.join(res['unscored'][:5])}{'…' if len(res['unscored'])>5 else ''}")
        for r in breach_reasons:
            print(f"    → {r}")
        print()

    if args.json_out:
        out = os.path.abspath(os.path.expanduser(args.json_out))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
        print(f"report written to {out}")

    if not any_scored:
        print("error: no gold examples had matching predictions — nothing scored", file=sys.stderr)
        return 2
    return 1 if any_breach else 0


if __name__ == "__main__":
    sys.exit(main())
