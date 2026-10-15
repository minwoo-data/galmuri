#!/usr/bin/env python
"""Entry-point guard: /galmuri and /forge run the skills directly (0.2.1).

The old commands/*.md wrappers are gone, so each SKILL.md must carry what they
held: user-invocable frontmatter, an argument-hint, and an `## Arguments` table
with a `(no argument)` row. Run `python tests/check_entrypoints.py` (exit 1 on a
failure) or collect it with pytest.
Created by: Minwoo Park
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = sorted((ROOT / "skills").glob("*/SKILL.md"))


def frontmatter(text):
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    return m.group(1) if m else ""


def problems_for(path):
    text = path.read_text(encoding="utf-8")
    fm = frontmatter(text)
    out = []
    if not re.search(r"^user-invocable:\s*true\s*$", fm, re.M):
        out.append("frontmatter lacks 'user-invocable: true'")
    if not re.search(r"^argument-hint:\s*\S", fm, re.M):
        out.append("frontmatter lacks argument-hint")
    sec = re.search(r"^## Arguments\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not sec:
        out.append("no '## Arguments' section")
    else:
        body = sec.group(1)
        if not re.search(r"^\| *Argument *\|", body, re.M):
            out.append("'## Arguments' has no argument table")
        if "(no argument)" not in body:
            out.append("argument table has no '(no argument)' row")
    return out


def all_problems():
    found = []
    if not SKILLS:
        found.append("no skills/*/SKILL.md found")
    for p in SKILLS:
        found += ["%s: %s" % (p.relative_to(ROOT).as_posix(), x) for x in problems_for(p)]
    manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    if (ROOT / "commands").exists():
        found.append("commands/ is back: the skills are the entry points")
    if "commands" in manifest:
        found.append("plugin.json still declares 'commands'")
    if not (ROOT / manifest.get("skills", "./skills/")).is_dir():
        found.append("plugin.json 'skills' path does not exist")
    return found


def test_entrypoints():
    assert not all_problems(), all_problems()


if __name__ == "__main__":
    probs = all_problems()
    for p in probs:
        print("FAIL " + p)
    print("entrypoints: %s (%d skills)" % ("FAIL" if probs else "ok", len(SKILLS)))
    sys.exit(1 if probs else 0)
