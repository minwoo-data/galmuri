---
name: <kebab-slug>
description: <one-line summary - the first-pass signal for whether this technique applies>
category: enforcement | discipline | architecture | ops | knowledge | testing | security
portability: high | medium
requires: [<git>, <python3>, <bash4>, ...]   # tools/runtime the technique assumes
origin: <generic-context, e.g. "a Flask web app with multi-session agent work"> (NO project name)
---

# <Technique Title - name the mechanism, not the feature>

## Problem
<The recurring problem this solves, stated generically. What goes wrong without
it? Why does it keep happening? No domain specifics.>

## Technique
<The reusable mechanism. How it works, in enough detail to rebuild. Name the
moving parts (e.g. "a PreToolUse hook that inspects the tool input and returns
permissionDecision: deny"). Keep it project-agnostic.>

## How to apply (reconstruct steps)
1. <Concrete step a fresh agent can follow on a new project.>
2. <...>
3. <... up to the point where the technique is live and verifiable.>

## Adaptation notes
<What must change per new project: paths, tool names, thresholds, which rule to
enforce. The knobs.>

## Evidence / why it works
<The rationale, and the failure it was born from - generically. "Smoke-check was
not a hard gate, so a drift slipped to main" -> stated without naming the repo.>

## Pitfalls
<Known sharp edges: fail-open vs fail-closed, false positives, bypass conditions.>

Related: [[other-card-slug]]
