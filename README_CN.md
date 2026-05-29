# Prism-H 📚⚖️

**面向人文社科的 Prism** —— 适用于 Claude Code（以及 Codex CLI、Cursor、Trae 等 agent）的学科感知研究流水线。

🤖 **AI agent：** 请改读 [`AGENT_GUIDE.md`](AGENT_GUIDE.md)，那是为 LLM 阅读组织的结构化版本。

![Prism Logo](docs/prism_logo.svg)

[English README](README.md) | 中文

> 🪶 **极致轻量、零依赖、零锁定。** 每个技能都是一份纯 Markdown 的 `SKILL.md`，没有框架、没有数据库、没有 Docker。把 Claude Code 换成 [Codex CLI](skills/skills-codex/) 或别的 agent，工作流照样跑。
>
> *💡 Prism-H 是一套方法论，不是一个平台。把工作流带到你想去的任何地方。* 🌱

Prism-H 是 [Prism](https://github.com/catalsqlb-cmd/Prism) 的人文社科专版。它保留了「文献 → 研究问题 → 证据 → 评审 → 成稿」的研究生命周期与跨模型评审闭环，但移除了所有与计算实验相关的部分（GPU 跑实验、机器学习选题自动化、专利撰写）。剩下的全部针对**教义学、论证型、质性以及实证社科研究**做了调校。

这些技能编排**跨模型协作**：Claude Code 负责推进研究，外部 LLM（经 [Codex MCP](https://github.com/openai/codex)）担任批判性评审 —— **速度 × 严谨**。

## 🎓 支持的学科

PRISM 自动识别会写出一份 `PRISM_PROFILE.md`，据此为每个学科适配文献来源、证据标准、论文结构、引注体例与评审维度：

| ID | 学科 |
|----|------|
| `law` | 法学 |
| `sports-law` | 体育法 / 体育治理 |
| `philosophy` | 哲学（侧重道德与政治哲学） |
| `logic` | 逻辑学（形式逻辑与哲学逻辑） |
| `economics` | 经济学 / 金融 |
| `social-sciences` | 社会科学 |
| `education` | 教育学 |
| `management` | 管理学 / 商科 |
| `communications` | 传播学 / 媒介研究 |
| `humanities` | 人文学科（默认兜底） |

## 🚀 快速开始

**全流程** —— 给 Prism-H 一个研究方向，它端到端跑完整个生命周期：

```
/prism-pipeline "兴奋剂裁决中运动员获得公正程序的权利"
```

`/prism-pipeline` 额外带有 **Soul Protocol**（一段简短的作者访谈 + 人工把关节点 + 最终的文风审计）。若只要相同的阶段、**不要**访谈层，请用：

```
/research-pipeline "兴奋剂裁决中运动员获得公正程序的权利"
```

也可以**逐阶段**直接调用各个技能：

```
/research-lit "主题"                    # 文献综述（Zotero / Obsidian / 网络 / Semantic Scholar）
/research-refine "问题 … | 论点 …"       # 打磨研究问题 / 论点
/statute-case-mapper "主张"             # （法学）主张 → 实证法 / 案例 / CAS 裁决 映射
/comparative-law "X 与 Y 之间的某议题"   # （法学）功能比较法
/argument-stress-test "主张"            # 论证健全性对抗闸门
/research-review "论点"                 # 学科感知的批判性评审
/citation-audit                         # 投稿前核验参考文献
/paper-writing "RESEARCH_LOG.md"        # 规划 → 写作 → 编译
```

## 🔁 流水线

```
PRISM 识别 → /research-lit → 研究问题拟定 → 发展证据 → /research-review → /paper-writing（可选）
```

- **发展证据** 指各学科所要求的形态：带实证法/案例/规则的法律争点图与比较矩阵；带反驳/回应图的论证重构；带分析框架的史料语料库；或带分析撰写的数据集 / 问卷 / 访谈 / 编码方案。
- **质量闸门**（默认仅作建议，`strict` 下为阻断）：法学用 `statute-case-mapper` / `comparative-law` / `argument-stress-test` / `citation-audit`；形式逻辑用 `proof-checker` / `formula-derivation`；论证型工作用 `argument-stress-test`；实证社科用 `paper-claim-audit`。

## 🧩 支线

- **基金** —— `/grant-proposal` 从一个已验证的研究问题分叉而出。
- **投稿回应** —— `/rebuttal` 消化外部评审意见（绝不编造证据）。
- **演示** —— `/paper-slides`、`/paper-poster` 消费已编译、已审计的论文。
- **协作** —— `/overleaf-sync` 仅作为传输层。
- **记忆** —— `/research-wiki` 与可移植的 [LLM-Wiki](skills/llm-wiki/) 持久化来源、论证与评审结论。

## 🛠️ 安装

推荐方式（项目级软链接）：

```bash
bash tools/install_prism.sh /path/to/your/project
```

安装时一并搭建个人知识库：

```bash
bash tools/install_prism.sh /path/to/your/project --with-wiki /path/to/wiki
```

每个技能会被软链接到 `<project>/.claude/skills/<skill-name>`；`<project>/.prism/installed-skills.txt` 中的清单记录每一条受管链接，卸载时绝不触碰你自己的同名技能。

## 📝 引注体例

Prism-H 内置了人文社科作者真正会投的体例路由：中文法学与社科期刊用脚注/尾注，美国法用 Bluebook，英国/欧盟法用 OSCOLA，社会科学用 APA，人文学科用 Chicago。法律引注精确到条/款/项、含完整案号、CAS 裁决用标准格式。详见 [`citation-cn-footnote.md`](skills/shared-references/citation-cn-footnote.md) 与 [`citation-discipline.md`](skills/shared-references/citation-discipline.md)。

## 🔑 核心规则

- **以画像为准** —— 每个阶段都读 `PRISM_PROFILE.md`；缺失时回落到人文学科默认配置。
- **不编造证据** —— 主张必须可追溯到扎实的来源、案例、数据或有效论证。
- **跨模型评审** —— 执行者与评审者是不同的模型，评审者会主动探测执行者看不见的盲点。

## 📄 许可

MIT。派生自 [Prism](https://github.com/catalsqlb-cmd/Prism) 并裁剪至人文社科。
