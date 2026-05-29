#!/usr/bin/env python3
"""llm_wiki.py — scaffold and lint a general-purpose personal "LLM Wiki".

Implements Karpathy's LLM-Wiki pattern (gist 442a6bf…) as a portable,
stdlib-only CLI so any user installing Prism can sync the whole workflow to
a local directory.

Three layers:
    raw/      immutable source material (never edited by the agent)
    wiki/     generated, human-readable Markdown knowledge (the durable KB)
    CLAUDE.md schema/contract describing how the wiki is built & maintained

Subcommands:
    init  <root>            scaffold the three-layer structure + seed files
    lint  <root>            report orphans, stale pages, missing concepts,
                            and likely contradictions; exit 1 if any error-level
    log   <root> --msg ...  append a dated line to wiki/log.md

Search is delegated to the sibling `query_wiki.py` (the `/llm-wiki query`
subcommand calls that). This tool focuses on structure & hygiene.

Status tags used across the wiki: 已确认 / 有争议 / 推论 / 待核验.
"""

import argparse
import datetime
import os
import re
import sys

LINK_RE = re.compile(r"\[\[([^\]#|]+)")
STATUS_TAGS = ("已确认", "有争议", "推论", "待核验")
STALE_DAYS = 180

WIKI_DIRS = ("topics", "concepts", "sources", "memos")


def today():
    return datetime.date.today().isoformat()


# ---------------------------------------------------------------- init

CLAUDE_SCHEMA = """\
# LLM Wiki — Schema & Maintenance Contract

This directory is a personal knowledge base built on Karpathy's LLM-Wiki
pattern. An LLM agent (Prism / Claude Code) reads and maintains it under the
rules below.

## Three layers

| Layer | Path | Mutability | Purpose |
|-------|------|-----------|---------|
| Raw   | `raw/`   | **immutable** — never edit or delete | source material: PDFs, clippings, transcripts, dumps |
| Wiki  | `wiki/`  | agent-generated, human-readable | distilled, linked, durable knowledge |
| Schema| `CLAUDE.md` (this file) | human-owned | how the wiki is built & linted |

## Wiki structure

```
wiki/
  index.md        navigation catalog (one line per durable page)
  log.md          append-only timeline of every change
  topics/         broad subject pages
  concepts/       single-idea atomic notes
  sources/        per-source summaries (1 page per raw/ item)
  memos/          synthesis, answers, critiques, long-lived outputs
```

## Page conventions

- Every page starts with `# Title` (H1) matching its subject.
- Link related pages with Obsidian-style `[[topics/foo]]` / `[[concepts/bar]]`.
- Tag every non-trivial claim with a status:
  - `已确认` — confirmed, stable prior knowledge
  - `有争议` — contested; preserve competing positions
  - `推论` — inference; usable as reasoning, not as a source
  - `待核验` — unverified; do NOT cite as settled support
- Cite sources with a link to the relevant `[[sources/...]]` page or a raw
  anchor. Claims with no source anchor must be tagged `待核验`.

## Workflows

- **ingest**: read a `raw/` item → write/update a `[[sources/...]]` page →
  fold durable facts into the relevant `topics/`/`concepts/` page → append
  `log.md` → update `index.md` if a page was created.
- **query**: `python3 scripts/query_wiki.py --wiki wiki --query "<topic>"`
  before doing broad external search; read prior knowledge first.
- **lint**: `python3 scripts/llm_wiki.py lint .` to find orphans, stale
  pages, contradictions, and missing concept pages.

## Hard rules

1. Never modify or delete anything under `raw/`.
2. Prefer updating an existing page over creating a near-duplicate.
3. Every write appends `wiki/log.md` and (for new pages) updates
   `wiki/index.md`.
"""

INDEX_SEED = """\
# Wiki Index

Navigation catalog. One line per durable page: a wiki-link to the page plus a
one-line hook. See the Concepts section below for the format.

## Topics

## Concepts

- [[concepts/example-concept]] — delete once you have real notes

## Sources

## Memos
"""

