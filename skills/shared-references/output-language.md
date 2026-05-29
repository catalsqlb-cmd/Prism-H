# Output Language Protocol

## Language Detection

Determine the output language using this priority:
1. Check `CLAUDE.md` for a `language:` field in `## Pipeline Status` — if `language: zh` or `language: cn`, output in Chinese
2. If the user's most recent message is in Chinese, output in Chinese
3. Default: English

## What to Localize

- Section headings and labels
- Descriptions, analysis, commentary, recommendations
- Template boilerplate text
- Status messages and warnings

## What NOT to Localize

- Code, shell commands, file paths, directory names
- Paper titles, author names, venue names, BibTeX entries
- Technical terms with no standard Chinese translation (keep English, optionally annotate: "attention mechanism (注意力机制)")
- LaTeX content — paper-writing workflow outputs English for international venues; for Chinese venues (法学研究、中国法学、体育科学 etc.), outputs Chinese with discipline-appropriate citation format (see `citation-cn-footnote.md`)
- JSON state files — keys and structure remain English
- **Machine-parsed markers** — never localize the following, regardless of language setting:
  - Markdown frontmatter keys (e.g., `outcome:`, `node_id:`, `title:`, `type:`)
  - Research Wiki schema fields parsed by `tools/research_wiki.py` (e.g., `outcome: negative`, `outcome: positive`, `node_id:`)
  - `MANIFEST.md` column headers and table structure
  - Any field that downstream tools or scripts read programmatically

## Skill-Specific Rules

| Skill | Language Support | Notes |
|-------|-----------------|-------|
| /research-review | Partial | AUTO_REVIEW.md follows setting; reviewer prompts stay English |
| /research-refine | Full | FINAL_PROPOSAL.md follows setting |
| /research-refine-pipeline | Full | PIPELINE_SUMMARY.md follows setting |
| /research-pipeline | Full | Inherits from sub-skills |
| /argument-stress-test | Full | Claim descriptions follow setting |
| /paper-writing | Conditional | English LaTeX for international venues; **Chinese LaTeX/Word for Chinese venues** (法学研究、体育科学 etc.) — see `citation-cn-footnote.md` |
| /paper-write | Conditional | Same as /paper-writing: language follows target venue |
