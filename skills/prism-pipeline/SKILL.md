---
name: prism-pipeline
description: "PRISM — Pipeline for Research with Intelligent Subject Mapping. Discipline-aware full research pipeline with interactive decision gates and Soul Protocol. Auto-detects research discipline from user input, RESEARCH_BRIEF.md, or project context (standalone detection or full lifecycle). Soul Interview → 6 human checkpoints → soul-aware writing → soul audit. Ensures every paper has a real problem, personal judgment, coherent thread, real-world concern, disciplined pruning, and something only the author could write. Use when user says \"prism\", \"detect discipline\", \"识别学科\", \"全流程\", \"full pipeline\", \"多学科研究\", \"从找idea到投稿\", or wants discipline detection or the complete research lifecycle with user-guided decisions."
argument-hint: [research-direction]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Skill, mcp__codex__codex, mcp__codex__codex-reply
---

# PRISM Pipeline: Discipline-Aware Research from Idea to Submission

*Pipeline for Research with Intelligent Subject Mapping*

End-to-end **user-guided** research workflow for: **$ARGUMENTS**

## Constants

- **INTERACTIVE_MODE = full** — Controls how many decision gates pause for user input. `full` = all 6 gates + soul interview (default); `lite` = 3 core gates (Gate 2/3/5 only); `off` = autonomous mode (legacy behavior).
- **SOUL_PROTOCOL = true** — When `true` (default for humanities/social sciences/law), runs Soul Interview, soul-enriched gates, thread audit, and pruning checkpoints. When `false`, gates operate in the standard mode without soul dimensions. Auto-enabled when discipline is `law`, `sports-law`, `economics`, `social-sciences`, `humanities`, `philosophy`, `education`, `management`. (`logic` stays `false` by default — formal work needs no soul dimensions; philosophical-logic papers can enable it manually.)
- **AUTO_PROCEED = false** — When `false` (default), all gates wait for user confirmation. When `true`, auto-select top-ranked options and continue.
- **ARXIV_DOWNLOAD = false** — When `true`, `/research-lit` downloads the top relevant PDFs during literature survey.
- **HUMAN_CHECKPOINT = true** — When `true` (default), the auto-review loops pause after each round. When `false`, loops run fully autonomously.
- **REVIEWER_DIFFICULTY = medium** — How adversarial the reviewer is. `medium` / `hard` / `nightmare`.
- **AUTO_WRITE = false** — When `true`, automatically invoke Workflow 3 after research completes.
- **ENABLE_RESEARCH_WIKI = auto** — `auto` updates `/research-wiki` only when an active wiki exists; `true` initializes/updates it; `false` skips persistent graph updates.
- **LOCAL_WIKI_ROOT = auto** — External Markdown/Obsidian wiki root. `auto` detects a discipline-matching local wiki (e.g., `sports-law-wiki`); override with an absolute path.
- **LOCAL_WIKI_MODE = read-write** — `read-only` queries local wiki only; `read-write` also writes durable memos/backlinks when outputs have long-term value.
- **QUALITY_GATES = standard** — `off` skips optional audits; `standard` runs discipline-appropriate evidence checks when inputs exist; `strict` blocks writing/submission until critical issues are resolved.
- **FUNDING_TRACK = false** — When `true`, branch after idea discovery into `/grant-proposal` before implementation.
- **VENUE = auto** — Target venue. When `auto`, inferred from `PRISM_PROFILE.md` (Tier A venue of detected discipline). Override with any venue name: `ICLR`, `NeurIPS`, `法学研究`, `AER`, `NEJM`, `Nature`, `管理世界`, etc.
- **DISCIPLINE = auto** — Research discipline. When `auto` (default), PRISM auto-detects from user input and project context. Override with an explicit ID: `law`, `sports-law`, `economics`, `social-sciences`, `humanities`, `philosophy`, `logic`, `education`, `management`, `communications`.
- **CONFIDENCE_THRESHOLD = 0.7** — Below this score, ask the user to confirm discipline detection.
- **PROFILES_DIR = `../shared-references/prism-profiles/`** — Discipline profile definitions.
- **MODE = full** — `full` runs the complete pipeline; `detect-only` runs only Stage 0 (discipline detection) and outputs `PRISM_PROFILE.md`, then stops. Use `detect-only` when you only need discipline routing without the full research lifecycle.

> Override via argument:
> ```
> /prism-pipeline "体育赛事转播权的法律保护" — discipline: law, venue: 法学研究
> /prism-pipeline "体育赛事数据权益保护" — discipline: sports-law, venue: 体育科学, interactive: full
> /prism-pipeline "罗尔斯差别原则对体育资源分配的证成" — discipline: philosophy, venue: 哲学研究
> /prism-pipeline "minimum wage effects" — discipline: economics, venue: AER, interactive: lite
> /prism-pipeline "短视频平台对青少年注意力的影响" — discipline: communications, interactive: lite
> ```

## Overview

This skill chains the entire research lifecycle with **discipline-aware methodology routing**, **6 interactive decision gates**, and a **Soul Protocol** that ensures every paper carries the author's genuine voice:

```
Soul Interview → PRISM detect → Gate 0 → /research-lit → Gate 1 → research questions → Gate 2
├── Stage -1 ──┤── Stage 0 ──┤         ├── Stage 1a ───┤          ├── Stage 1b ──┤

→ Gate 3 → Gate 4 → develop evidence → /research-review → Gate 5 → /paper-writing → Soul Audit
├──── Stage 2 ──────┤           ├──── Stage 4 ─────┤         ├── Stage 6 ────┤ Stage 7

(MODE=detect-only stops after Stage 0, outputting only PRISM_PROFILE.md)
```

---

## Soul Protocol: Writing Papers with a Soul

> **Core principle**: AI can help you write a "correct" paper, but only you can write "your" paper. The Soul Protocol exists to protect and amplify the human elements that make a paper worth reading.

The Soul Protocol operates at three levels:

### Level 1: Soul Interview (Stage -1)

