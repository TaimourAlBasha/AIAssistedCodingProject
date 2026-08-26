# My AI Coding Playbook

## When I reach for AI first

I use AI to understand an unfamiliar repository, turn a broad request into
small acceptance criteria, design focused tests, and check claims across code,
documentation, CI, and Docker. It helped me connect task rules across models,
storage, routes, tests, and the frontend. I also use it to suggest commands and
verification steps, but I expect the evidence to come from the repository or a
real run.

## When I do not reach for AI first

I do not use AI to make personal judgments or claim observations I did not
make. I will not paste passwords, tokens, private keys, `.env` values, customer
data, or unredacted account details into a prompt. I also pause before a
destructive Git or filesystem action when I cannot explain the exact target.

## My non-negotiables

- Read the relevant files before making repository claims.
- Keep changes within the requested scope and preserve unrelated behavior.
- Review the diff before accepting or committing a change.
- Mark missing evidence honestly instead of filling it with a guess.
- Keep personal and account information out of logs and documentation.

## My review rules

For code, I run the smallest relevant test and then the full suite. For visible
behavior, I add a browser check because a passing backend test does not prove
the interface feels correct. For CI, I verify that a real failed expectation
produces red and that restoring it produces green. For Docker, I check the
build, mapped `/health`, Docker health state, runtime command, and non-root user.
For documentation, I compare important commands, routes, status codes, and
limitations with the source or runtime.

I record whether I accepted, edited, or rejected important AI output. The
centered invalid-transition message is an example: the first result worked but
did not meet the user experience I wanted, so I requested another revision.

## What I am still figuring out

I have not used Cursor in this project, so I do not rank it from imagined
experience. I am still learning when infrastructure improvements such as fully
pinned dependencies belong in the current task and when they should stay in a
documented backlog. I also want to define requirements and acceptance criteria
earlier so fewer revisions are needed.

## Decision Card

- New feature: I use a repository-aware coding agent for planning and a
  reviewed implementation loop.
- Code review: I use an agent that can inspect the diff and nearby code, then I
  verify each substantive claim myself.
- Debugging: I use GitHub Copilot for focused setup or command troubleshooting
  and repository tests for confirmation.
- Infrastructure: I use a repository-aware agent with direct CI and Docker
  verification.
- Never share: credentials, tokens, private keys, `.env` values, customer data,
  or unredacted personal account details.
- One rule: I do not accept an AI contribution until I can explain the change
  and point to evidence that verifies it.

## 30-day commitment

I will reread this playbook within 30 days, compare it with the AI work I did
during that period, and revise any rule that did not help me make a clear and
responsible decision.
