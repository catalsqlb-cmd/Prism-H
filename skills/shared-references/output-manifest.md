# Output Manifest Protocol

After writing any output file, append an entry to `MANIFEST.md` in the project root.

## Format

If `MANIFEST.md` does not exist, create it with this header:

```markdown
# Research Output Manifest

> Auto-maintained by Prism skills. Tracks all generated artifacts across the research lifecycle.

| Timestamp | Skill | File | Stage | Description |
|-----------|-------|------|-------|-------------|
```

Then append one row per output file written:

```
| 2026-05-29 14:30 | /research-lit | lit-stage/LIT_REVIEW_20260529_143022.md | literature | 24 sources surveyed for "athlete rights" direction |
| 2026-05-29 14:30 | /research-lit | lit-stage/LIT_REVIEW.md | literature | latest copy |
```

## Stage Values

| Stage | Skills |
|-------|--------|
| `literature` | /research-lit, /novelty-check, /research-review |
| `evidence` | /research-refine, /research-refine-pipeline, /statute-case-mapper, /comparative-law, /argument-stress-test |
| `review` | /research-review |
| `paper` | /paper-writing, /paper-write, /paper-compile |

## Pre-flight Check

Before writing output, if the skill depends on a prerequisite file from a previous stage:
1. Check if the prerequisite file exists at its expected stage-scoped path (e.g., `idea-stage/IDEA_REPORT.md`, `review-stage/AUTO_REVIEW.md`)
2. If not found at the stage-scoped path, check the legacy root-level path (e.g., `./IDEA_REPORT.md`, `./AUTO_REVIEW.md`) — see [Path Fallback Rule](output-versioning.md#path-fallback-rule-backward-compatibility)
3. If not found at either path, warn: "⚠️ Expected {file} (from {skill}) but not found. Run {skill} first?"
4. Do not block — the user may have the file elsewhere or want to proceed anyway
