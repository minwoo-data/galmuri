---
name: galmuri
description: "Harvest reusable, project-agnostic techniques from a project into portable technique cards in a knowledge repo (minwoo-data style)."
argument-hint: "<project-path> [--out <dir>] [--scope enforcement,discipline,architecture,ops,knowledge,testing,security] [--deny <tok,tok>] [--dry-run] [--update] | --continue <slug>"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
---

# /galmuri Command (갈무리)

Harvest an existing project for the reusable *mechanisms* buried in it - the
hooks, rules, CI guards, discipline protocols, and structural patterns - and
store them as portable, project-agnostic technique cards in a knowledge repo.
Goal: the knowledge repo alone (e.g. `minwoo-data`) preserves ~90% of the
know-how even if the source project disappears.

갈무리 = to gather a harvest and store it away properly for later use. This skill
gathers the *technique*, never the feature. Business logic, domain rules, data,
and secrets are deliberately skipped.

## Parse Arguments

Inspect `$ARGUMENTS` to determine the action:

| Argument Pattern | Action |
|---|---|
| `<project-path>` | Galmuri the project at `<project-path>` (default: cwd) into the default out dir |
| `--out <dir>` | Target knowledge dir for cards (default: sibling `../minwoo-data/knowledge`, else `./distilled`) |
| `--scope a,b,c` | Restrict extraction to the listed seams (default: all seven) |
| `--deny tok,tok` | Extra redaction tokens beyond the auto-seeded denylist |
| `--dry-run` | Survey + classify only; print the would-extract list, write nothing |
| `--update` | Re-run: refresh existing cards by slug, add new, never delete hand-edited cards without confirmation |
| `--continue <slug>` | Resume an interrupted run from `<out>/.galmuri/<slug>/state.json` |
| (no argument) | Show interactive menu (see below) |

## No Argument Provided

**EXECUTE:** Call the AskUserQuestion tool with the following JSON:

```json
{
  "questions": [
    {
      "question": "Which project do you want to galmuri into portable technique cards?",
      "header": "갈무리",
      "options": [
        {"label": "Current directory", "description": "Harvest the project in the current working directory"},
        {"label": "Enter a path", "description": "Provide a path to the project to extract know-how from"},
        {"label": "Continue a run", "description": "Resume an interrupted run - you'll be asked for the slug next"}
      ],
      "multiSelect": false
    }
  ]
}
```

After the user selects, re-run this command with the resolved argument string.

## Prerequisites (check before execute)

1. **Target project exists** - `test -d "<project-path>"` before starting.
2. **Out dir is NOT inside the source project** - refuse self-harvest (cards
   would pollute the project being read). Resolve and compare absolute paths.
3. **Git present (optional)** - used to read commit history as an extraction
   signal; degrade gracefully if absent.

## Execute

Read the skill file, then follow its workflow exactly:

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/galmuri/SKILL.md`
2. Follow SKILL.md's Phase 0 -> Phase 5 with the argument string: `$ARGUMENTS`
3. Respect SKILL.md's hard invariants:
   - Source project is READ-ONLY (never edit the project being harvested)
   - Output only under the resolved `--out` dir
   - Redaction is mandatory - no project-identifying strings survive in a card
     (Phase 4 denylist grep is a hard gate, not advisory)
   - Every card must pass the "reconstruct test" (self-contained enough that a
     fresh agent can re-apply it on an unrelated project from the card alone)
   - Extract the mechanism, never the business feature

## Output expectations

On success, the user should find:
- `<out>/<category>/*.md` - portable technique cards (one mechanism each)
- `<out>/INDEX.md` - one-line-per-card index (MEMORY.md style)
- A run summary: cards extracted by category, coverage estimate, and the
  list of candidates skipped as project-only.

## Notes for the main agent

- Cards reuse the user's existing memory-card frontmatter + Why/How shape on
  purpose - `minwoo-data` should read like a portable extension of each
  project's local `memory/` system.
- When the same mechanism appears in several projects, prefer ONE card with
  `Adaptation notes` over near-duplicate cards. Link related cards with
  `[[slug]]`.
- If a candidate cannot be generalized without leaking the domain, drop it and
  log it under "skipped as project-only" - do not force a weak card.
