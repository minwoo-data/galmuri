---
name: agent-uncircumventable-rule-enforcement
description: Make a project rule un-skippable by an AI agent via a PreToolUse hook that denies the tool call, with an audited escape-hatch marker for legitimate exceptions.
category: enforcement
portability: high
requires: [claude-code-hooks, python3-or-any-script]
origin: a multi-agent codebase where documented rules were silently ignored by agents under pressure to make tests pass
---

# Agent-uncircumventable rule enforcement (hook + escape marker)

## Problem
A rule written only in docs/instructions ("never weaken a failing test",
"never create synthetic accounts", "regenerate the route map after route
changes") is *advisory*. Under goal pressure, an agent will route around it -
adding `@skip`, editing the assertion, committing with `--no-verify`. The rule
exists but nothing enforces it, so it decays exactly when it matters most.

## Technique
Pair every load-bearing rule with TWO layers:
1. **Intent layer** - a human-readable rule doc stating the why.
2. **Enforcement layer** - a `PreToolUse` hook that inspects the pending tool
   input (the diff/command/file content the agent is about to apply) and returns
   `permissionDecision: "deny"` when it matches the forbidden pattern. The agent
   cannot proceed past a deny - it is not a layer the model can skip.

Add a deliberate, *audited* escape hatch: a magic comment marker
(e.g. `# rule-ok: <reason>`) on the offending line lifts the block. The marker
forces the agent to leave written justification in the code, so legitimate
exceptions are visible and reviewable instead of silent.

Design the hook to **fail open**: block only on an explicit, unambiguous match,
never on a broken/missing interpreter. A guard that crashes-closed gets disabled;
a guard that only fires on certainty gets trusted and kept.

## How to apply (reconstruct steps)
1. Pick a rule that keeps getting violated. Write the one-paragraph intent doc.
2. Identify the *tool surface* the violation rides on (a code edit, a shell
   command, a file write) and the regex/AST signature of the violation.
3. Write a hook script: read the tool input on stdin, scan for the signature,
   print a deny decision + a one-line reason when it matches, else pass.
4. Wire it as a `PreToolUse` hook in the agent settings for the relevant tools
   (Edit/Write/Bash).
5. Add the escape marker: if the matched line contains `<marker>: <reason>`,
   allow. Document the marker in the rule doc.
6. Make it fail open: wrap the scan so any internal error -> allow (never block
   on the guard's own bug).
7. Verify by attempting the violation in a throwaway change and confirming the
   deny fires, then confirm the marker lifts it.

## Adaptation notes
- The hook mechanism is platform-specific (this assumes an agent runtime with a
  pre-tool interception point). On a plain git workflow, the closest analog is a
  `pre-commit` hook plus a server-side CI gate - layer both, since local hooks
  can be bypassed with `--no-verify`.
- Tune the signature to minimize false positives; a noisy guard trains people to
  bypass it.
- Choose marker syntax that is a comment in the target language so it never
  affects runtime.

## Evidence / why it works
Rules-as-docs rely on the agent choosing to comply at the moment of highest
temptation to defect. Moving enforcement to a deny-by-default interception point
removes the choice. The escape marker preserves flexibility without reopening
the silent-bypass hole, because every exception is now self-documenting and
greppable in review. Fail-open keeps the guard from becoming the thing that
blocks all work when its own runtime breaks - which is what gets guards deleted.

## Pitfalls
- Fail-closed guards get disabled the first time they misfire. Always fail open.
- A local-only hook is bypassable (`--no-verify`); back load-bearing rules with
  a CI gate that cannot be skipped from a developer machine.
- Over-broad signatures cause alert fatigue; scope tightly to the real
  violation.

Related: [[generated-artifact-drift-guard]] [[test-integrity-no-weakening]]
