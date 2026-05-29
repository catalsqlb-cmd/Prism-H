# Local Wiki Link Protocol

Use this reference when PRISM needs to connect a research project to an external local Markdown/Obsidian wiki rather than only the project-local `research-wiki/` graph.

## Purpose

The local wiki is the user's durable knowledge base. PRISM should:

1. Read existing wiki pages before repeating literature or source work.
2. Use wiki pages as the user's prior knowledge baseline.
3. Write back only durable, reusable research outputs.
4. Preserve source integrity: never modify `raw/` files.

## Supported Wiki Shapes

### Prism research-wiki

Detected by a project-local `research-wiki/` directory with:

```
research-wiki/
  index.md
  query_pack.md
  papers/
  ideas/
  experiments/
  claims/
  graph/edges.jsonl
```

Use `/research-wiki` and `tools/research_wiki.py` for this shape.

### External Markdown / Obsidian wiki

Detected by an external root with:

```
wiki/
  index.md
  log.md
raw/
scripts/query_wiki.py        # optional but preferred for search
AGENTS.md or CLAUDE.md       # optional maintenance rules
```

Example shapes (use your own paths):

- `<home>/<topic>-wiki/` — a standalone topic knowledge base (e.g. a sports-law
  or political-philosophy wiki) with `wiki/index.md` at its root
- `<project>/wiki/` — a wiki living inside a research project directory

Do not hard-fail if a candidate path does not exist; auto-detection is
opportunistic. Users declare their own wiki roots via the resolution order below
(env var, project config, or an explicit command override) — Prism ships no
hard-coded personal paths.

## Resolution Order

Resolve `LOCAL_WIKI_ROOT` in this order:

1. Explicit override in the user command, e.g. `local_wiki: /path/to/wiki-root`.
2. `CLAUDE.md`, `AGENTS.md`, or `RESEARCH_BRIEF.md` entries named `Local Wiki`, `Wiki Root`, `Knowledge Base`, or `知识库`.
3. The `PRISM_WIKI_ROOT` environment variable, if set and valid.
4. Per-discipline defaults declared by the user in `CLAUDE.md`/`AGENTS.md` under a
   `Discipline Wikis` mapping (e.g. `sports-law -> ~/sports-law-wiki`). Prism ships
   no built-in personal paths; only user-declared mappings are honored.
5. Current project if it has `wiki/index.md`.
6. Disabled if no candidate validates.

A valid external wiki root must have `wiki/index.md`. If it also has `AGENTS.md` or `CLAUDE.md`, read that maintenance file before writing.

## Query Protocol

Before broad external search, query the local wiki:

1. Read `<root>/wiki/index.md` to identify relevant pages.
2. Run the wiki search helper. Wikis scaffolded by `/llm-wiki init` (or
   `install_prism.sh --with-wiki`) ship `<root>/scripts/query_wiki.py`; the
   canonical copy also lives at Prism `tools/query_wiki.py`. Prefer the
   wiki-local copy when present:
   ```bash
   python3 <root>/scripts/query_wiki.py --wiki <root>/wiki --query "<topic>" --top 8
   # or, if the wiki has no scripts/ dir:
   python3 <prism-repo>/tools/query_wiki.py --wiki <root>/wiki --query "<topic>" --top 8
   ```
3. Read only the top relevant pages needed for the current task.
4. Treat wiki conclusions by status:
   - `已确认`: stable prior knowledge
   - `有争议`: preserve competing positions
   - `推论`: usable as inference, not source text
   - `待核验`: do not cite as settled support

## Write-Back Protocol

Write back only when `LOCAL_WIKI_MODE=read-write` and the output has durable value.

Allowed write targets:

- `wiki/memos/` for research memos, synthesis, critique, and long-lived answers
- `wiki/sources/` for source summaries
- `wiki/topics/`, `wiki/concepts/`, `wiki/cases/`, `wiki/statutes/`, `wiki/comparative/` for stable pages that fit existing structure
- `wiki/log.md` append-only timeline
- `wiki/index.md` navigation updates when new pages are added

Forbidden write targets:

- `raw/` source materials
- `.meta/` compiled ledgers unless the wiki's own script updates them
- generated outputs outside `wiki/` unless the user requests an export

Every write-back must:

1. Prefer updating an existing page over creating a duplicate.
2. Include source anchors or mark claims `待核验`.
3. Add backlinks using Obsidian-style `[[relative/page]]` links where consistent with the wiki.
4. Append `wiki/log.md` with date, action, affected pages, and source/project context.
5. Update `wiki/index.md` if a new durable page is created.

## Bridge Artifacts

In the active research project, write a lightweight bridge note when a local wiki is linked:

```
LOCAL_WIKI_LINK.md
```

Recommended fields:

```markdown
# Local Wiki Link

- Root: /absolute/path/to/wiki-root
- Mode: read-only | read-write
- Discipline: sports-law
- Query command: python3 /absolute/path/scripts/query_wiki.py --wiki /absolute/path/wiki --query "<topic>" --top 8
- Last synced: YYYY-MM-DD

## Linked Pages

- [[topics/...]] — reason

## Write-Back Log

- YYYY-MM-DD — wrote wiki/memos/... from prism-pipeline Stage X
```

This bridge note connects project artifacts to the external wiki without forcing the external wiki to mirror every temporary project file.

## Relationship to Prism research-wiki

Use both systems when useful:

- External local wiki: durable human-readable domain knowledge and Obsidian-style pages.
- `research-wiki/`: structured graph of papers, ideas, experiments, and claims for Prism automation.

When both exist, do not merge directories. Instead:

1. Query external wiki for prior domain knowledge.
2. Update `research-wiki/` for project lifecycle graph.
3. Write selected durable summaries back to external wiki memos or source pages.
