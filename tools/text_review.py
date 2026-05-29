#!/usr/bin/env python3
"""Prism-H deterministic text-review lint (确定性文本评估引擎).

A cheap, model-free pre-check for academic prose. It uses regex / template
matching to catch deterministic problems BEFORE you spend tokens on a
cross-model adversarial review (`/argument-stress-test`, `/research-review`).

The philosophy: a model checking its own output is no check at all. These
rules are dumb but reliable — they find the classes of defect that humanities
& social-science drafts repeatedly exhibit:

  R-series  credibility   vague citations, fabricated/future years, over-assertion
  T-series  terminology   one concept rendered with several Chinese translations
  F-series  format        empty footnotes, missing GB/T 7714 type tags, punctuation
  S-series  register      colloquialisms, inconsistent self-reference
  ST-series structure     missing abstract/keywords/refs, no thesis sentence
  L-series  argument      "assert-without-argue", "list-without-advance",
                          quotation-without-analysis, unsupported premises,
                          narrative drowning analysis, intensifiers without evidence

The L-series is the highest-value part: it is a deterministic proxy for the
argumentative-soundness defects that `/argument-stress-test` probes with a
model. Run this first; escalate the survivors to the model.

Usage:
    python tools/text_review.py paper.md
    python tools/text_review.py paper.md --severity error
    python tools/text_review.py paper.md --format json
    python tools/text_review.py chapter1.md chapter2.md   # multiple files

Adapted for Prism-H from ganzhi-black/humanities-thesis-skill (MIT).
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    ERROR = "error"      # must fix: fabricated refs, broken format
    WARNING = "warning"  # should fix: inconsistent terms, register
    INFO = "info"        # optional: notice / polish


@dataclass
class Issue:
    rule: str
    severity: Severity
    message: str
    line: int = 0
    context: str = ""
    suggestion: str = ""

    def to_dict(self) -> dict:
        return {
            "rule": self.rule,
            "severity": self.severity.value,
            "message": self.message,
            "line": self.line,
            "context": self.context[:100] if self.context else "",
            "suggestion": self.suggestion,
        }


# ═══════════════════════════════════════════════════════
# 1. Credibility (R-series)
# ═══════════════════════════════════════════════════════

def check_fabricated_references(text: str) -> list[Issue]:
    """Detect probable fabricated / vague citations."""
    issues: list[Issue] = []
    current_year = datetime.date.today().year
    for i, line in enumerate(text.split("\n"), 1):
        for _ in re.findall(r"(有学者|有研究者|有人|据研究)(指出|认为|发现|表明|提出)", line):
            issues.append(Issue(
                rule="R1-01", severity=Severity.ERROR,
                message="模糊引用：使用了「有学者指出」类表述但未给出具体文献",
                line=i, context=line.strip()[:80],
                suggestion="替换为具体的作者名+出处，或删除这个引用",
            ))
        if "[待补充" in line or "[待查证" in line:
            issues.append(Issue(
                rule="R1-02", severity=Severity.INFO,
                message="发现待补充占位符，提交前需要补充具体信息",
                line=i, context=line.strip()[:80],
            ))
        for year_str in re.findall(r"[（(]\s*((?:19|20)\d{2})\s*[)）]", line):
            if int(year_str) > current_year + 1:
                issues.append(Issue(
                    rule="R1-03", severity=Severity.ERROR,
                    message=f"引用年份 {year_str} 超过当前年份（{current_year}），可能是编造的",
                    line=i, context=line.strip()[:80],
                ))
    return issues


def check_unsupported_claims(text: str) -> list[Issue]:
    """Detect over-assertion: absolutes without qualification."""
    issues: list[Issue] = []
    patterns = [
        (r"毫无疑问", "建议改为「可以认为」或「有理由认为」"),
        (r"众所周知", "建议改为「学界普遍认为」并附引用"),
        (r"不言而喻", "学术论文中应当明确论证，而非诉诸不言而喻"),
        (r"显而易见", "建议改为「从以上分析可以看出」"),
        (r"必然", "建议改为「很可能」或「在很大程度上」，除非有充分论证"),
        (r"完全(?:是|证明了|说明了)", "建议加入限定词，避免绝对化"),
        (r"无可辩驳", "学术论文中应避免此类修辞"),
    ]
    for i, line in enumerate(text.split("\n"), 1):
        for pattern, suggestion in patterns:
            m = re.search(pattern, line)
            if m:
                issues.append(Issue(
                    rule="R3-01", severity=Severity.WARNING,
                    message=f"过度断言：使用了「{m.group()}」",
                    line=i, context=line.strip()[:80], suggestion=suggestion,
                ))
    return issues


# ═══════════════════════════════════════════════════════
# 2. Terminology consistency (T-series)
# ═══════════════════════════════════════════════════════

# Concept groups where mixing translations signals inconsistency. Seeded for
# the humanities theory canon plus terms relevant to law / moral philosophy.
_SYNONYM_GROUPS = [
    ["赤裸生命", "裸命", "裸生命"],
    ["灵晕", "灵韵", "灵光"],
    ["延异", "延差", "分延"],
    ["规训", "训诫", "纪律"],
    ["操演性", "述行性", "展演性"],
    ["话语", "论述"],
    ["异托邦", "异质空间", "异质地方"],
    ["解域化", "去疆域化", "去辖域化"],
    ["询唤", "质询", "召唤"],
    ["主体化", "主体建构", "主体构成"],
    # law / governance / moral philosophy
    ["正当程序", "正当法律程序", "法律正当程序"],
    ["比例原则", "比例性原则"],
    ["相称性", "相称原则", "比例相称"],
    ["可证立性", "可证成性", "可辩护性"],
    ["道德运气", "道德运"],
]


def check_terminology_consistency(text: str) -> list[Issue]:
    issues: list[Issue] = []
    lines = text.split("\n")
    for group in _SYNONYM_GROUPS:
        found_terms: list[str] = []
        found_lines: dict[str, list[int]] = {}
        for i, line in enumerate(lines, 1):
            for term in group:
                if term in line:
                    if term not in found_terms:
                        found_terms.append(term)
                    found_lines.setdefault(term, []).append(i)
        if len(found_terms) > 1:
            locations = "; ".join(
                f"「{t}」(第{','.join(str(l) for l in found_lines[t][:3])}行)"
                for t in found_terms
            )
            issues.append(Issue(
                rule="T-01", severity=Severity.WARNING,
                message="术语不一致：同一概念使用了多个译名",
                context=locations,
                suggestion=f"建议统一使用「{found_terms[0]}」，或在首次出现时注明不同译法",
            ))
    return issues


# ═══════════════════════════════════════════════════════
# 3. Citation / format (F-series)
# ═══════════════════════════════════════════════════════

def check_citation_format(text: str) -> list[Issue]:
    issues: list[Issue] = []
    for i, line in enumerate(text.split("\n"), 1):
        if re.match(r"^[①②③④⑤⑥⑦⑧⑨⑩]\s*$", line.strip()):
            issues.append(Issue(
                rule="F-01", severity=Severity.ERROR,
                message="空脚注：脚注编号后没有内容",
                line=i, context=line.strip(),
            ))
        if re.search(r"^\[\d+\]\s+\S", line) and not re.search(r"\[[MJDCNPS](?:/OL)?\]", line):
            issues.append(Issue(
                rule="F-02", severity=Severity.WARNING,
                message="参考文献条目可能缺少文献类型标识（如 [M] [J] [D]）",
                line=i, context=line.strip()[:80],
                suggestion="GB/T 7714 要求标注 [M]专著 [J]期刊 [D]学位论文 等",
            ))
        is_ref_line = bool(re.match(r"^\s*\[\d+\]", line) or re.match(r"^\s*[①②③④⑤⑥⑦⑧⑨⑩]", line))
        if not is_ref_line:
            line_no_parens = re.sub(r"[（(][^）)]*[）)]", "", line)
            if re.search(r"[一-鿿][,.;:?!]", line_no_parens):
                issues.append(Issue(
                    rule="F-03", severity=Severity.WARNING,
                    message="中文语境中使用了英文标点",
                    line=i, context=line.strip()[:80],
                    suggestion="中文语境应使用全角标点（，。；：？！）",
                ))
    return issues


def check_heading_consistency(text: str) -> list[Issue]:
    has_chinese = has_number = False
    for line in text.split("\n"):
        s = line.strip()
        if re.match(r"^第[一二三四五六七八九十]+[章节]", s):
            has_chinese = True
        if re.match(r"^\d+(\.\d+)*\s+\S", s):
            has_number = True
    if has_chinese and has_number:
        return [Issue(
            rule="F-04", severity=Severity.WARNING,
            message="标题编号体系混用：同时使用了「第X章」和数字编号",
            suggestion="选择一种体系并全文统一",
        )]
    return []


# ═══════════════════════════════════════════════════════
# 4. Register (S-series)
# ═══════════════════════════════════════════════════════

def check_register(text: str) -> list[Issue]:
    issues: list[Issue] = []
    informal = [
        (r"其实", "学术论文中一般不用「其实」，建议改为「实际上」或直接陈述"),
        (r"说白了", "过于口语化，建议删除或改为学术表述"),
        (r"大家都知道", "建议改为「学界普遍认为」并附引用"),
        (r"很明显", "建议用具体论证替代「很明显」"),
        (r"当然了", "建议改为「诚然」或「固然」"),
        (r"这个问题很有意思", "建议直接说明问题的学术意义"),
        (r"笔者觉得", "建议改为「笔者认为」或「本文认为」"),
        (r"总之就是", "建议改为「综上所述」或「概言之」"),
    ]
    for i, line in enumerate(text.split("\n"), 1):
        for pattern, suggestion in informal:
            m = re.search(pattern, line)
            if m:
                issues.append(Issue(
                    rule="S-01", severity=Severity.WARNING,
                    message=f"语体问题：使用了口语化表述「{m.group()}」",
                    line=i, context=line.strip()[:80], suggestion=suggestion,
                ))
    return issues


def check_self_reference(text: str) -> list[Issue]:
    refs_found: dict[str, list[int]] = {}
    for i, line in enumerate(text.split("\n"), 1):
        for ref in ["笔者", "本文", "本研究", "我们"]:
            if ref in line:
                refs_found.setdefault(ref, []).append(i)
        if re.search(r"我(?:认为|以为|将|的|在本|试图|倾向于|主张|发现)", line):
            refs_found.setdefault("我", []).append(i)
    if len(refs_found) > 2:
        terms = ", ".join(f"「{k}」" for k in refs_found)
        return [Issue(
            rule="S-02", severity=Severity.WARNING,
            message=f"自称用法不统一：同时使用了 {terms}",
            suggestion="建议全文统一使用「本文」或「笔者」",
        )]
    return []


# ═══════════════════════════════════════════════════════
# 5. Structure (ST-series)
# ═══════════════════════════════════════════════════════

def check_structure(text: str) -> list[Issue]:
    issues: list[Issue] = []
    for name, pattern, msg in [
        ("摘要", r"摘\s*要|Abstract", "论文缺少摘要"),
        ("关键词", r"关键词|Keywords", "论文缺少关键词"),
        ("参考文献", r"参考文献|References|Bibliography", "论文缺少参考文献"),
    ]:
        if not re.search(pattern, text):
            issues.append(Issue(
                rule="ST-01", severity=Severity.INFO, message=msg,
                suggestion=f"检查是否遗漏了{name}部分",
            ))
    # thesis sentence in the introduction
    lines = text.split("\n")
    intro = ""
    in_intro = False
    for line in lines:
        if re.search(r"引言|绪论|导论|Introduction", line):
            in_intro = True
            continue
        if in_intro:
            if re.match(r"^(第[一二三]|[一二三]、|\d+[\s.])", line.strip()):
                break
            intro += line + "\n"
    if intro:
        indicators = ["本文论证", "本文认为", "本文试图", "本文旨在",
                      "本研究认为", "笔者认为", "本文的核心论点"]
        if not any(ind in intro for ind in indicators):
            issues.append(Issue(
                rule="ST-02", severity=Severity.WARNING,
                message="引言中未发现明确的论点句",
                suggestion="引言末尾应有一句明确的论点陈述（如「本文论证……」）",
            ))
    return issues


# ═══════════════════════════════════════════════════════
# 6. Argumentation logic (L-series) — the high-value checks
# ═══════════════════════════════════════════════════════

_CONNECTORS = {
    "因此", "所以", "故而", "由此可见", "正因为", "之所以", "因为", "由于",
    "这意味着", "这说明", "这表明", "可见",
    "然而", "但是", "不过", "尽管如此", "虽然", "但", "却",
    "不仅如此", "更重要的是", "进一步", "更为关键的是", "而且",
    "在此基础上", "由此出发",
    "相比之下", "与之不同", "相反", "反之", "另一方面",
    "换言之", "也就是说", "具体而言", "之所以这样说",
    "这一点可以从", "从中可以看出", "值得注意的是",
}

_LISTING_SIGNALS = [r"^同时[,，]", r"^此外[,，]", r"^另外[,，]", r"^还有[,，]",
                    r"^也[,，]", r"^并且[,，]", r"^以及"]


def _paragraphs(lines: list[str]) -> list[list[tuple[int, str]]]:
    paras: list[list[tuple[int, str]]] = []
    cur: list[tuple[int, str]] = []
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not s:
            if cur:
                paras.append(cur[:]); cur.clear()
        elif re.match(r"^(#|>|\[|第[一二三四五六七八九十]+|[\d]+\.)", s):
            if cur:
                paras.append(cur[:]); cur.clear()
        else:
            cur.append((i, s))
    if cur:
        paras.append(cur)
    return paras


def check_argumentation_logic(text: str) -> list[Issue]:
    issues: list[Issue] = []
    lines = text.split("\n")
    paragraphs = _paragraphs(lines)

    # L-01: assert-without-argue (4+ consecutive sentences, no connector)
    for para in paragraphs:
        if len(para) < 4:
            continue
        sentences: list[tuple[int, str]] = []
        for line_no, line_text in para:
            for sent in re.split(r"[。！？]", line_text):
                if len(sent.strip()) > 5:
                    sentences.append((line_no, sent.strip()))
        if len(sentences) < 4:
            continue
        streak = max_streak = 0
        streak_start = 0
        for line_no, sent in sentences:
            if any(c in sent for c in _CONNECTORS):
                streak = 0
            else:
                if streak == 0:
                    streak_start = line_no
                streak += 1
                max_streak = max(max_streak, streak)
        if max_streak >= 4:
            issues.append(Issue(
                rule="L-01", severity=Severity.WARNING,
                message=f"段落中连续 {max_streak} 句缺少论证连接（第{streak_start}行附近）",
                line=streak_start, context=para[0][1][:60] + "...",
                suggestion="检查这些句子之间是否缺少因果、转折、递进等逻辑关系。"
                           "考虑用「这意味着……」「之所以……是因为……」补充论证",
            ))

    # L-02: list-without-advance (3+ paragraphs starting with coordinating words)
    listing_streak = 0
    listing_start = 0

    def flush_listing():
        nonlocal listing_streak
        if listing_streak >= 3:
            issues.append(Issue(
                rule="L-02", severity=Severity.WARNING,
                message=f"连续 {listing_streak} 个段落以并列词开头（第{listing_start}行起）",
                line=listing_start,
                suggestion="并列结构适合罗列现象，但学术论文需要递进论证。"
                           "考虑重组为「提出观察→分析原因→得出推论」的递进结构",
            ))
        listing_streak = 0

    for para in paragraphs:
        if not para:
            continue
        if any(re.match(p, para[0][1]) for p in _LISTING_SIGNALS):
            if listing_streak == 0:
                listing_start = para[0][0]
            listing_streak += 1
        else:
            flush_listing()
    flush_listing()

    # L-03: quotation-without-analysis
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not s or not re.search(r'[”」』][\s。]*$', s):
            continue
        next_content = ""
        for j in range(i, min(i + 3, len(lines))):
            nl = lines[j].strip() if j < len(lines) else ""
            if nl:
                next_content = nl
                break
        if next_content and re.match(
            r"^(此外|同时|另外|与此同时|除此之外|值得一提的是|[“「『])", next_content
        ):
            issues.append(Issue(
                rule="L-03", severity=Severity.WARNING,
                message="引文后可能缺少分析：引用结束后直接跳到了新话题",
                line=i, context=s[:60],
                suggestion="引文之后应紧跟分析——这段引文说明了什么？它如何支撑你的论点？",
            ))

    # L-04: chapter openings without transition
    heading_lines = [
        i for i, line in enumerate(lines, 1)
        if re.match(r"^(第[一二三四五六七八九十]+[章节]|#{1,3}\s+\d)", line.strip())
    ]
    for idx, heading_line in enumerate(heading_lines):
        if idx == 0:
            continue
        first_para = ""
        for j in range(heading_line, min(heading_line + 5, len(lines))):
            if j < len(lines):
                nl = lines[j - 1].strip()
                if nl and not re.match(r"^(第|#|\d+\.)", nl):
                    first_para = nl
                    break
        if first_para:
            for pattern in [r"^[A-Z一-鿿]+（.*?）是", r"^在\d{4}年", r"^关于.{2,6}的研究"]:
                if re.match(pattern, first_para):
                    issues.append(Issue(
                        rule="L-04", severity=Severity.INFO,
                        message="章节开头可能缺少与上一章的逻辑衔接",
                        line=heading_line, context=first_para[:60],
                        suggestion="章节开头建议从上一章留下的问题或张力切入，"
                                   "而不是直接从背景介绍或理论定义开始",
                    ))
                    break
    return issues


def check_argumentation_depth(text: str) -> list[Issue]:
    issues: list[Issue] = []
    for i, line in enumerate(text.split("\n"), 1):
        s = line.strip()
        if not s or len(s) < 10:
            continue

        # L-05: unproven value-laden causal premises
        for pattern, desc in [
            (r"(由于|因为|鉴于)(.{4,30})(并非|不是|并不|并未|未必是|绝非)", "前提中的否定性判断"),
            (r"(由于|因为|鉴于)(.{2,15})(所认为的|所谓的|所理解的)", "前提中嵌入了主观判断"),
        ]:
            m = re.search(pattern, s)
            if m:
                window = s[max(0, m.start() - 20):m.end() + 40]
                if not re.search(r"[①②③④⑤⑥⑦⑧⑨⑩]|\[\d+\]|（.*?\d{4}.*?）", window):
                    issues.append(Issue(
                        rule="L-05", severity=Severity.WARNING,
                        message=f"因果前提可能未论证：{desc}，但未见引用或论证支撑",
                        line=i, context=s[:80],
                        suggestion="「由于/因为」引导的前提如果包含价值判断，"
                                   "需要先论证这个前提成立，再用它推导结论",
                    ))
                break

        # L-06: narrative drowning analysis
        for sent in re.split(r"[。！？]", s):
            sent = sent.strip()
            if len(sent) < 100:
                continue
            narrative = len(re.findall(
                r"(?:发生|出现|建立|成立|颁布|发动|开始|结束|到达|返回|出版|发表|签署|"
                r"宣布|任命|组建|迁移|抵达|爆发|写道|记载|描述|讲述|描绘|记录|引述|转述|"
                r"复述|设置|进入|离开|逃离|攻打|占领|投降|撤退)", sent))
            analytic = len(re.findall(
                r"(?:表明|说明|揭示|意味着|体现|反映|证明|论证|暗示|可见|因此|由此|换言之|"
                r"之所以|正因为|由此可见|呈现出|构成了|指向了|折射出|回应了|挑战了|颠覆了)", sent))
            if narrative >= 4 and analytic == 0:
                issues.append(Issue(
                    rule="L-06", severity=Severity.INFO,
                    message="长句中叙述成分可能过多，缺少分析性表述",
                    line=i, context=sent[:80] + "...",
                    suggestion="考虑将叙事部分压缩，或在叙述后立即跟上分析"
                               "（这意味着什么？为什么这个细节重要？）",
                ))

        # L-07: conclusion piling up undeveloped concepts
        for starter in ["由此可见", "综上所述", "综上", "总之", "概言之", "可见"]:
            if starter in s:
                after = s[s.index(starter):]
                if len(re.findall(r"[、]", after)) >= 4:
                    issues.append(Issue(
                        rule="L-07", severity=Severity.WARNING,
                        message=f"总结句中堆砌了 {len(re.findall(chr(12289), after)) + 1} 个以上并列概念",
                        line=i, context=after[:80],
                        suggestion="总结不应引入前文未充分展开的新概念。"
                                   "检查这些并列项是否都在前文得到论证——否则删去或补充论证",
                    ))
                break

        # L-08: intensifiers without supporting evidence
        for word in re.findall(r"(显然|极其|无疑|毋庸置疑|不言自明|必然地|确凿无疑)", s):
            idx = s.index(word)
            surrounding = s[max(0, idx - 60):idx + 60]
            markers = len(re.findall(
                r"(不仅|而且|第一|第二|首先|其次|一方面|另一方面|例如|比如|根据|据)", surrounding))
            if markers < 2:
                issues.append(Issue(
                    rule="L-08", severity=Severity.WARNING,
                    message=f"强断言「{word}」附近未见充分的论据支撑",
                    line=i, context=surrounding.strip()[:80],
                    suggestion=f"「{word}」暗示结论不证自明，但学术论文中应展示推理过程。"
                               "建议删去强度词，或补充多重论据",
                ))
    return issues


# ═══════════════════════════════════════════════════════
# Aggregate
# ═══════════════════════════════════════════════════════

ALL_CHECKS = [
    check_fabricated_references,
    check_unsupported_claims,
    check_terminology_consistency,
    check_citation_format,
    check_heading_consistency,
    check_register,
    check_self_reference,
    check_structure,
    check_argumentation_logic,
    check_argumentation_depth,
]

_SEVERITY_ORDER = {Severity.ERROR: 0, Severity.WARNING: 1, Severity.INFO: 2}


def review(text: str) -> list[Issue]:
    """Run every check, return issues sorted by severity then line."""
    issues: list[Issue] = []
    for fn in ALL_CHECKS:
        try:
            issues.extend(fn(text))
        except Exception as e:  # one bad rule must not sink the run
            print(f"[warn] rule {fn.__name__} failed: {e}", file=sys.stderr)
    issues.sort(key=lambda x: (_SEVERITY_ORDER.get(x.severity, 9), x.line))
    return issues


def _format_text(path: str, issues: list[Issue]) -> str:
    if not issues:
        return f"✓ {path}: 未发现确定性问题"
    icon = {Severity.ERROR: "✗", Severity.WARNING: "⚠", Severity.INFO: "·"}
    n_err = sum(1 for x in issues if x.severity is Severity.ERROR)
    n_warn = sum(1 for x in issues if x.severity is Severity.WARNING)
    n_info = sum(1 for x in issues if x.severity is Severity.INFO)
    out = [f"{path}: {len(issues)} 项（错误 {n_err} / 警告 {n_warn} / 提示 {n_info}）"]
    for x in issues:
        loc = f"L{x.line}" if x.line else "—"
        out.append(f"  {icon[x.severity]} [{x.rule} {loc}] {x.message}")
        if x.context:
            out.append(f"      ↳ {x.context}")
        if x.suggestion:
            out.append(f"      ⇒ {x.suggestion}")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Prism-H deterministic text-review lint")
    ap.add_argument("files", nargs="+", help="Markdown/text files to review")
    ap.add_argument("--severity", choices=["error", "warning", "info"],
                    help="Only show issues at or above this severity")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    min_rank = _SEVERITY_ORDER[Severity(args.severity)] if args.severity else 99
    all_results: dict[str, list[Issue]] = {}
    total_errors = 0

    for path in args.files:
        if not os.path.isfile(path):
            print(f"[warn] not a file: {path}", file=sys.stderr)
            continue
        with open(path, "r", encoding="utf-8") as f:
            issues = review(f.read())
        issues = [x for x in issues if _SEVERITY_ORDER.get(x.severity, 9) <= min_rank]
        all_results[path] = issues
        total_errors += sum(1 for x in issues if x.severity is Severity.ERROR)

    if args.format == "json":
        print(json.dumps(
            {p: [x.to_dict() for x in iss] for p, iss in all_results.items()},
            ensure_ascii=False, indent=2,
        ))
    else:
        print("\n\n".join(_format_text(p, iss) for p, iss in all_results.items()))

    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
