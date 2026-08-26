# My AI Coding Playbook

This is an AI-assisted draft based on my recorded course prompts, decisions,
verification evidence, and reflections. I will review the wording and make sure
it still represents my own decisions before submission.

## When I reach for AI first

- I use AI when I need to understand an unfamiliar repository, plan a change
  across several files, or turn a broad goal into smaller acceptance criteria.
  This helped me connect the due-date and tag behavior across models, storage,
  routes, tests, and the frontend.
- I use AI to suggest focused tests and verification steps. Break tests, CI
  green-red-green evidence, Docker health checks, and browser checks showed me
  that running code once is not enough.
- I use AI for repository and documentation review when it can cite actual
  files. Generic advice is less useful than a claim I can compare with source.

## When I do not reach for AI

- I do not ask AI to make personal decisions that require my own judgment, such
  as claiming a manual observation I did not make or pretending I used a tool I
  did not use.
- I do not use AI as a reason to paste passwords, tokens, private keys, `.env`
  values, customer data, or unredacted account and session details.
- I do not approve a destructive Git or filesystem action when I do not fully
  understand the target. The nested repository and unrelated `main` history are
  reasons to stop and confirm the intended repository root.

## My non-negotiables

- The agent must read the relevant files before making repository claims.
- Changes must stay inside the requested scope. Module 5 is documentation-first
  and does not authorize comments implementation or broad application changes.
- I review the diff before accepting a change and keep unrelated files intact.
- Missing evidence is labeled as missing; it is not replaced by a confident
  guess.
- Personal and account details are redacted from logs and documentation.

## My review rules

- For code, I inspect the focused diff and run the smallest relevant test before
  the full suite. I use a browser or live HTTP check when automated tests do not
  prove the user-visible behavior.
- For CI, I confirm that a real failing expectation produces a red run and that
  restoring it produces green again.
- For Docker, I verify the build, `/health`, Docker health state, mapped port,
  and non-root user rather than accepting the Dockerfile by appearance.
- For documentation, I compare claims with the implementation and keep
  automated evidence separate from manual evidence.
- I record whether I accepted, edited, or rejected important AI output and why.

## What I am still figuring out

- I have not used Cursor in this project, so I cannot rank its workflow from
  personal evidence.
- I am still learning when an infrastructure improvement, such as dependency
  pinning, is necessary now and when it belongs in a documented backlog.
- I want to improve at defining requirements and acceptance criteria before the
  first prompt so fewer revisions are needed later.
- I am still learning how to balance broad repository context with a small,
  targeted context that reduces assumptions.

## Decision Card

For a new feature I reach for: Codex App for repository-grounded planning and a reviewed implementation loop.

For a code review I reach for: Codex App for evidence-backed diff and nearby-code inspection.

For debugging I reach for: GitHub Copilot for focused command and setup troubleshooting, then repository tests for confirmation.

For infrastructure I reach for: Codex App with terminal verification for CI and Docker work.

I will never paste credentials, tokens, private keys, `.env` values, real customer data, or unredacted personal account details into an AI tool.

My one rule is: I do not accept an AI contribution until I can explain the relevant change and point to evidence that verifies it.

## 30-day commitment

I will reread this playbook within 30 days, compare it with the AI work I did
during that period, and revise any rule that did not lead to a clear decision
in practice.
