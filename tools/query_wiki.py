#!/usr/bin/env python3
"""query_wiki.py — stdlib-only keyword search over a local Markdown/Obsidian wiki.

This is the canonical search helper referenced by
`shared-references/local-wiki-link.md` and the `/llm-wiki` skill. It ranks
wiki pages against a free-text query so an agent can read only the most
relevant pages before doing broad external work.

No third-party dependencies. Works on any directory of `.md` files.

Usage:
    python3 query_wiki.py --wiki <wiki-dir> --query "<topic>" [--top 8]
    python3 query_wiki.py --wiki <wiki-dir> --query "<topic>" --json

Scoring (simple, transparent, good enough for a few hundred pages):
    - title/H1 match            weight 5 per query term
    - filename match            weight 4 per query term
    - Obsidian [[link]] target  weight 3 per query term
    - heading (##..) match      weight 2 per query term
    - body term frequency       weight 1 per occurrence (capped)
    - status tag bonus: 已确认 +2, 有争议 +1 (stable knowledge ranks higher)

Exit codes:
    0  ran successfully (even if zero matches)
    2  wiki directory invalid
"""

import argparse
import json
import os
import re
import sys

STATUS_BONUS = {"已确认": 2.0, "有争议": 1.0, "推论": 0.0, "待核验": -1.0}
WIKI_SUBDIR_HINTS = ("wiki", ".")
MAX_BODY_HITS_PER_TERM = 8  # cap term-frequency so long pages don't dominate

LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
H1_RE = re.compile(r"^#\s+(.*)$", re.MULTILINE)
HEADING_RE = re.compile(r"^#{2,6}\s+(.*)$", re.MULTILINE)
WORD_RE = re.compile(r"[\w一-鿿]+", re.UNICODE)


def tokenize(text):
    """Split into lowercased word tokens; keep CJK runs whole."""
    return [t.lower() for t in WORD_RE.findall(text)]


def query_terms(query):
    """Tokenize the query. For CJK queries, also add character bigrams so a
    multi-character topic still matches pages that use it in running text."""
    raw = tokenize(query)
    terms = set(raw)
    for tok in raw:
        if re.fullmatch(r"[一-鿿]+", tok) and len(tok) >= 2:
            for i in range(len(tok) - 1):
                terms.add(tok[i : i + 2])
    return [t for t in terms if t]


def iter_markdown(wiki_dir):
    skip_dirs = {".git", ".meta", "raw", "node_modules", "__pycache__", ".obsidian"}
    for root, dirs, files in os.walk(wiki_dir):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for fn in files:
            if fn.lower().endswith(".md"):
                yield os.path.join(root, fn)


def detect_status(text):
    for status in STATUS_BONUS:
        if status in text:
            return status
    return None


def score_page(path, terms, wiki_dir):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        return None

    lower = text.lower()
    rel = os.path.relpath(path, wiki_dir)
    fname = os.path.basename(path).lower()

    h1 = H1_RE.search(text)
    title = h1.group(1).strip() if h1 else os.path.splitext(os.path.basename(path))[0]
    title_l = title.lower()

    headings = " ".join(HEADING_RE.findall(text)).lower()
    link_targets = " ".join(LINK_RE.findall(text)).lower()

    score = 0.0
    matched = []
    for term in terms:
        hit = False
        if term in title_l:
            score += 5
            hit = True
        if term in fname:
            score += 4
            hit = True
        if term in link_targets:
            score += 3
            hit = True
        if term in headings:
            score += 2
            hit = True
        tf = lower.count(term)
        if tf:
            score += min(tf, MAX_BODY_HITS_PER_TERM)
            hit = True
        if hit:
            matched.append(term)

    if score == 0:
        return None

    status = detect_status(text)
    if status:
        score += STATUS_BONUS[status]

    snippet = make_snippet(text, matched)
    return {
        "path": rel,
        "title": title,
        "score": round(score, 2),
        "status": status,
        "matched_terms": sorted(set(matched)),
        "snippet": snippet,
    }


def make_snippet(text, matched, width=160):
    if not matched:
        return ""
    lower = text.lower()
    pos = min((lower.find(t) for t in matched if lower.find(t) >= 0), default=-1)
    if pos < 0:
        return ""
    start = max(0, pos - width // 3)
    end = min(len(text), start + width)
    frag = text[start:end].replace("\n", " ").strip()
    return ("…" if start > 0 else "") + frag + ("…" if end < len(text) else "")


def resolve_wiki_dir(arg):
    """Accept either a wiki root (containing wiki/) or the wiki dir itself."""
    arg = os.path.abspath(os.path.expanduser(arg))
    if os.path.isdir(os.path.join(arg, "wiki")):
        return os.path.join(arg, "wiki")
    return arg


def main(argv=None):
    ap = argparse.ArgumentParser(description="Keyword search over a local Markdown wiki.")
    ap.add_argument("--wiki", required=True, help="Path to wiki dir (or a root containing wiki/).")
    ap.add_argument("--query", required=True, help="Free-text topic to search for.")
    ap.add_argument("--top", type=int, default=8, help="Max results to print (default 8).")
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = ap.parse_args(argv)

    wiki_dir = resolve_wiki_dir(args.wiki)
    if not os.path.isdir(wiki_dir):
        print(f"error: wiki directory not found: {wiki_dir}", file=sys.stderr)
        return 2

    terms = query_terms(args.query)
    if not terms:
        print("error: empty query after tokenization", file=sys.stderr)
        return 2

    results = []
    for path in iter_markdown(wiki_dir):
        scored = score_page(path, terms, wiki_dir)
        if scored:
            results.append(scored)

    results.sort(key=lambda r: (-r["score"], r["path"]))
    top = results[: args.top]

    if args.json:
        print(json.dumps({"wiki": wiki_dir, "query": args.query, "results": top},
                         ensure_ascii=False, indent=2))
        return 0

    if not top:
        print(f"No pages matched '{args.query}' in {wiki_dir}")
        return 0

    print(f"Top {len(top)} of {len(results)} matches for '{args.query}':\n")
    for i, r in enumerate(top, 1):
        tag = f" [{r['status']}]" if r["status"] else ""
        print(f"{i}. {r['title']}{tag}  (score {r['score']})")
        print(f"   {r['path']}")
        if r["snippet"]:
            print(f"   {r['snippet']}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
