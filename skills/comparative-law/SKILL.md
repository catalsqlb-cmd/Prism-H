---
name: comparative-law
description: Functional comparative-law analysis — compares how different legal systems solve the same governance problem by functional equivalents, not by superficial jurisdiction labels, and screens for transplant feasibility into the target system. Use when user says "比较法分析", "comparative law", "做功能比较", "比较各国/各法域", "comparative sports law", or wants a rigorous comparison that avoids shallow jurisdiction lists.
argument-hint: [problem-or-claim and the systems to compare]
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, Agent, WebFetch, WebSearch, mcp__codex__codex, mcp__codex__codex-reply
---

# Comparative Law: Functional Comparison & Transplant Screening

Run a comparison the way comparative-law methodology actually requires: start from
a **shared functional problem**, find how each system solves it (whatever doctrinal
label or institution it uses), then assess whether a foreign solution can be
transplanted into the target system. This skill exists because the most common
comparative failure — flagged by every `law` / `sports-law` profile — is the
"superficial jurisdiction list": "在美国是X，在德国是Y，在日本是Z，所以中国应当W",
with no functional equivalence and no transplant analysis.

## Context: $ARGUMENTS

## Constants

- OUT_DOC: `COMPARATIVE_ANALYSIS.md` at the project / paper root
- OUT_JSON: `COMPARATIVE_ANALYSIS.json` (machine-consumable; feeds `/legal-writing` and `/argument-stress-test`)
- Default target system: from `PRISM_PROFILE.md` (Chinese sports law for `sports-law`); else ask or infer.

## When to Use

- When an argument relies on a foreign model and needs to be made rigorous
- Before `/argument-stress-test`'s comparative-validity test, to supply the analysis it checks
- Standalone, to map the solution space for a governance problem

## Protocol

### Step 1: State the functional problem (tertium comparationis)

Name the **shared problem** all systems face, stated functionally and neutrally —
not in any one system's doctrinal vocabulary. This is the *tertium comparationis*,
the common third term that makes comparison valid.

- ✅ "How does each system allocate the commercial value of live-event data
  between the organizer and third parties?"
- ❌ "How does each system treat 赛事数据的不正当竞争保护?" (already framed in one
  system's doctrine — biases the comparison)

### Step 2: Find functional equivalents per system

For each system being compared, identify **whatever legal mechanism actually
performs that function** — it may be a statute, a tort doctrine, a competition-law
rule, an IP right, a contractual / association-rule regime, or a CAS award line.
Do not assume the function lives in the same doctrinal box as in the home system.
Record per system:

- `system`: jurisdiction or governance order (state, EU, CAS, FIFA, NCAA, …)
- `mechanism`: the actual functional solution (with pin-cites)
- `how_it_works`: the operative rule in one or two sentences
- `enforcement`: who enforces it and how (court / arbitral / association / self-help)
- `outcome`: the practical result it produces for the function in Step 1

### Step 3: Compare on the function, not the label

Build a comparison matrix keyed by the function. Surface:

- where systems **converge** (same outcome via different mechanisms)
- where they **diverge** and *why* (different background institutions, not just
  different rules — e.g. presence/absence of a database right, of antitrust
  scrutiny, of a strong association-autonomy tradition)
- which differences are **doctrinal surface** vs **functionally consequential**

### Step 4: Transplant screening

For any foreign solution proposed for the target system, screen feasibility:

- `legal_compatibility`: does it fit the target's positive law and rule hierarchy?
- `institutional_fit`: do the enforcing institutions exist in the target (courts,
  arbitral bodies, regulators, associations with the needed capacity)?
- `background_conditions`: does the solution depend on background conditions the
  target lacks (e.g. a database sui generis right, a particular antitrust regime)?
- `adaptation_needed`: what must change for it to work in the target?
- `verdict`: `transplantable` | `transplantable-with-adaptation` | `ill-suited`

A solution that works abroad because of background conditions the target lacks is
`ill-suited` even if doctrinally attractive — saying so is the point of the screen.

### Step 5: Emit artifacts

Write `COMPARATIVE_ANALYSIS.json` and `.md`. JSON schema:

```json
{
  "skill": "comparative-law",
  "date": "2026-05-29",
  "discipline": "sports-law",
  "function": "如何在赛事组织者与第三方之间分配赛事数据的商业价值",
  "target_system": "中国法",
  "systems": [
    {
      "system": "欧盟",
      "mechanism": "数据库特殊权利（Database Directive 96/9/EC sui generis right）",
      "how_it_works": "对数据库的实质性投入获得独立于版权的提取/再利用控制权。",
      "enforcement": "成员国法院",
      "outcome": "组织者获得较强的私权式控制。"
    },
    {
      "system": "美国",
      "mechanism": "无数据库专有权，主要依赖合同 + 盗用(misappropriation)/热点新闻原则的有限残余",
      "how_it_works": "以准入合同和有限的不正当竞争法理控制，私权化程度低。",
      "enforcement": "法院（合同/侵权）",
      "outcome": "控制力较弱，更依赖私人秩序。"
    }
  ],
  "convergence": ["都承认组织者对赛事接入有合同层面的控制"],
  "divergence": ["是否承认独立于合同的私权式数据权利——取决于是否存在数据库特殊权利这一背景制度"],
  "transplant": {
    "candidate": "欧盟式数据库特殊权利",
    "legal_compatibility": "中国现行法无对应 sui generis 权利，需新设或借由反不正当竞争一般条款近似实现",
    "institutional_fit": "法院可执行，但缺乏专门登记/权利边界制度",
    "background_conditions": "依赖一个中国尚不存在的数据库专有权背景制度",
    "adaptation_needed": "改以反不正当竞争+合同的功能近似方案，而非直接移植专有权",
    "verdict": "transplantable-with-adaptation"
  }
}
```

### Step 6: Print summary

```
📋 Comparative Analysis Complete  (discipline: sports-law)

  Function:        赛事数据商业价值的分配
  Systems compared: 欧盟 / 美国 / 中国(目标)
  Convergence:      1 point
  Divergence:       1 functionally-consequential difference
  Transplant:       transplantable-with-adaptation
                    (欧盟专有权依赖中国缺失的背景制度，建议功能近似)

  See COMPARATIVE_ANALYSIS.md for the matrix and transplant screen.
```

## Local Wiki Defaults

Query the profile's external wiki / `research-wiki/` before web search (read
`wiki/index.md`, run `query_wiki.py`). Write durable comparative memos to
`wiki/memos/`. Never modify `raw/`.

## Key Rules

- **Tertium comparationis first.** No comparison without a neutral functional
  problem statement. Framing the function in one system's doctrine biases everything.
- **Functional equivalents, not labels.** The same function may live in tort here,
  competition law there, contract elsewhere. Find the mechanism that does the work.
- **Explain divergence by institutions, not just rules.** Different outcomes usually
  trace to different background conditions; name them.
- **Always screen transplant feasibility.** A foreign solution is a recommendation
  only after the background-conditions check. `ill-suited` is a valid, valuable result.
- **No superficial jurisdiction lists.** A flat "country X does A, Y does B" with no
  function and no transplant screen is exactly the anti-pattern this skill replaces.
