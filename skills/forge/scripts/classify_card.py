#!/usr/bin/env python3
"""Classify a galmuri technique card's actionable SHAPE.

Not every card should become a Claude Code *skill*. A skill is an LLM-invoked
workflow that applies judgment when a trigger matches. Many cards are really:
  - hook      : an un-skippable gate (pre-commit / PreToolUse / CI deny)
  - command   : a repeatable operational routine run on demand (/deploy, /backup)
  - reference : a structural pattern / know-how doc loaded on demand
  - skill     : a multi-step judgment workflow triggered by task context

This is an ADVISORY heuristic (signals + score), not a gate. `forge` targets the
skill shape; for a hook/command/reference verdict it warns but still proceeds if
the user explicitly asked for a skill.

Usage: classify_card.py <path-to-card.md>   ->  JSON verdict on stdout.
Pure stdlib.
"""
import sys
import os
import re
import json

# (regex, shape, weight, why) — scanned against frontmatter category + body.
SIGNALS = [
    (r"\b(PreToolUse|pre-commit|pre commit|deny hook|deny-by-default|un-skippable|blocks? the (change|commit)|CI gate|guard(rail)?|lint)\b", "hook", 3, "un-skippable enforcement gate"),
    (r"\b(escape marker|fail-open|fail-closed|denylist grep|hard gate)\b", "hook", 2, "gate mechanics"),
    (r"\b(routine|run on demand|deploy|backup|rotation|migration|handover bundle|port allocation|restore-test)\b", "command", 3, "operational routine run on demand"),
    (r"\b(structural convention|service layer|factory pattern|thin[- ]routes|config overlay|architecture (map|doc|diagram|convention))\b", "reference", 2, "structural pattern / know-how"),
    (r"\b(load[- ]on[- ]demand|reference (doc|material)|checklist|index file|memory[- ]card)\b", "reference", 2, "reference material"),
    (r"\b(workflow|interview|step[- ]by[- ]step judgment|analyze|classify|synthesize|decide between|when .{0,40} do)\b", "skill", 3, "LLM judgment workflow"),
    (r"\b(reviewers?|lenses?|perspectives?|in parallel|reconcil\w+|spawn\b.{0,30}(agent|reviewer|subagent))\b", "skill", 3, "parallel multi-perspective judgment workflow"),
    (r"\b(triggers? (on|when)|on a trigger match|invoked when|apply (this|the technique) when)\b", "skill", 2, "trigger-driven invocation"),
]

CATEGORY_LEAN = {
    "enforcement": ("hook", 2),
    "discipline": ("hook", 1),
    "ops": ("command", 2),
    "testing": ("command", 1),
    "architecture": ("reference", 2),
    "knowledge": ("reference", 1),
    "security": ("hook", 1),
}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: classify_card.py <path-to-card.md>"}))
        sys.exit(1)
    path = sys.argv[1]
    if not os.path.exists(path):
        print(json.dumps({"error": f"File not found: {path}"}))
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    fm = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    category = None
    if fm:
        cat_m = re.search(r"^category:\s*([a-z]+)", fm.group(1), re.MULTILINE)
        if cat_m:
            category = cat_m.group(1).strip()

    scores = {"hook": 0, "command": 0, "reference": 0, "skill": 0}
    reasons = {"hook": [], "command": [], "reference": [], "skill": []}

    if category in CATEGORY_LEAN:
        shape, w = CATEGORY_LEAN[category]
        scores[shape] += w
        reasons[shape].append(f"frontmatter category '{category}'")

    body = content.lower()
    for rx, shape, weight, why in SIGNALS:
        if re.search(rx, body, re.IGNORECASE):
            scores[shape] += weight
            reasons[shape].append(why)

    verdict = max(scores, key=scores.get)
    total = sum(scores.values()) or 1
    confidence = round(scores[verdict] / total, 2)
    # Skill-shaped only when 'skill' is the winning shape. A high absolute skill
    # score next to an even higher hook/command score is NOT skill-shaped - the
    # card's dominant mechanism wins. Override is via forge's --force-skill.
    skill_ok = verdict == "skill"
    # Keyword classification is brittle on knowledge cards that *mention* doc/
    # reference terms while actually describing a workflow. Flag the case where
    # 'skill' is a strong runner-up so the agent (and forge) treat the verdict as
    # a hint, not a gate. This is the documented advisory escape hatch.
    borderline_skill = (not skill_ok) and scores["skill"] >= 3

    if skill_ok:
        advice = "Card is skill-shaped - forge a SKILL.md."
    elif borderline_skill:
        advice = (
            f"Verdict '{verdict}', but strong skill signals are present "
            f"(skill score {scores['skill']}). Borderline - the agent should read "
            f"the card and decide; forge with --force-skill if it is a workflow."
        )
    else:
        advice = (
            f"Card looks {verdict}-shaped, not a skill. A {verdict} artifact "
            f"likely fits better; forging a skill anyway is allowed but may be a poor fit."
        )

    out = {
        "card": os.path.basename(path),
        "category": category,
        "verdict": verdict,
        "confidence": confidence,
        "scores": scores,
        "reasons": reasons[verdict],
        "skill_shaped": skill_ok,
        "borderline_skill": borderline_skill,
        "advice": advice,
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
