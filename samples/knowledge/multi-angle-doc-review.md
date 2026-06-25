---
name: multi-angle-doc-review
description: Review a document from several independent reader perspectives in parallel, then reconcile their findings, so blind spots a single pass misses get caught.
category: knowledge
portability: high
requires: [an-agent-runtime-that-can-spawn-parallel-subagents]
origin: an agent whose single-pass document reviews kept missing issues that were obvious to a different kind of reader
---

# Multi-angle document review

## Problem
A single review pass carries one reviewer's bias: a clarity-focused reader misses
architectural risk, an architecture-focused reader misses where a newcomer would
get lost. Reviewing a spec, a PRD, or a design doc one way leaves predictable
blind spots, and the gaps only surface later when the wrong reader hits them.

## Technique
Spawn several independent reviewers in parallel, each given a distinct lens
(clarity, longevity/architecture, newcomer comprehension), each blind to the
others so they do not converge prematurely. Each returns findings plus a one-line
verdict. A reconciliation pass then merges the findings, surfaces where the lenses
disagree as an explicit choice, and produces a single prioritized list. The
diversity of lenses is the mechanism — redundant identical reviewers add cost
without catching new classes of problem.

## How to apply (reconstruct steps)
1. Identify the document and the 3-5 lenses that matter for it.
2. Spawn one reviewer per lens in a single batch, each prompted to apply only its
   lens and to end with a one-line verdict.
3. Collect all reviews once they return.
4. Reconcile: merge findings, dedupe, and mark cross-lens disagreements.
5. Emit one prioritized findings list, disagreements flagged for a decision.

## Adaptation notes
Pick lenses by document type — a PRD wants user-value and feasibility lenses; an
architecture doc wants longevity and operability lenses. Keep lenses few and
genuinely distinct; merging near-identical lenses wastes the parallelism.

## Evidence / why it works
Different reader models fail in different ways; running them in parallel and
reconciling catches a broader class of issue than one deeper single pass, at
roughly the same wall-clock cost.

## Pitfalls
- Identical or overlapping lenses add cost without new coverage.
- Skipping reconciliation leaves the user with N contradictory reviews and no
  decision.

Related: [[load-on-demand-reference-skills]]