Before any research begins, extract the author's genuine connection to the problem. This produces `SOUL_BRIEF.md` — the single most important document in the pipeline. Every downstream stage reads it.

### Level 2: Soul-Enriched Gates

Each of the 6 decision gates adds soul-specific questions that go beyond "what to choose" into "why you care." The user's answers are recorded in `SOUL_BRIEF.md` and `DECISION_LOG.md`, and the AI must respect them throughout.

### Level 3: Soul Audit (Writing Phase)

During paper writing, every section draft is tested against 3 questions before proceeding:
1. Does this section advance the author's core argument, or is it padding?
2. Is the author's voice and judgment present, or has it been replaced by generic academic prose?
3. Does this connect back to the thread established in `SOUL_BRIEF.md`?

### The Six Soul Dimensions

| # | Dimension | What It Means | When It's Checked |
|---|-----------|---------------|-------------------|
| 1 | **真实问题** | Not topic-hunting. A real contradiction the author has observed. | Soul Interview, Gate 1 |
| 2 | **自己的判断** | The author has a preliminary position — not neutrality cosplaying as objectivity. | Soul Interview, Gate 2 |
| 3 | **主线贯穿** | One sentence that every chapter serves. If a section can't explain its relationship to this sentence, it doesn't belong. | Gate 3, Thread Audit, Soul Audit |
| 4 | **现实关怀** | This research matters to real people. Who? Why? What changes if we solve it? What breaks if we don't? | Soul Interview, Gate 2, Gate 5 |
| 5 | **反思与取舍** | The discipline to cut. Every paragraph must earn its place. | Soul Audit (per-section pruning) |
| 6 | **非写不可** | Something in this paper could only have been written by this specific author — their puzzlement, experience, anger, or insight. | Soul Interview, Gate 5, final check |

---

## Pipeline

### Stage -1: Soul Interview (灵魂访谈)

**Skip if `SOUL_PROTOCOL=false`.**

Before any research begins, conduct a structured conversation with the user to extract the raw material that gives a paper its soul. This is NOT a questionnaire — it's a dialogue. Ask one question at a time, listen to the answer, and follow up based on what the user reveals.

**The interview proceeds through 4 phases:**

#### Phase 1: 真实困惑 — What bothers you?

Ask the user (using `AskUserQuestion` or direct conversation):

> "在你接触 [research direction] 的过程中，有没有什么让你觉得'不对劲'的事情？不是从文献里读到的gap，而是你自己观察到的、经历过的、或者和别人讨论时争论过的一个矛盾或困惑。"

Follow up until the user articulates a concrete tension, not an abstract topic. Good answers sound like:
- "我发现中国体育赛事转播权的纠纷越来越多，但法院判决的逻辑完全不一致..."
- "我不理解为什么国际上普遍承认的运动员权利，在中国的体育治理中几乎被忽略..."
- "我在实习时遇到一个案子，让我意识到现有的法律框架根本处理不了这个问题..."

Bad answers (push back gently): "我觉得体育法是一个新兴领域" (too generic) / "导师建议我研究这个方向" (no personal connection)

#### Phase 2: 初步判断 — What do you think?

> "关于这个问题，你现在心里有没有一个初步的判断或直觉？哪怕不成熟也没关系——你倾向于认为答案是什么？"

The point is to surface the author's pre-theoretical intuition. This becomes the thesis seed. Reassure the user: a good paper doesn't start from neutrality, it starts from a position that gets refined through research.

#### Phase 3: 现实关怀 — Why does it matter?

Ask the user to answer these four questions (can be one at a time):

1. **这个问题影响谁？** — Not "学术界", but real people: athletes, clubs, broadcasters, fans, regulators...
2. **如果不解决，会怎样？** — What concrete harm continues?
3. **如果解决了，会改变什么？** — What institutional practice would change?
4. **为什么是你来写？** — What about your background, experience, or position makes you the right person to address this?

#### Phase 4: 一句话主线 — The thread

Ask the user to try to state their core argument in one sentence:

> "试着用一句话概括你想在这篇论文中论证什么。格式可以是：'我认为……，因为……，所以应当……'"

If the user can't do it yet, that's fine — help them draft a tentative version and note that it will be refined. But this sentence becomes the "thread" (主线) that every subsequent stage checks against.

**Output: `SOUL_BRIEF.md`**

Write to the project root:

```markdown
# Soul Brief

## 真实问题 (The Real Problem)
[The specific contradiction or tension the author observed — in their own words]

## 初步判断 (Preliminary Judgment)
[The author's current position/intuition — what they think the answer might be]

## 现实关怀 (Real-World Stakes)
- **影响谁**: [who is affected]
- **不解决会怎样**: [what harm continues]
- **解决了会改变什么**: [what practice changes]
- **为什么是我**: [why this author]

## 一句话主线 (The Thread)
[One sentence: "I argue that... because... therefore..."]
(Status: tentative / confirmed — will be refined through Gates)

## 非写不可 (The Irreducible Core)
[What personal experience, puzzlement, or conviction drives this paper — what could only come from this author]
```

**Key rule**: `SOUL_BRIEF.md` is the author's voice. The AI may help refine the phrasing, but NEVER overwrite the substance. All downstream stages must read it and respect it.

---

### Stage 0: PRISM — Discipline Detection

Like a prism splitting white light into a spectrum — this stage takes a raw research direction and refracts it into discipline-specific methodology, literature sources, review criteria, and paper structure.

**If `DISCIPLINE` is set to a specific ID** (e.g., `law`, `economics`):
- Skip auto-detection (score = 1.0)
- Read the corresponding profile from `PROFILES_DIR/{DISCIPLINE}.md`
- Write `PRISM_PROFILE.md` to project root

**If `DISCIPLINE = auto`** (default), run the detection workflow:

#### Step 0.1: Gather Evidence

Collect text signals from multiple sources (in priority order):