LOG_SEED = """\
# Wiki Log

Append-only timeline. Format: `- YYYY-MM-DD — <action> — <pages> — <context>`.

- {date} — init — scaffolded LLM Wiki structure — llm_wiki.py init
"""

GITIGNORE_SEED = """\
.obsidian/
.DS_Store
__pycache__/
"""

CONCEPT_EXAMPLE = """\
# Example Concept

> Delete this file once you have real notes. It shows the expected shape.

A single-idea atomic note. State the idea in one or two sentences, then tag it.

The core claim goes here. 已确认

Related: [[index]]

Sources: none yet — 待核验
"""


def write_if_absent(path, content):
    if os.path.exists(path):
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return True


def cmd_init(args):
    root = os.path.abspath(os.path.expanduser(args.root))
    os.makedirs(root, exist_ok=True)

    created = []
    # raw layer
    raw_keep = os.path.join(root, "raw", ".gitkeep")
    if write_if_absent(raw_keep, ""):
        created.append("raw/")

    # wiki layer
    for d in WIKI_DIRS:
        keep = os.path.join(root, "wiki", d, ".gitkeep")
        if write_if_absent(keep, ""):
            created.append(f"wiki/{d}/")

    if write_if_absent(os.path.join(root, "wiki", "index.md"), INDEX_SEED):
        created.append("wiki/index.md")
    if write_if_absent(os.path.join(root, "wiki", "log.md"),
                       LOG_SEED.format(date=today())):
        created.append("wiki/log.md")
    if write_if_absent(os.path.join(root, "wiki", "concepts", "example-concept.md"),
                       CONCEPT_EXAMPLE):
        created.append("wiki/concepts/example-concept.md")

    # schema layer
    if write_if_absent(os.path.join(root, "CLAUDE.md"), CLAUDE_SCHEMA):
        created.append("CLAUDE.md")
    if write_if_absent(os.path.join(root, ".gitignore"), GITIGNORE_SEED):
        created.append(".gitignore")

    # ship the search helper alongside so the wiki is self-contained
    scripts_dir = os.path.join(root, "scripts")
    here = os.path.dirname(os.path.abspath(__file__))
    for helper in ("query_wiki.py", "llm_wiki.py"):
        src = os.path.join(here, helper)
        dst = os.path.join(scripts_dir, helper)
        if os.path.exists(src) and not os.path.exists(dst):
            os.makedirs(scripts_dir, exist_ok=True)
            with open(src, "r", encoding="utf-8") as fh:
                data = fh.read()
            with open(dst, "w", encoding="utf-8") as fh:
                fh.write(data)
            os.chmod(dst, 0o755)
            created.append(f"scripts/{helper}")

    if created:
        print(f"Initialized LLM Wiki at {root}")
        for c in created:
            print(f"  + {c}")
    else:
        print(f"LLM Wiki already initialized at {root} (nothing to do)")
    print("\nNext: drop sources into raw/, then run '/llm-wiki ingest'.")
    return 0


# ---------------------------------------------------------------- lint

def wiki_dir_of(root):
    return os.path.join(root, "wiki")


def iter_pages(wiki_dir):
    skip = {".git", ".meta", "raw", "__pycache__", ".obsidian"}
    for r, dirs, files in os.walk(wiki_dir):
        dirs[:] = [d for d in dirs if d not in skip]
        for fn in files:
            if fn.lower().endswith(".md"):
                yield os.path.join(r, fn)


def page_key(wiki_dir, path):
    rel = os.path.relpath(path, wiki_dir)
    return os.path.splitext(rel)[0].replace(os.sep, "/")


