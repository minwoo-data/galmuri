---
name: verify-deploy-by-artifact-digest
description: Confirm a deploy actually moved production by checking the running artifact's content digest, not a moving tag or a green pipeline.
category: ops
portability: high
requires: [container-runtime-or-any-immutable-artifact-store]
origin: a containerized web app deployed by retagging an image, where a green pipeline did not guarantee the new build was live
---

# Verify deploy by artifact digest, not by tag or pipeline color

## Problem
A green deploy pipeline and a moved tag (`:prod`, `latest`, `release`) are both
*intentions*, not *facts*. The pipeline can pass while the runtime still serves
the old artifact: the tag was retagged but the host never pulled, the pull
failed silently, or a second deployer raced it. "CI is green" answers the wrong
question.

## Technique
Verify the **content-addressed digest** of the artifact actually running, and
compare it to the digest you intended to ship. A digest is immutable: it is the
identity of the exact bytes. Tags are mutable pointers; pipeline status is about
the build step, not the live process.

Concretely: capture the intended artifact's digest at build/publish time, then
after deploy query the *running* instance for the digest it is actually executing
and assert equality. Only a digest match proves production moved.

## How to apply (reconstruct steps)
1. At publish time, record the immutable digest of the artifact you intend to
   ship (e.g. the image `RepoDigest`, a file content hash, a release checksum).
2. After the deploy step reports success, query the running instance for the
   digest it is actually serving - inspect the live process/container, not the
   registry.
3. Assert `running_digest == intended_digest`. Treat any mismatch as a failed
   deploy even if every upstream step was green.
4. Add a lightweight runtime endpoint or inspect command that surfaces the live
   digest so this check is one command, not a forensic dig.
5. Gate "deploy done" on this assertion in your verification routine.

## Adaptation notes
- For containers: compare `RepoDigest` from inspecting the running container.
- For static files / functions: compare a content hash served by a health/version
  endpoint against the published checksum.
- Works anywhere artifacts are content-addressable; if your platform only has
  mutable tags, add a build-stamped version string the runtime echoes back.

## Evidence / why it works
Mutable pointers and build-step status decouple "I asked for X" from "X is
running." A content digest recouples them because it cannot point at the wrong
bytes. This catches the whole class of "looked deployed, wasn't" incidents:
silent pull failures, stale hosts, retag races.

## Pitfalls
- Comparing tags instead of digests reintroduces the exact bug - a tag can be
  repointed without the runtime changing.
- Caches/CDNs in front of the runtime can serve old content past a real deploy;
  verify at the origin, then bust the edge.
- A health endpoint that reports the *configured* version rather than the
  *running* one is theater; surface the actual loaded artifact.

Related: [[agent-uncircumventable-rule-enforcement]]