1. **Explicit user input**: Parse `$ARGUMENTS` for discipline keywords or explicit `— discipline: law` override.
2. **RESEARCH_BRIEF.md**: If exists in project root, read `## Background > Discipline`, `## Background > Field` and `## Background > Sub-area`, plus the full Problem Statement.
3. **SOUL_BRIEF.md**: If exists (from Stage -1), use the "真实问题" section for discipline clues.
4. **CLAUDE.md**: Check for `## Discipline` or `## Field` section.
5. **Local wiki hints**: Check `## Local Wiki`, `## Wiki Root`, `## Knowledge Base`, or `## 知识库` entries in project files; wiki roots such as `sports-law-wiki` or `political-philosophy-wiki` are strong discipline signals.
6. **Project files**: Scan filenames and directory names for domain signals:
   - `.tex` files with `\usepackage{bluebook}` → law
   - filenames or notes mentioning 体育法, CAS, WADA, IOC, FIFA, sports governance, event broadcasting → sports-law
   - proof/derivation-heavy notes with `proof`, `lemma`, `theorem`, modal/deontic operators in section titles → logic
   - `stata`, `.do`, `.dta` files → economics/social-sciences
   - `SPSS`, `survey_data` → social-sciences
   - `.bib` files: scan venue names for discipline clues

#### Step 0.2: Score Disciplines

For each supported discipline, compute a match score based on:

- **Keyword density**: Count trigger keywords from the evidence text (see table below).
- **Venue match**: If a target venue is mentioned, match against discipline venue lists.
- **Explicit override**: If user specified `— discipline: X`, use that directly (score = 1.0).
- **Sub-field specificity**: Prefer more specific matches (e.g., `sports-law` over generic `law`, `logic` over generic `philosophy` when proof obligations dominate, `law` over generic `social-sciences`).

**Supported Disciplines and Trigger Keywords:**

| ID | Name | Trigger Keywords |
|----|------|-----------------|
| `communications` | Communications / Media Studies | media, journalism, communication, public opinion, framing, discourse, audience, platform, social media, 传播, 舆论 |
| `law` | Law / Legal Studies | law, legal, statute, precedent, court, jurisdiction, legislation, regulation, rights, liability, compliance, jurisprudence, doctrine |
| `sports-law` | Sports Law / Sports Governance | sports law, 体育法, CAS, WADA, IOC, FIFA, league rules, athlete rights, broadcasting rights, event data, 体育赛事, 竞赛规程 |
| `economics` | Economics / Finance | economics, econometrics, market, equilibrium, welfare, utility, game theory, mechanism design, causal inference, RCT, DID, IV, panel data |
| `social-sciences` | Social Sciences | sociology, political science, anthropology, psychology, survey, interview, ethnography, discourse analysis, qualitative |
| `humanities` | Humanities | history, literature, hermeneutics, textual analysis, close reading, critical theory, historiography, cultural studies, philology |
| `philosophy` | Philosophy (moral & political) | philosophy, ethics, metaethics, normative, moral, 道德哲学, 伦理学, justice, rights, deontology, consequentialism, virtue ethics, contractualism, reflective equilibrium, thought experiment, conceptual analysis, 政治哲学 |
| `logic` | Logic (formal & philosophical) | logic, 逻辑学, modal logic, deontic logic, proof theory, model theory, completeness, soundness, decidability, consequence relation, intuitionistic, paraconsistent, paradox, formalization, sequent calculus |
| `education` | Education Research | pedagogy, curriculum, classroom, student learning, assessment, instructional design, educational technology |
| `management` | Management / Business | organizational behavior, strategy, supply chain, marketing, entrepreneurship, innovation management, corporate governance |

#### Step 0.3: Select and Confirm

- If top score >= `CONFIDENCE_THRESHOLD` and clearly dominates (>= 2x second place): **auto-select**.
- If top score >= `CONFIDENCE_THRESHOLD` but close to second: **present top 2 and ask user**.
- If top score < `CONFIDENCE_THRESHOLD`: **ask user to specify**.
- For **interdisciplinary** research (two disciplines score similarly high): select the primary and note the secondary.
- If detection fails entirely and `AUTO_PROCEED=true`: default to `humanities`.

#### Step 0.4: Load Profile and Write Output

Read the corresponding profile from `PROFILES_DIR/{discipline_id}.md`.

Write `PRISM_PROFILE.md` to project root:

```markdown
# PRISM Profile

- **Discipline**: [Name]
- **ID**: [discipline_id]
- **Confidence**: [score]
- **Secondary Discipline**: [if interdisciplinary, otherwise "none"]
- **Detected From**: [source: user input / RESEARCH_BRIEF / SOUL_BRIEF / project files]
- **Detection Date**: [ISO 8601]

## Methodology Profile
[Copy the relevant sections from the loaded discipline profile]

## Venue Routing
[Copy venue tiers from the profile]

## Literature Sources
[Copy database priority from the profile]

## Paper Structure Template
[Copy paper structure from the profile]

## Review Dimensions
[Copy review scoring dimensions from the profile]

## Local Wiki Link
[If a local wiki root is detected or specified, record root path, mode, query command, and write-back policy. Otherwise "none".]
```

#### Step 0.5: Present to User

```
PRISM detected: [Name] (confidence: X%)
Secondary: [if any]
Source: [what triggered the detection]

Methodology: [1-line summary]
Top venues: [3-5 venues]
Literature databases: [primary sources]

Profile saved to PRISM_PROFILE.md.
```

**Output:** `PRISM_PROFILE.md` — consumed by all downstream stages.

**If `MODE=detect-only`**: Stop here. Return the detection result and exit.

After the profile is written, read `../shared-references/prism-routing.md` and apply the profile's **Recommended Pipeline Modules** if present. Do not paste other skill bodies into this file; invoke specialist skills conditionally and keep this skill as the orchestration layer.

If `LOCAL_WIKI_ROOT != false`, also read `../shared-references/local-wiki-link.md` and resolve the project-to-wiki link. Record the selected wiki root and mode in `PRISM_PROFILE.md` under `## Local Wiki Link`.

