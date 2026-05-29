---
name: statute-case-mapper
description: Maps each normative claim in a legal argument to its supporting positive law, cases, arbitral awards, and organization rules — tagging rule hierarchy and checking that case/award selection is systematic rather than cherry-picked. Produces a claim→authority mapping table. Use when user says "建立法条案例映射", "statute case map", "把论点对应到法条", "map claims to authority", "梳理请求权基础/案例", or wants to ground a doctrinal argument in concrete legal materials.
argument-hint: [path-to-draft or claim-list]
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, Agent, WebFetch, WebSearch, mcp__codex__codex, mcp__codex__codex-reply
---

# Statute / Case Mapper: Claim → Authority Grounding

Turn a doctrinal argument into an auditable **mapping table**: every load-bearing
normative claim linked to the specific positive law, cases, arbitral awards, and
organization rules that support (or undercut) it, with the rule hierarchy made
explicit and the case selection checked for systematicity. This is the materials
layer that `/argument-stress-test` then audits and `/legal-writing` then drafts
from — the law/humanities analog of turning a result into grounded claims.

## Context: $ARGUMENTS

## Constants

- MAP_DOC: `STATUTE_CASE_MAP.md` at the project / paper root (human-readable table)
- MAP_JSON: `STATUTE_CASE_MAP.json` (machine-consumable, read by `/argument-stress-test` and `/legal-writing`)
- Authority tiers (highest → lowest binding force, default Chinese law):
  `constitution` > `statute` (法律) > `administrative-regulation` (行政法规) >
  `local-regulation` / `department-rule` (地方性法规/部门规章) > `judicial-interpretation`
  (司法解释) > `guiding-case` (指导性案例) > `ordinary-case` (普通判例, persuasive) >
  `association-rule` (协会/联盟规则) > `contract` (合同/章程) > `event-rule` (赛事规则) >
  `soft-law` (CAS说理/学说/政策, persuasive only). CAS awards are `arbitral`.

## When to Use

- After claims exist (from `/legal-writing`, `/paper-plan`, or a draft) and before
  `/argument-stress-test` — the map is the evidence the stress-test checks against
- When the user has an argument but no organized authority base yet
- To diagnose cherry-picking: surface contrary authority the draft ignores

Discipline-aware: read `PRISM_PROFILE.md` if present. For `sports-law`, pull the
profile's *Literature Sources* (CNKI, 北大法宝, CAS database, IOC/WADA/FIFA rules)
as the search order. For `humanities`, "authority" becomes primary texts / canonical
sources and the hierarchy collapses to primary > secondary > tertiary.

## Protocol

### Step 1: Collect the claims

If given a draft, extract load-bearing normative claims (same decomposition as
`/argument-stress-test` Step 1). If given a claim list, use it directly. Record
`claim_id`, `claim_text`, `claim_type`.

### Step 2: Map each claim to authority

For each claim, search the profile's sources and the local wiki first (see Local
Wiki Defaults below) for the authorities that bear on it. For each authority found:

- `cite`: full pin-cite (法条款项 / 案号 / CAS 案号 / 规则条款)
- `tier`: from the hierarchy above
- `authority_status`: `binding` | `persuasive` | `arbitral` | `contractual` | `soft-law`
- `relation`: `supports` | `partially-supports` | `cuts-against` | `mixed`
- `pinpoint`: the specific provision / holding / paragraph that does the work
- `excerpt`: short verbatim quote of the operative text (for `/citation-audit` L3)

**Actively look for `cuts-against` authority.** A claim mapped only to supporting
sources is suspect — note the contrary authorities you searched for and whether
any exist. Recording "searched X, found no contrary authority" is itself a result.

### Step 3: Rank and select systematically

When a claim has many candidate cases/awards, do not just keep the favorable ones.
Record the *selection rule* you applied (e.g. "all guiding cases on this issue +
the three most-cited ordinary cases + any CAS award since 2015 on point"). The
selection rule is part of the artifact — it is what makes the mapping defensible
and what `/argument-stress-test`'s systematic-selection test checks.

### Step 4: Flag gaps

For each claim, set `grounding_status`:

- `well-grounded` — binding authority directly on point, no ignored contrary authority
- `thinly-grounded` — only persuasive / general-clause / soft-law support
- `contested` — significant `cuts-against` authority exists and must be addressed
- `ungrounded` — no authority found; claim is currently unsupported
- `needs-fetch` — promising authority identified but full text not yet retrieved

### Step 5: Emit artifacts

Write `STATUTE_CASE_MAP.json` and `STATUTE_CASE_MAP.md`. JSON schema:

```json
{
  "skill": "statute-case-mapper",
  "date": "2026-05-29",
  "target": "paper/main.tex",
  "discipline": "sports-law",
  "claims": [
    {
      "claim_id": "C1",
      "claim_text": "赛事组织者对赛事数据享有可受法律保护的商业控制利益。",
      "claim_type": "interpretive",
      "grounding_status": "contested",
      "selection_rule": "反不正当竞争一般条款相关指导性案例 + 数据/数据库不正当竞争主流判例 + 比较法上欧盟数据库指令。",
      "authorities": [
        {
          "cite": "《反不正当竞争法》第2条",
          "tier": "statute",
          "authority_status": "binding",
          "relation": "partially-supports",
          "pinpoint": "诚实信用与公认商业道德的一般条款",
          "excerpt": "经营者在生产经营活动中，应当遵循自愿、平等、公平、诚信的原则……"
        },
        {
          "cite": "（某数据不正当竞争案，案号）",
          "tier": "ordinary-case",
          "authority_status": "persuasive",
          "relation": "supports",
          "pinpoint": "认定对数据的实质性投入可受反不正当竞争法保护",
          "excerpt": "……"
        },
        {
          "cite": "（反对将赛事数据私权化的学说/案例）",
          "tier": "soft-law",
          "authority_status": "soft-law",
          "relation": "cuts-against",
          "pinpoint": "信息自由流通与公共领域的反对意见",
          "excerpt": "……"
        }
      ]
    }
  ]
}
```

### Step 6: Print summary

```
📋 Statute/Case Map Complete  (discipline: sports-law)

  Claims mapped:        12
  ✅ well-grounded:      7
  ⚠️ thinly-grounded:   2
  ⚠️ contested:         2   (contrary authority must be addressed)
  ❌ ungrounded:        1
  ⏳ needs-fetch:       0

  Next: run /argument-stress-test to audit the grounding,
        or /citation-audit (L3) to verify the excerpts.

  See STATUTE_CASE_MAP.md for the full table.
```

## Local Wiki Defaults

If the profile or `CLAUDE.md` declares an external wiki root, or `research-wiki/`
exists, **query it before web search**: read `wiki/index.md`
and run the wiki's `scripts/query_wiki.py` (or `tools/query_wiki.py`) for each
claim's key terms. Map durable authority summaries back to `wiki/sources/` and
stable statutes/cases to their matching folders. Never modify `raw/`.

## Key Rules

- **Hierarchy is mandatory.** Every authority carries a `tier` and
  `authority_status`. An unranked citation is not done.
- **Hunt contrary authority.** The mapper's job is not advocacy; an honest map
  records what cuts against the claim. `contested` is a feature, not a failure.
- **Selection rule is an artifact.** "Why these cases" must be written down, or
  the systematic-selection audit cannot pass.
- **Excerpts feed L3.** Capture verbatim operative text so `/citation-audit` can
  verify claim↔source at the claim level.
- **Map, don't argue.** This skill grounds; `/legal-writing` drafts;
  `/argument-stress-test` judges. Keep the roles separate.