def cmd_lint(args):
    root = os.path.abspath(os.path.expanduser(args.root))
    wiki_dir = wiki_dir_of(root)
    if not os.path.isdir(wiki_dir):
        print(f"error: no wiki/ under {root} (run 'init' first)", file=sys.stderr)
        return 2

    pages = list(iter_pages(wiki_dir))
    keys = {page_key(wiki_dir, p) for p in pages}
    basenames = {os.path.splitext(os.path.basename(p))[0]: page_key(wiki_dir, p)
                 for p in pages}

    warnings = []
    errors = []
    now = datetime.datetime.now().timestamp()

    incoming = {k: 0 for k in keys}
    index_path = os.path.join(wiki_dir, "index.md")
    index_text = ""
    if os.path.exists(index_path):
        with open(index_path, encoding="utf-8", errors="replace") as fh:
            index_text = fh.read()

    for path in pages:
        key = page_key(wiki_dir, path)
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()

        # broken links + count incoming
        for tgt in LINK_RE.findall(text):
            tgt = tgt.strip()
            resolved = tgt if tgt in keys else basenames.get(os.path.basename(tgt))
            if resolved is None:
                warnings.append(f"broken link [[{tgt}]] in {key}")
            else:
                incoming[resolved] = incoming.get(resolved, 0) + 1

        # missing H1
        if not re.search(r"^#\s+\S", text, re.MULTILINE):
            warnings.append(f"missing H1 title in {key}")

        # untagged substantive page (skip index/log and tiny stubs)
        base = os.path.basename(path)
        if base not in ("index.md", "log.md") and len(text) > 200:
            if not any(tag in text for tag in STATUS_TAGS):
                warnings.append(f"no status tag ({'/'.join(STATUS_TAGS)}) in {key}")

        # stale
        age_days = (now - os.path.getmtime(path)) / 86400
        if age_days > STALE_DAYS and base not in ("index.md", "log.md"):
            warnings.append(f"stale ({int(age_days)}d since edit): {key}")

        # contradiction heuristic: same page carries both 已确认 and 待核验
        # for overlapping content is common & fine; flag only 有争议 with no
        # competing marker nearby is NOT an error. Instead flag claims tagged
        # both 已确认 and 待核验 on the same line.
        for ln in text.splitlines():
            if "已确认" in ln and "待核验" in ln:
                warnings.append(f"conflicting status on one line in {key}: {ln.strip()[:60]}")

    # orphans: not in index and no incoming links
    for key in keys:
        base = os.path.basename(key)
        if base in ("index", "log"):
            continue
        in_index = key in index_text or os.path.basename(key) in index_text
        if incoming.get(key, 0) == 0 and not in_index:
            warnings.append(f"orphan (no incoming links, not in index): {key}")

    # missing concept: index references a [[concepts/x]] page that doesn't exist
    for tgt in LINK_RE.findall(index_text):
        tgt = tgt.strip()
        if tgt not in keys and os.path.basename(tgt) not in basenames:
            errors.append(f"index.md references missing page [[{tgt}]]")

    print(f"Linted {len(pages)} pages under {wiki_dir}")
    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  ✗ {e}")
    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  ⚠ {w}")
    if not errors and not warnings:
        print("  ✓ clean")

    return 1 if errors else 0


# ---------------------------------------------------------------- log

def cmd_log(args):
    root = os.path.abspath(os.path.expanduser(args.root))
    log_path = os.path.join(wiki_dir_of(root), "log.md")
    if not os.path.exists(log_path):
        print(f"error: {log_path} not found (run 'init' first)", file=sys.stderr)
        return 2
    with open(log_path, "a", encoding="utf-8") as fh:
        fh.write(f"- {today()} — {args.msg}\n")
    print(f"appended to {log_path}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Scaffold and lint a personal LLM Wiki.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="scaffold three-layer wiki structure")
    p_init.add_argument("root", help="wiki root directory to create/populate")
    p_init.set_defaults(func=cmd_init)

    p_lint = sub.add_parser("lint", help="report orphans/stale/contradictions")
    p_lint.add_argument("root", help="wiki root directory")
    p_lint.set_defaults(func=cmd_lint)

    p_log = sub.add_parser("log", help="append a dated line to wiki/log.md")
    p_log.add_argument("root", help="wiki root directory")
    p_log.add_argument("--msg", required=True, help="log message")
    p_log.set_defaults(func=cmd_log)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