**Key rules for detection:**
- **Backward compatible**: If no discipline is detected and user doesn't specify, default to `humanities`.
- **User override always wins**: `— discipline: law` bypasses all detection logic.
- **Interdisciplinary support**: Law & Economics, Computational Social Science, Bioinformatics, etc. — pick the primary methodology and note the secondary.
- **Do not block the pipeline**: If detection is uncertain, pick the best guess and let the user correct at Gate 0.
- **Profile files are read-only references**: Never modify the discipline profile files themselves.

---

#### Gate 0 — 学科与方法论确认

**Trigger**: After `PRISM_PROFILE.md` is written.

**Purpose**: Let the user confirm or redirect the discipline detection, methodology paradigm, and target venue before committing to a discipline-specific pipeline.

**Present to user**:

1. Show the detected discipline, confidence score, methodology summary, and top venues
2. Generate 2-3 options:

| Option | Example for sports-law topic |
|--------|------------------------------|
| **A: 确认当前学科** | "体育法 (sports-law)，以体育治理规则与法律规范互动为方法论核心，目标期刊《体育科学》" |
| **B: 调整为相邻学科** | "法学 (law)，以传统法教义学为方法论核心，可投《法学研究》《法学》等法学核心期刊" |
| **C: 跨学科模式** | "体育法+法经济学，以法经济学分析体育治理问题，目标《体育科学》或《经济法学评论》" |

3. Each option should include:
   - Discipline ID and name
   - Methodology paradigm (1 sentence)
   - Literature databases that will be used
   - Target venue tiers (top 3)
   - How this choice shapes the entire downstream pipeline

**Soul dimension** (if `SOUL_PROTOCOL=true`): After the user selects, ask:
> "你在灵魂访谈中提到的那个真实困惑，用 [chosen discipline] 的方法论来回答，你觉得自然吗？还是需要跨学科才能说清楚？"

**After user selects**: Update `PRISM_PROFILE.md` if the user changed the discipline; log to `DECISION_LOG.md`.

---

### Stage 1a: Literature Survey

If `RESEARCH_BRIEF.md` exists in the project root, it will be automatically loaded as detailed context.

**Discipline-aware**: Use the databases and search strategies from `PRISM_PROFILE.md`.

**Soul-aware**: Before running the literature survey, read `SOUL_BRIEF.md` and use the author's "真实问题" and "初步判断" to focus the search. The literature survey should seek out:
- Papers that address the same tension the author identified
- Papers that take a position the author might disagree with (to sharpen the judgment)
- Papers that report the real-world stakes the author cares about

Invoke literature survey (the first sub-step of idea discovery):
```
/research-lit "$ARGUMENTS"
```

Specialist enrichment:
- If the profile recommends `multi-search` or `knowledge-synthesis`, use them for broad multi-topic source maps.
- If the profile is `law`, `sports-law`, or `humanities`, prefer `research-lit` / `semantic-scholar` over generic arXiv-first searches, and target the profile's sources (CNKI, 北大法宝, CAS, HeinOnline, JSTOR).
- If `LOCAL_WIKI_ROOT` resolves to an external wiki, query it before external search.

**Output:** Literature survey results with identified research gaps, debates, and trends.

---

#### Gate 1 — 研究抓手选择

**Trigger**: After the literature survey completes.

**Purpose**: The "research anchor" (研究抓手) is the specific angle, gap, or entry point through which the user enters the research problem. This is arguably the most creative and consequential decision in the entire pipeline. Different anchors lead to fundamentally different papers.

**Present to user**:

1. Summarize the literature landscape: key debates, gaps, and trends found
2. Generate 2-3 distinct research anchors, each representing a different entry point into the topic:

**Example for "体育赛事数据权益保护":**

| Option | Research Anchor | Entry Point Type |
|--------|----------------|-----------------|
| **A: 权利定性之争** | 体育赛事数据究竟是何种权利（知识产权/财产权/数据权益）？从权利性质的理论争议切入 | 理论争议型 |
| **B: 实践困境驱动** | 从体育数据商业化中的典型纠纷案例（如NBA v. Motorola）切入，分析现行法律保护的不足 | 案例驱动型 |
| **C: 比较法视角** | 从欧盟《数据法案》与美国体育数据立法实践的差异切入，为中国提供制度借鉴 | 比较法型 |

3. Each anchor option should explain:
   - **核心切入点**: What specific question or tension anchors the research
   - **为什么可行**: Why this angle has sufficient literature support and novelty space
   - **预期贡献**: What kind of contribution this anchor naturally leads to (theoretical, practical, institutional)
   - **下游影响**: How this anchor shapes the research question, methods, and paper structure

**Soul dimension** (if `SOUL_PROTOCOL=true`):

After presenting the options, add a soul-specific prompt:

> "回看你的灵魂访谈：你最初的困惑是'[quote from SOUL_BRIEF.md 真实问题]'。哪个抓手最能让你直面这个困惑？不是哪个最容易发表，而是哪个最让你有话想说？"

If none of the generated anchors match the author's genuine concern, explicitly offer:
> **Option D: 你自己的抓手** — "如果上面的选项都不对，请直接告诉我你想从哪里切入。你的真实困惑本身可能就是最好的抓手。"

**After user selects**: Record the chosen anchor; this becomes the guiding thread for idea generation in Stage 1b.

---

### Stage 1b: Research-Question Formulation & Validation

Using the user's chosen research anchor and the literature from Stage 1a, formulate candidate research questions / theses, then validate them:

```
1. Draft 3–6 candidate research questions or theses grounded in the Stage 1a literature
   and the author's chosen anchor (read SOUL_BRIEF.md first).
2. /novelty-check [candidate questions]   → screen for genuine contribution vs. settled debate
3. /research-review [top candidates]       → external critical read before committing
```

**Soul-aware**: When formulating research questions, read `SOUL_BRIEF.md` and ensure each candidate:
- Address the author's stated "真实问题", not a sanitized version of it
- Allow space for the author's "初步判断" to be tested (not predetermined to be confirmed or refuted)
- Have clear "现实关怀" — each idea must answer "so what?" for real people

**Output:** `idea-stage/IDEA_REPORT.md` with ranked, validated ideas aligned to the user's chosen anchor.

