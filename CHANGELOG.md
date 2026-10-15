# Changelog

All notable changes to this plugin are documented in this file. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.2.1] - 2026-10-14

### Changed
- `/galmuri` and `/forge` now run the skills directly. The duplicate wrappers
  `commands/galmuri.md` and `commands/forge.md` are removed, as is
  `"commands"` in `plugin.json`. Each skill registered twice before, once as a
  command and once as a skill.
- Both `SKILL.md` frontmatters gained `user-invocable: true`, `argument-hint` and
  `allowed-tools`, copied from the command files.

### Moved from the command files into the skills
- galmuri: the argument table with defaults (`--out` falls back to the sibling
  `../minwoo-data/knowledge`, then `./distilled`; `--scope` defaults to all seven
  seams; `--dry-run` writes nothing) is now `## Arguments`.
- galmuri: the no-argument AskUserQuestion menu (Current directory / Enter a
  path / Continue a run) is now the `(no argument)` row.
- galmuri: the prerequisites are now Phase 0 bullets. The run refuses a missing
  project and refuses an out dir inside the source; git is optional.
- galmuri: the meaning of 갈무리 is now under the title.
- forge: the argument table and the no-argument behaviour (ask for the card
  path) are now `## Arguments`.
- forge: the prerequisites (`python3` on PATH, the standard card shape) are now
  `## Prerequisites`.
- Invariants, output expectations and notes were already in the skills.

### Added
- `tests/check_entrypoints.py` (stdlib; also runs under pytest) fails when a
  skill loses `user-invocable: true`, its `argument-hint`, its `## Arguments`
  table or the `(no argument)` row, or when `commands/` or the `"commands"`
  manifest key comes back.

## [0.2.0]

### Added
- forge: technique card → verified skill (skill-only MVP).

## [0.1.1]

### Added
- galmuri: portable technique distiller.
