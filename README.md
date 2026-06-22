# 갈무리 (galmuri)

Harvest reusable, project-agnostic techniques out of a project and store them as
portable **technique cards** in a knowledge repo - so the know-how survives even
if the source project disappears.

> 갈무리 = to gather a harvest and store it away properly for later use.

`prism` / `mangchi` / `triad` make *this* project better. **galmuri makes the
next project inherit what this one learned.**

## What it does

```
/galmuri <project-path> [--out <dir>] [--scope ...] [--dry-run] [--update]
```

1. **Survey** - fans out read-only subagents, one per "seam" (enforcement,
   discipline, architecture, ops, knowledge, testing, security).
2. **Classify** - dedupes by mechanism, drops anything too project-specific to
   generalize.
3. **Extract + redact** - writes one card per reusable mechanism, stripping
   org/product/host/email identifiers into placeholders.
4. **Portability gate** - a denylist grep (hard) + a "reconstruct test"
   (a fresh agent must be able to re-apply the technique from the card alone).
5. **Index** - appends to `INDEX.md`, MEMORY.md style.

## Invariants

- Source project is **read-only**.
- Output only under `--out`.
- **Redaction is mandatory** - no project-identifying strings in a card.
- Cards capture the **mechanism, never the feature** (no business logic, data,
  or secrets).

## Output

```
<out>/
  enforcement/*.md      # one portable technique each
  ops/*.md
  knowledge/*.md
  ...
  INDEX.md              # one line per card
  .galmuri/<slug>/      # run state + skipped-as-project-only log
```

Card shape mirrors the user's per-project memory-card format, so `minwoo-data`
reads as a portable, cross-project extension of local `memory/`.

See `samples/` for two cards galmuri produced from a real Flask project (redacted).

## Install

Part of the `haroom_plugins` marketplace (alongside ddaro / prism / triad /
mangchi). Add the plugin entry to `haroom_plugins/.claude-plugin/marketplace.json`
and the `plugins/galmuri` submodule, then `/plugin update`.

Created by: Minwoo Park