---

#### Gate 2 — 研究题目与核心问题确认

**Trigger**: After `idea-stage/IDEA_REPORT.md` is generated.

**Purpose**: Let the user finalize the research topic, title, and core research question(s). This is the "what are we writing about" decision.

**Present to user**:

1. Show the top 2-3 ideas from the IDEA_REPORT, each with:
   - Proposed paper title (中文 + 英文)
   - Core research question (1-2 sentences)
   - Sub-questions (2-3 supporting questions)
   - Novelty assessment (from `/novelty-check`)
   - Feasibility assessment

**Example for anchor "权利定性之争":**

| Option | Title | Core Question |
|--------|-------|---------------|
| **A** | 《体育赛事数据的权利属性与法律保护路径研究》 | 体育赛事数据应被纳入何种权利范畴？现有知识产权法、反不正当竞争法与数据立法如何协调保护？ |
| **B** | 《数据要素化背景下体育赛事数据权益的类型化保护》 | 在数据作为生产要素的政策背景下，体育赛事数据权益应如何进行类型化区分并设计差异化保护机制？ |
| **C** | 《体育赛事数据权益保护的法经济学分析》 | 从效率与激励的视角，体育赛事数据的最优产权配置与保护强度应如何确定？ |

2. Each option should preview:
   - **研究问题链**: Core question → sub-questions → specific analysis targets
   - **预期创新点**: What novel contribution this framing enables
   - **适合期刊**: Which venues this framing best suits

**Soul dimension** (if `SOUL_PROTOCOL=true`):

After the user selects a topic, conduct a soul check:

> **判断确认**: "你选了这个题目。现在，抛开学术话语，用大白话说一说：关于这个问题，你自己的观点是什么？你倾向于什么样的结论？这个观点可能是错的吗？"

Record the user's answer in `SOUL_BRIEF.md` under `## 初步判断`, refining the earlier tentative version. Then ask:

> **现实关怀确认**: "这篇论文写完之后，你希望它能改变什么？是让法官判案时有一个更好的依据？还是让立法者注意到一个被忽视的问题？还是让从业者改变某种做法？"

Record in `SOUL_BRIEF.md` under `## 现实关怀`.

> **主线更新**: Based on the user's answers, help them refine the "一句话主线". Ask: "现在能不能重新试一下那句话：'我认为……，因为……，所以应当……'"

Update `SOUL_BRIEF.md` with the refined thread. Mark status as `confirmed` if the user is satisfied.

**After user selects**: Record the title and research question; initialize `RESEARCH_PLAN.md` with the confirmed topic. If `FUNDING_TRACK=true`, branch to `/grant-proposal` at this point.

---

### Stage 2: Research Route & Methodology Design

Once the research topic is confirmed, design the research route and methodology.

**Before execution, two more gates let the user shape the "how".**

---

#### Gate 3 — 研究路线选择

**Trigger**: After topic confirmation (Gate 2).

**Purpose**: Define the overall research roadmap — the logical progression from problem statement to conclusion. Different routes structure the paper's argument flow differently.

**Present to user**:

1. Based on the confirmed topic and discipline profile, generate 2-3 alternative research routes:

**Example for "体育赛事数据的权利属性与法律保护路径研究":**

| Option | Research Route | Argument Flow |
|--------|---------------|---------------|
| **A: 规范分析路线** | 法律概念界定 → 现行法评析 → 比较法考察 → 制度建构 | 从"是什么"到"应该是什么"的规范推进，适合法教义学论文 |
| **B: 案例实证路线** | 典型案例梳理 → 裁判规则提炼 → 问题诊断 → 制度回应 | 从实践到理论再到制度的归纳推进，适合实证法学论文 |
| **C: 法经济学路线** | 经济学模型构建 → 激励结构分析 → 效率评估 → 最优制度设计 | 从理论模型到制度建议的演绎推进，适合交叉学科论文 |

2. Each route option should include:
   - **逻辑主线**: The main logical thread from start to conclusion (4-6 steps)
   - **关键论证节点**: The 2-3 most important analytical steps
   - **数据/素材需求**: What materials are needed (cases, statutes, data, interviews...)
   - **预计章节结构**: Rough chapter/section outline this route naturally produces
   - **风险提示**: What could go wrong with this route (data availability, argumentation gaps)

**Soul dimension** (if `SOUL_PROTOCOL=true`):

**Thread check** — After the user selects a route, verify coherence:

> "你的主线是'[quote 一句话主线 from SOUL_BRIEF.md]'。我们来检查一下：这条路线的每一步是否都在为这个论证服务？"

Walk through each step of the chosen route and ask: "这一步和你的主线是什么关系？" If any step can't be clearly connected, flag it and discuss whether to adjust the route or the thread.

**After user selects**: Record the chosen route and its logical progression; this shapes both the methodology gate and the paper structure.

---

#### Gate 4 — 研究方法确认

**Trigger**: After research route is chosen (Gate 3).

**Purpose**: Confirm the specific research methods, data sources, and analytical tools. This is the "with what tools" decision.

**Present to user**:

1. Based on the chosen route, generate 2-3 methodology combinations:

**Example for "规范分析路线":**

| Option | Method Combination | Key Tools |
|--------|-------------------|-----------|
| **A: 纯法教义学** | 法律解释 + 体系化分析 + 比较法（德日欧美） | 法规数据库（北大法宝、Westlaw）、立法资料、学说梳理 |
| **B: 法教义学+实证补充** | 法律解释为主 + 司法案例统计分析为辅 | 法规数据库 + 裁判文书网数据抓取 + 案例编码分析 |
| **C: 法教义学+法经济学** | 法律解释为主 + 经济学激励分析框架为辅 | 法规数据库 + 博弈论/产权理论模型 + 域外制度效果数据 |

2. Each option should specify:
   - **核心方法**: Primary and secondary research methods
   - **数据来源**: Specific databases, case libraries, datasets to use
   - **分析工具**: Software, frameworks, or analytical models
   - **技能要求**: What the researcher needs to know or learn
   - **产出形态**: What the analysis produces (tables, models, case summaries, comparative matrices...)

