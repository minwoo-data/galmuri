# Card → Skill field mapping & rubric

How `forge` turns a galmuri technique card into a Claude Code SKILL.md that
passes the 9 quality criteria. Loaded on demand by `forge`'s SKILL.md.

## Shape rubric (run `classify_card.py` first)

A card is **skill-shaped** when applying it means an agent runs a multi-step
**judgment workflow** triggered by task context. It is NOT skill-shaped when it
is really:

| Verdict | Looks like | Forge a skill? |
|---|---|---|
| hook | pre-commit / PreToolUse / CI deny gate, un-skippable rule | No — scaffold a hook (out of MVP scope). Decline. |
| command | a routine run on demand (deploy, backup, handover) | No — a slash command fits better. Decline. |
| reference | a structural pattern / load-on-demand doc | No — keep as a reference. Decline. |
| skill | "when X, analyze/review/decide/synthesize …" | **Yes** — this is the path below. |

`classify_card.py` is advisory. If the verdict is not `skill` but the user
explicitly asked to forge a skill, proceed but surface the mismatch in the report.

## Field mapping (card → SKILL.md)

| Card field | → SKILL.md element | Transform |
|---|---|---|
| frontmatter `name` | frontmatter `name` | keep kebab slug |
| frontmatter `description` (one-liner) | **seed** for the new `description` | rewrite into third-person trigger format (below) |
| `## Problem` | the WHEN — drives trigger phrases + "## When to use this" | mine 3-5 concrete task phrasings a user would type |
| `## Technique` | "## What it does" (1 short para) | strip to the mechanism, imperative voice |
| `## How to apply` (reconstruct steps) | "## Workflow" (numbered steps) | rephrase as imperative agent steps |
| `## Adaptation notes` | "## Inputs / knobs" | the per-use parameters |
| `## Pitfalls` | "## Guardrails" | keep as cautions, imperative |
| `## Evidence / why it works` | one "## Why" line | compress to a sentence |
| frontmatter `requires` | "## Prerequisites" | list tools/runtime |
| `Related: [[slug]]` | "## References" | link cards; satisfies progressive-disclosure check |

## The description contract (the make-or-break check)

`verify_skill.py` FAILS unless the `description:` field:
1. contains the exact phrase **`This skill should be used when`**, AND
2. contains **≥3 quoted trigger phrases** (`"..."`).

Triggers are NOT the card title — they are how a *user phrases the task*. Derive
them from the card's Problem. Example, for `design-token-reuse-guard`:

```
description: This skill should be used when reviewing UI changes for design-token
  drift — when the user says "check for raw hex values", "are we bypassing design
  tokens", "audit colors against the token set", or "find magic spacing values".
```

That is one `This skill should be used when` + four quoted triggers → PASS.

## Voice rules (imperative_form check)

Write the body in imperative / third-person. Never "You should run…" → "Run…".
Quoted trigger phrases and code blocks are exempt (the checker excludes them),
so user-facing example phrases in quotes are fine.

## Word count

Target 1,500-2,000 words (PASS), ≤3,000 (WARN), >3,000 (FAIL). A thin card will
land under target → WARN, not FAIL. Do not pad to hit the band; a tight 800-word
skill that WARNs is better than 1,800 words of filler. Flag the WARN in the report.

## Auto-fix table (when verify_skill.py reports FAIL)

| FAIL check | Fix |
|---|---|
| third_person | prepend "This skill should be used when" to description |
| trigger_phrases | add quoted user-phrasings until ≥3 |
| imperative_form | rewrite the flagged "You …" sentence as a command |
| references_exist | create the referenced file, or drop the backtick mention |
| name/description/frontmatter | repair the YAML block |
| word_count >3000 | move detail into a `references/` file (progressive disclosure) |

Re-run `verify_skill.py` after each fix until `summary == PASS`.
