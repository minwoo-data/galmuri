---
name: galmuri
description: Extract reusable, project-agnostic techniques (hooks, rules, guards, structural patterns) from a project and write portable technique cards to a knowledge repo, so the know-how survives without the project. Source is read-only; cards are redacted and self-contained.
---

# 갈무리 (galmuri) - Project Know-How Extraction

## TL;DR

- **Target**: any project that has accumulated discipline - hooks, rules, CI
  guards, skills, ADRs, ops routines.
- **Job**: scan -> classify -> redact -> emit portable technique cards into a
  knowledge repo.
- **Output**: one card per reusable *mechanism*, using the same
  frontmatter + Why/How shape as the user's memory-card system.
- **Invariant**: source project READ-ONLY; output only under `--out`; every
  card passes the portability gate (no project-identifying strings, plus a
  self-contained "reconstruct" recipe).
- **Goal**: a knowledge repo like `minwoo-data` preserves ~90% of the technique
  know-how even with the source project gone.

> This description is exposed in the skill catalogue - it is the first-pass
> signal for whether to pick galmuri.

## Philosophy - opposite of a code reviewer

| | prism / mangchi | **galmuri** |
|---|---|---|
| Direction | look INTO one file, find faults | **look ACROSS a project, lift patterns OUT** |
| Output | findings to fix | **portable cards to keep** |
| Writes | the file under review | **a separate knowledge repo only** |
| Unit | a bug / an axis | **a reusable mechanism** |
| Lifetime | this PR | **outlives the project** |

prism/mangchi/triad make THIS project better. galmuri makes the NEXT project
inherit what this one learned.

## Hard invariants

1. **Source is read-only.** Never edit the source project being read.
2. **Output is confined.** Write only under the resolved `--out` knowledge dir.
3. **Redaction is mandatory.** No project-identifying strings (org name, product
   name, internal hostnames, real human emails/names except the author byline,
   internal repo slugs, ticket prefixes) survive in a card. Enforced by a
   denylist grep in Phase 4 - a hard gate, not advice.
4. **Self-contained cards.** Each card must pass the *reconstruct test*: a fresh
   agent on an unrelated project can re-apply the technique from the card alone.
5. **Mechanism, not feature.** Business logic, domain rules, data, and secrets
   are never techniques. Extract how the guardrail/pattern works, not what the
   app does.
6. **Idempotent / resumable.** A run is keyed on a slug with
   `<out>/.galmuri/<slug>/state.json`; `--update` refreshes by slug and never
   deletes a hand-edited card without confirmation.

## What counts as a "technique" (extraction targets, by seam)

- **enforcement** - PreToolUse / pre-commit hooks, CI gates, drift guards,
  deny-by-default rules, anything that makes a rule un-skippable by an agent.
- **discipline** - agent working rules, change-discipline, evidence
  requirements, parallel-session protocols, review-before-merge ladders.
- **architecture** - recurring structural conventions (factory pattern,
  thin-routes/fat-services, config/logging conventions, load-on-demand
  reference skills, blueprint registration).
- **ops** - backup + verify routines, deploy-by-digest verification, port
  allocation for parallel worktrees, dev-env hygiene boot-fail guards.
- **knowledge** - memory-card systems, ADR conventions, doc-drift harnesses,
  route-map generators.
- **testing** - test-integrity enforcement, per-test DB isolation fixtures,
  CI-with-empty-secrets discipline.
- **security** - secret-scan guardrails, ACL/auth conventions, prompt-injection
  defenses framed generically.

NOT a technique: feature code, domain/business rules, data files, secrets,
one-off scripts with no reusable shape.

## Phases

### Phase 0 - Resolve
- Parse `$ARGUMENTS`: `<project-path>` (default cwd), `--out`, `--scope`,
  `--deny`, `--dry-run`, `--update`, `--continue`.
- Resolve absolute paths. **Refuse if `--out` is inside `<project-path>`.**
- Seed the denylist automatically: read the project's identity surface
  (top-level README/package manifest/CLAUDE.md) and harvest the org name,
  product name, primary hostnames, and any human emails into the redaction
  denylist; merge with `--deny` tokens.