**Soul dimension** (if `SOUL_PROTOCOL=true`):

> "你选的方法能不能让你说出你想说的话？比如，如果你的判断是'现行法保护不足'，这个方法能为这个判断提供充分的证据支持吗？还是只能描述现状而无法做出评价？"

**After user selects**: Finalize `RESEARCH_PLAN.md` with the complete research design (topic + route + methods). Proceed to execution.

---

### Stage 2-exec: Research Execution

Once all design gates are cleared, build the evidence base according to the chosen approach:

1. Read `RESEARCH_PLAN.md` with the user's confirmed route and methods
2. Build the research framework:
   - **Sports Law**: Build legal issue map, statutes/cases/rules list, CAS or sports-governance materials, and comparative matrix
   - **Law**: Draft doctrinal analysis structure, identify statutes and cases, prepare comparative law matrix
   - **Philosophy**: Reconstruct the argument, formalize key inferences, build the objection/response map
   - **Logic**: Normalize notation, state assumptions, build the theorem/derivation dependency map and proof obligations
   - **Economics**: Assemble dataset, specify the empirical/identification strategy, prepare the analysis write-up
   - **Social Sciences / Education**: Design research instrument, prepare coding scheme, draft interview/intervention protocol
   - **Management / Communications**: Assemble case or corpus, develop the analytical framework
   - **Humanities**: Compile source corpus, develop analytical framework, begin close reading
3. Execute preliminary analysis and document findings in `RESEARCH_LOG.md`

### Stage 3: Develop the Evidence Base

Execute the research plan:
- Compile doctrinal/case analysis, run the empirical analysis, or conduct textual/conceptual analysis as the discipline requires
- Document all intermediate findings in `RESEARCH_LOG.md`
- Collect the supporting evidence for each claim in the research plan

### Stage 3.5: Evidence and Integrity Gates

Run only when `QUALITY_GATES != off`. Treat failures as advisory under `standard`; under `strict`, stop before Stage 4/6 until critical failures are fixed.

- **Law / sports law**: Run `statute-case-mapper` to ground claims, `comparative-law` for functional comparison, `argument-stress-test` for doctrinal/normative argument gaps, then `citation-audit` (L3) for legal source-to-claim checks.
- **Philosophy / logic (formal)**: Run `/proof-checker` on theorem/proof files; use `/formula-derivation` when assumptions or derivation targets are still unstable.
- **Philosophy / logic (argumentative) & humanities**: Run `argument-stress-test` to check inferential validity and engagement with objections.
- **Social sciences / economics / education / management (empirical)**: Run `/paper-claim-audit` to check that manuscript claims are supported by the cited sources and reported data.
- **All disciplines**: Update `/research-wiki` with accepted claims, rejected claims, evidence gaps, and follow-up tasks when wiki mode is enabled.
- **External wiki**: When `LOCAL_WIKI_MODE=read-write`, write durable research memos or backlinks to the linked local wiki only for stable, reusable outputs; never modify `raw/` source files.

**Soul-aware evidence check** (if `SOUL_PROTOCOL=true`):

After the evidence gates run, conduct a soul-evidence alignment check:

> Read `SOUL_BRIEF.md` and compare the author's "初步判断" against the evidence collected. Present a brief report:
> - **判断得到支持的部分**: Where the evidence supports the author's intuition
> - **判断需要修正的部分**: Where the evidence challenges the author's position
> - **新发现**: Unexpected findings that might enrich the argument
>
> Ask the user: "研究结果和你最初的判断有出入吗？你的主线需要调整吗？"
>
> If the user wants to adjust, update `SOUL_BRIEF.md` — especially the "一句话主线" and "初步判断". This is not a failure; it's intellectual honesty.

### Stage 4: Critical Review

Get a critical external read of the developed argument/manuscript:

```
/research-review "$ARGUMENTS — [chosen thesis title]"
```

**Discipline-aware**: The reviewer uses the discipline's review dimensions from `PRISM_PROFILE.md`. For example:
- **Law reviewer**: Scores on doctrinal rigor, argument quality, comparative depth, practical relevance
- **Philosophy reviewer**: Scores on argument validity, engagement with objections, conceptual clarity, originality
- **Economics / social-science reviewer**: Scores on identification/method, robustness, data/source quality, policy relevance

If `HUMAN_CHECKPOINT=true`, pause after the review and summarize key issues for the user. For a deeper pass, re-run `/research-review` or hand specific claims to `/argument-stress-test`.

**Output:** `review-stage/RESEARCH_REVIEW.md`.

### Stage 5: Research Summary & Writing Handoff

Generate `NARRATIVE_REPORT.md` with discipline-appropriate content:
- Problem statement and core claim
- Method / analytical framework summary
- Key results with evidence for each claim
- Evidence gate results and unresolved risks
- Figure/table inventory
- Limitations and remaining follow-up items

---

#### Gate 5 — 论文框架确认

**Trigger**: After `NARRATIVE_REPORT.md` is generated, before paper writing.

**Purpose**: Let the user finalize the paper's structural blueprint before drafting begins. The paper structure determines argument flow, emphasis, and page allocation.

**Present to user**:

1. Based on the research results, the chosen route, and the discipline profile, generate 2-3 paper structure options:

**Example for a sports-law paper using the 规范分析 route:**

| Option | Structure | Emphasis |
|--------|-----------|----------|
| **A: 经典五章法学结构** | 引言 → 概念界定与理论基础 → 域外考察与比较分析 → 中国现行法评析与问题诊断 → 制度完善建议 → 结论 | 平衡理论与实践，适合综合性法学期刊 |
| **B: 问题导向四章结构** | 引言(问题提出) → 体育赛事数据保护的现实困境 → 困境成因的法理分析 → 保护路径的制度构建 → 结论 | 问题驱动，适合强调实践意义的期刊 |
| **C: 比较法主导结构** | 引言 → 美国模式分析 → 欧盟模式分析 → 中国现状与借鉴 → 本土化制度方案 → 结论 | 比较法为主线，适合国际视野的法学期刊 |

