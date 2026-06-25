---
name: forge
description: "Forge a Claude Code skill from a single galmuri technique card — classify the card's shape, scaffold a SKILL.md from its fields, and verify against the 9 quality criteria."
argument-hint: "<card-path> [--out <dir>] [--force-skill]"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# /forge Command (단조)

Turn ONE galmuri technique card into a working Claude Code **skill**. The
companion to `/galmuri`: galmuri harvests cards out of a project; forge turns a
card back into an executable artifact — here, a verified `SKILL.md`.

This is the **skill-only MVP**. A card that is really a hook, a command, or a
reference is detected and declined with the better-fit verdict, not forced into a
skill.

## Parse Arguments

| Argument | Action |
|---|---|
| `<card-path>` | The single technique card to forge (required) |
| `--out <dir>` | Output dir for the scaffold (default `./forged/<card-slug>/`) |
| `--force-skill` | Forge a skill even if the classifier says another shape fits better |
| (no argument) | Ask the user for the card path |

## Prerequisites
- `python3` on PATH (the classifier and verifier are pure-stdlib Python).
- A galmuri technique card with the standard frontmatter + Problem / Technique /
  How to apply / Adaptation notes / Pitfalls shape.

## Execute

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/forge/SKILL.md`.
2. Follow its Phase 0 → Phase 4 with the argument string: `$ARGUMENTS`.
3. Respect its hard invariants:
   - One card in, one skill out.
   - Classify first; decline non-skill cards unless `--force-skill`.
   - Facts from the card only — never invent technique steps.
   - Not done until `scripts/verify_skill.py` returns `summary: PASS`.
   - Write only under the resolved out dir.

## Output expectations
On success the user finds `<out>/SKILL.md` — a scaffolded skill that passes the
9-criteria gate — plus a report: the classifier verdict, the verifier
pass/fail/warn summary, and any WARN to review.

## Notes
- forge guarantees the *static* quality gate (frontmatter, third-person trigger
  description with ≥3 phrases, imperative voice, references section, word budget).
  It does not run skillers-suda's live `claude -p` trigger A/B eval — that heavier
  engine is a separate follow-up.
- Pair with `/galmuri`: harvest a project into cards, then forge the skill-shaped
  ones into real skills.