- Compute a run slug; create `<out>/.galmuri/<slug>/state.json`.

### Phase 1 - Survey (parallel fan-out)
Spawn one read-only subagent per in-scope seam in a single message (the prism
fan-out convention). Each agent scans its seam and returns candidate techniques:

```
{ title, seam, source_files: [..], what_it_does (generic),
  why_reusable, portability_guess: high|medium|none }
```

Agents must read the *mechanism* (the hook script, the rule file, the guard),
not the business code it protects.

### Phase 2 - Classify & dedupe
- Merge candidate lists; dedupe by mechanism, not by file (two files
  implementing the same guard = one card).
- Drop `portability_guess: none` (cannot generalize without leaking the domain);
  record them in the "skipped as project-only" log.
- Rank survivors by reuse value (how often this pattern would help a new
  project). Keep high + medium.

### Phase 3 - Extract & redact
For each survivor, write `<out>/<category>/<slug>.md` from
`templates/technique-card.md`:
- Generalize: state the problem and mechanism with the domain stripped out.
- Redact: replace every denylist token with a placeholder
  (`<ORG>`, `<APP>`, `<HOST>`, `<USER>`, `<REPO>`).
- Fill Problem / Technique / How to apply (numbered reconstruct steps) /
  Adaptation notes / `requires`.

### Phase 4 - Portability gate (verify pass, hard)
1. **Denylist grep** each freshly written card. Any hit = FAIL -> re-redact and
   re-grep until clean. A card with a leak never lands in the index.
2. **Reconstruct test**: a Verifier subagent reads each card cold (no project
   context) and answers: "Could I re-apply this on an unrelated project from
   this card alone?" -> PASS / REVISE. REVISE -> fill the missing step, re-test.
- Only cards that pass both checks are indexed.

### Phase 5 - Reconcile links, index, report
1. **Link reconciliation** (a `[[link]]` that points nowhere silently breaks
   recall). Collect every `[[slug]]` across all cards and compare to the set of
   actual card filenames. For each reference:
   - **Slug typo** (the target card exists under a different slug) -> repoint the
     link to the correct existing slug. A dangling typo MUST be fixed before
     indexing.
   - **Genuine forward-link** (points to a real technique not yet carded) -> keep
     it, and list it in the run summary as "worth carding next".
   - **Illustrative `[[...]]`** inside a code span or prose example (e.g. a card
     that explains the wikilink syntax itself) -> not a real link; exclude it
     from the check.
2. **Update `<out>/INDEX.md`**: one line per card, `- [Title](relpath) - hook`,
   grouped by category (mirror the user's `MEMORY.md` index style).
3. **Run summary**: cards per category; the denylist / reconstruct-test /
   reconciliation results (all must be clean); an estimated coverage
   ("N reusable mechanisms captured; M candidates skipped as project-only"); the
   skipped-as-project-only list; and the forward-link "card next" list.

## Redaction denylist (seeded per run)
Auto-seed from the project's identity surface, then redact:
org name, product/app name, internal hostnames/domains, real human
emails/names (keep only the author byline), internal repo slugs, ticket/PR
prefixes, absolute machine paths. Placeholders: `<ORG> <APP> <HOST> <USER>
<REPO> <PATH>`. The author byline ("Created by: Minwoo Park") is allowed.

## Output expectations
- `<out>/<category>/*.md` - portable technique cards.
- `<out>/INDEX.md` - MEMORY.md-style index.
- `<out>/.galmuri/<slug>/` - run state + skipped-candidate log (audit trail).

## Notes
- Cards are intentionally the same shape as the user's per-project memory cards,
  so `minwoo-data` reads as a portable, cross-project extension of local memory.
- Prefer one card with `Adaptation notes` over near-duplicates when a mechanism
  recurs across projects; link with `[[slug]]`.
- `--dry-run` first on an unfamiliar project: review the would-extract list
  before committing cards.
