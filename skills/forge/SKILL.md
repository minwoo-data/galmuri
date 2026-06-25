---
name: forge
description: This skill should be used when turning a galmuri technique card into a working Claude Code skill — when the user says "forge this card into a skill", "make a skill from this technique card", "scaffold a SKILL.md from this card", or "card to skill". Classifies the card's shape first and declines non-skill cards.
---

# forge (단조) — Technique card → Skill

## TL;DR
Take ONE galmuri technique card and forge a Claude Code **skill** from it:
classify the card's actionable shape, and if it is skill-shaped, scaffold a
`SKILL.md` from the card's fields and verify it against the 9 quality criteria
before it lands. The companion to `galmuri`: galmuri *extracts* cards, forge
*turns a card into an executable artifact*.

This is the **skill-only MVP**. Cards that are really hooks, commands, or
references are detected and declined (with the better-fit verdict), not forced.

## Hard invariants
1. **One card in, one skill out.** Operate on a single card per run.
2. **Skill shape only.** Run the classifier; if the card is not skill-shaped,
   report the better fit (hook / command / reference) and stop unless the user
   explicitly insists on a skill.
3. **Facts from the card only.** Do not invent technique steps the card does not
   contain. The card is the source of truth; redaction placeholders stay.
4. **Verify before done.** A forged skill is not "done" until
   `scripts/verify_skill.py` returns `summary: PASS` (no FAIL checks).
5. **Output is confined.** Write the scaffold only under the resolved out dir
   (default `./forged/<slug>/`), never into the knowledge repo or the card.

## Workflow

### Phase 0 — Resolve
- Parse the argument: `<card-path>` (required), optional `--out <dir>`
  (default `./forged/<card-slug>/`), optional `--force-skill`.
- Confirm the card exists and read it. Extract its frontmatter
  (`name`, `description`, `category`, `requires`) and its sections
  (Problem / Technique / How to apply / Adaptation notes / Pitfalls /
  Evidence / Related).

### Phase 1 — Classify (advisory gate)
- Run `scripts/classify_card.py <card-path>`.
- The classifier is a keyword heuristic — a hint, not a verdict. Read the card
  and make the final call.
- If `skill_shaped` is true → continue to Phase 2.
- If `borderline_skill` is true (skill is a strong runner-up — common for
  knowledge cards that mention doc/reference terms while describing a workflow) →
  read the card; if it is genuinely a multi-step judgment workflow, continue to
  Phase 2 and note the borderline call in the report.
- Otherwise (clear hook / command / reference) → report the verdict and `advice`
  and stop, UNLESS `--force-skill` was given or the user already asked for a
  skill; then continue but record the shape mismatch for the final report.

### Phase 2 — Map & scaffold
- Read `references/card-to-skill-map.md` and apply the field mapping.
- Start from `templates/skill-scaffold.md`. Fill every placeholder from the
  card. The two make-or-break elements:
  - **description**: must contain the literal phrase
    `This skill should be used when` AND **≥3 quoted trigger phrases**. Derive
    triggers from the card's Problem as *how a user phrases the task*, not the
    card title.
  - **voice**: imperative throughout (no "You should…"); a `## References`
    section must exist (it links the source card → satisfies progressive
    disclosure).
- Write the result to `<out>/SKILL.md`.

### Phase 3 — Verify & auto-fix (hard)
- Run `scripts/verify_skill.py <out>/SKILL.md`.
- For each FAIL, apply the fix from the auto-fix table in
  `references/card-to-skill-map.md`, then re-run. Repeat until
  `summary: PASS`. Treat WARN (e.g. low word count on a thin card) as
  acceptable — surface it, do not pad with filler.

### Phase 4 — Report
- Print: the classifier verdict (+ mismatch note if forced), the final
  `verify_skill.py` JSON summary (pass/fail/warn), the out path, and any WARN to
  review. State plainly whether the skill PASSED the gate.

## Notes
- forge does not register the skill into a plugin or run a live trigger A/B eval
  (that is skillers-suda's heavier engine). It guarantees the *static* 9-criteria
  gate. Trigger-quality tuning is a follow-up.
- Keep the forged skill close to the card: a small, faithful skill beats a padded
  one. If the card is too thin to make a real workflow, say so rather than invent.

## References
- `references/card-to-skill-map.md` — field mapping, description contract, voice
  rules, auto-fix table.
- `scripts/classify_card.py` — advisory card-shape classifier.
- `scripts/verify_skill.py` — the 9-criteria gate (adapted from skillers-suda).
- `templates/skill-scaffold.md` — the SKILL.md skeleton forge fills.