2. Each option should include:
   - **章节大纲**: Full section/subsection outline with tentative sub-headings
   - **页面分配**: Approximate page allocation per section
   - **论证重心**: Where the main analytical weight falls
   - **创新点呈现**: Where and how the novel contribution appears in the structure
   - **适配期刊**: Which venues this structure best serves

**Soul dimension** (if `SOUL_PROTOCOL=true`):

**Thread audit** — For each proposed structure, annotate every section with its relationship to the "一句话主线":

```
章节                          与主线的关系
引言                          提出主线：[quote thread]
概念界定                      为主线的核心概念奠基
域外考察                      为主线提供比较法支撑
中国现行法评析                直接论证主线（主战场）
制度建议                      主线的制度落地
结论                          收束主线
```

Ask the user: "每一章都和你的主线有清晰的关系吗？有没有哪一章你觉得'必须有但说不清为什么'？那可能是需要砍掉的部分。"

**"非写不可"确认**:

> "你的论文里，最关键的那个独属于你的洞见，应该放在哪一章？哪个部分是你最想写的、最有话说的？那个部分要给足篇幅。"

Record the user's answer. During Stage 6, ensure the identified section gets priority attention and sufficient space.

**After user selects**: Finalize `PAPER_PLAN.md` with the confirmed structure. Proceed to paper writing.

---

### Stage 6: Paper Writing (Workflow 3 — with Soul Audit)

**Skip if `AUTO_WRITE=false` (default) and user does not request it.**

When invoked, the paper writing pipeline uses `PRISM_PROFILE.md`, `PAPER_PLAN.md`, and `SOUL_BRIEF.md` for:
- The user-confirmed paper structure from Gate 5
- Correct citation style — **中文法学/社科期刊使用脚注或尾注格式，详见 `../shared-references/citation-cn-footnote.md`**；国际期刊使用 Bluebook / APA / OSCOLA / natbib / IEEE
- Discipline-appropriate evidence presentation
- Venue-specific formatting (中文期刊输出中文内容，国际期刊输出英文)
- **The author's voice and judgment from SOUL_BRIEF.md**

**中文论文引用规则**:
- 法学类中文期刊（法学研究、中国法学、中外法学等）: 脚注（页下注），格式见 `citation-cn-footnote.md`
- 体育学类中文期刊（体育科学、体育与科学等）: 尾注（参考文献表），顺序编码制 GB/T 7714-2015
- 法律法规、司法解释、案例、CAS裁决: 专用格式见 `citation-cn-footnote.md`
- 重复引用使用"同上注""前引注X"简写规则
- 以目标期刊投稿须知为最终标准

```
/paper-writing "NARRATIVE_REPORT.md" — venue: $VENUE
```

#### Soul-Aware Writing Process (for humanities/social sciences)

When `SOUL_PROTOCOL=true`, paper writing follows a **section-by-section drafting + pruning** process instead of bulk generation:

**For each major section:**

1. **Draft the section** using research materials, following the user's chosen route and methods.

2. **Inject the author's voice**: Before finalizing, check `SOUL_BRIEF.md`:
   - Does this section reflect the author's "初步判断"? If the section is purely descriptive where the author has a position, flag it.
   - For the section identified as "非写不可" in Gate 5, ensure it carries the author's genuine insight, not just a literature summary.

3. **Pruning checkpoint** — After each section draft, ask the user 3 questions:

   > **推进检验**: "这一节在推进你的核心论点吗？还是只是在展示你读了很多文献？"
   >
   > **必要性检验**: "如果删掉这一节，你的论证链会断吗？如果不会断，这一节的作用是什么？"
   >
   > **主线检验**: "这一节和你的主线'[quote thread]'是什么关系？用一句话说。"

   Based on the user's answers:
   - If the section is padding → cut or compress significantly
   - If the section is supportive but not essential → compress to minimum
   - If the section is core to the argument → keep and potentially expand

4. **Record the pruning decision** in `DECISION_LOG.md`.

**After all sections are drafted**: Run a full thread audit — read the entire draft and verify that the "一句话主线" is visible and coherent from introduction to conclusion.

### Stage 7: Submission Quality Gates, Soul Audit, and Side Tracks

After a draft exists, run quality gates and the final soul audit:

#### Soul Audit (Final Check)

**Skip if `SOUL_PROTOCOL=false`.**

Before submission, conduct a final soul audit by re-reading `SOUL_BRIEF.md` and the completed draft. Present a report to the user:

```markdown
## Soul Audit Report

### 1. 真实问题 ✓/✗
你最初的困惑是：[quote]
论文是否直面了这个困惑？还是绕开了最难的部分？

### 2. 自己的判断 ✓/✗
你的立场是：[quote]
论文中你的判断是否清晰可辨？还是被"客观中立"的学术话语稀释了？

### 3. 主线贯穿 ✓/✗
你的主线是：[quote]
每一章是否都在服务这条主线？有没有离题的章节？

### 4. 现实关怀 ✓/✗
你说这个问题影响 [who]，论文中这种关怀是否具体而非空泛？
读者读完后能否感受到"这确实是个重要问题"？

### 5. 反思与取舍 ✓/✗
有没有可以进一步压缩的段落？
有没有"放在那里显得有学问但其实不推进论证"的部分？

### 6. 非写不可 ✓/✗
论文中是否有至少一个段落，只有你能写出来——
因为你的经历、你的困惑、你的洞察？
```

If any dimension fails, discuss with the user how to fix it before submission. This audit is advisory — the user decides whether to act on it.

#### Standard submission gates

- **Submission audit**: `/citation-audit` for bibliography integrity; `/paper-claim-audit` for paper-to-evidence fidelity; `/paper-compile` for LaTeX/PDF verification.
- **Iterative polish**: `/research-refine` only after the evidence/citation gate is clean enough to improve wording rather than hide defects.
- **Funding track**: `/grant-proposal` branches from a validated idea or review-ready proposal; it is parallel to the publish track, not a default pipeline step.
- **Post-submission**: `/rebuttal` for reviewer responses; `/paper-slides` and `/paper-poster` for presentation artifacts; `/overleaf-sync` for collaborator handoff.

## Decision Gate Protocol

Every gate follows the same interaction pattern:

### Gate Interaction Pattern

1. **Present current state**: Summarize what the pipeline has produced so far.
2. **Analyze alternatives**: Generate 2-3 distinct, viable options based on the discipline's methodology profile and the evidence gathered.
3. **Compare trade-offs**: For each option, explain:
   - Core approach and what makes it distinctive
   - Strengths and risks
   - Downstream impact on later stages (what changes if this option is chosen)
   - Estimated scope/difficulty
4. **Soul check** (if `SOUL_PROTOCOL=true`): Add the gate's soul-specific question — connecting the decision back to the author's genuine concern.
5. **Ask the user**: Use `AskUserQuestion` to present options with clear labels, descriptions, and preview content showing the concrete plan for each option.
6. **Record decision**: Write the user's choice and rationale to `DECISION_LOG.md` (append mode).
7. **Adapt downstream**: All subsequent stages read `DECISION_LOG.md` and `SOUL_BRIEF.md`, and adjust their behavior according to the user's accumulated decisions.

### Decision Log Format

Maintain `DECISION_LOG.md` in the project root. Append after each gate:

```markdown
## Gate [N]: [Gate Name]
- **Date**: [ISO 8601]
- **Options Presented**: [brief list]
- **User Choice**: [selected option]
- **User Notes**: [any additional input from user]
- **Soul Check Response**: [user's response to soul question, if applicable]
- **Downstream Impact**: [how this affects later stages]
```

### Skipping Gates

- If `INTERACTIVE_MODE=lite`: Only Gates 2, 3, 5 pause. Gates 0, 1, 4 auto-select the top option and log the decision.
- If `INTERACTIVE_MODE=off` or `AUTO_PROCEED=true`: All gates auto-select the top option and log the decision.
- The user can always say "skip" or "auto" at any gate to let the pipeline choose for them from that point forward.
- **Soul Interview is never skipped** when `SOUL_PROTOCOL=true`, regardless of `INTERACTIVE_MODE`.

## Output Protocols

> Follow these shared protocols for all output files:
> - **[Output Versioning Protocol](../shared-references/output-versioning.md)** — write timestamped file first, then copy to fixed name
> - **[Output Manifest Protocol](../shared-references/output-manifest.md)** — log every output to MANIFEST.md
> - **[Output Language Protocol](../shared-references/output-language.md)** — respect the project's language setting

## Key Rules

- **SOUL_BRIEF.md is the author's voice**: The AI may help refine phrasing, but NEVER overwrite the substance of the author's stated problem, judgment, or concern. When in doubt, quote the user's own words.
- **User decisions drive the pipeline**: The user's choices at each gate are binding. All downstream stages must respect accumulated decisions in `DECISION_LOG.md`.
- **Never skip a gate silently**: If `INTERACTIVE_MODE=full`, every gate MUST use `AskUserQuestion` to present options. If the tool is unavailable, present options as text and wait for user response.
- **Options must be genuinely distinct**: Each gate must offer substantively different alternatives, not minor variations. Options should lead to meaningfully different downstream paths.
- **Respect the user's expertise**: Present trade-offs honestly. Do not steer the user toward a predetermined choice. The "recommended" label should reflect genuine analytical assessment, not default behavior.
- **Decision log is cumulative**: Each gate reads all prior decisions. Gate 3 (research route) must be consistent with Gate 1 (research anchor) and Gate 2 (topic). If a later decision contradicts an earlier one, flag the inconsistency and ask the user to resolve it.
- **Pruning is a feature, not a bug**: During soul-aware writing, cutting content is encouraged. A shorter, tighter paper with a clear thread is better than a comprehensive survey that says nothing.
- **The author's judgment must be visible**: For humanities and social sciences, a paper that merely describes without taking a position is incomplete. The Soul Protocol exists to ensure the author's voice survives the writing process.
- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.
- **PRISM Profile is the single source of truth** for all discipline-specific behavior. Every stage reads it.
- **Local wiki link is a knowledge bridge**: Read from the linked local wiki early, write back only durable pages/memos, and keep project-specific temporary artifacts in the project directory.
- **Keep PRISM as an orchestrator**: Do not inline entire specialist skills; call them when the profile or artifact state justifies it.
- **Specialist skills are optional**: First invoke a named slash skill if available. If unavailable, search local skill roots (`.claude/skills`, `.codex/skills`, `.agents/skills`, `Prism-H/skills`) for `*/SKILL.md`, read the matching workflow as a reference, and execute the closest equivalent. If no match exists, fall back to the generic stage and record the limitation.
- **Quality gates protect claims**: Never let paper writing turn failed, partial, or unaudited evidence into strong claims.
- **If Stage 4 ends at round 4 without positive assessment**, stop and report remaining issues.
- **Budget awareness**: Track resource usage across the pipeline (database/archive access, interview hours, translation or transcription costs).
- **Fail gracefully**: If any stage fails, report clearly and suggest alternatives.
- **Profile-driven**: If `PRISM_PROFILE.md` is missing, fall back to `humanities` defaults. If `INTERACTIVE_MODE=off` and `SOUL_PROTOCOL=false`, behavior is the non-interactive pipeline.

## Composing with Other Skills

```
/prism-pipeline "topic"                        → full pipeline with PRISM + Soul Protocol (you are here)
/prism-pipeline "topic" — mode: detect-only    → discipline detection only (outputs PRISM_PROFILE.md and stops)
/research-pipeline "topic"                     → full pipeline without the Soul Protocol layer
/research-lit "topic"                          → literature review only
/paper-writing "report"                        → paper writing only
/grant-proposal "idea"                         → funding branch after idea validation
/citation-audit "paper/"                       → submission citation integrity gate
/paper-claim-audit "paper/"                    → submission evidence-fidelity gate
/research-wiki init/query                      → persistent research graph
```
