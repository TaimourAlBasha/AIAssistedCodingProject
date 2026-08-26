# Final AI Review and Ownership Record

## Scope and guardrails

This final-project pass used AI to inspect the repository, identify evidence
gaps, propose a focused test-and-documentation change, run verification, and
organize the results. It did not add comments, authentication, a database,
notifications, deployment, or a new user-interface feature.

`AGENTS.md` was checked for these required guardrails:

- verified stack, architecture, commands, and business rules
- final-project scope and explicit do-not rules
- files and information that must never be committed
- code placement, testing, documentation, and browser/Docker expectations
- a definition of done that includes tests, privacy, placeholders, and CI

## AI code-review triage

The reviewed final diff includes the changes to `tests/test_tasks.py`, README,
`AGENTS.md`, and the required evidence documents.

| AI review comment | Grade | Reason and action |
| --- | --- | --- |
| The route suite did not directly prove all three allowed PATCH status transitions. | Useful | `app/business_rules.py` defines three pairs, while the previous API test covered only one rejected reverse transition. A parameterized route test was added without changing runtime logic. |
| `/health` was used by Docker and README verification but had no direct route test. | Useful | The endpoint is part of the release contract. A focused test now verifies HTTP 200, `status: ok`, and a timezone-aware timestamp. |
| Split test dependencies out of `requirements.txt` before submission. | Noise | This could reduce the runtime image, but it is not required for this course release and would expand dependency-management scope. The current trade-off remains documented. |
| Add detailed OpenAPI metadata for every 404 and both HTTP 422 response shapes. | Noise | The runtime behaviors are implemented and tested; schema enrichment is a separate API-documentation improvement, not a correctness fix required by this release. |

The only runtime-area diff is test coverage. `app/` and `frontend/` behavior is
unchanged by the final-project work.

## Security review triage

| Finding | Grade | Evidence and decision |
| --- | --- | --- |
| Task routes have no authentication or authorization. | Valid | No route has an identity or permission dependency. README already identifies this as an intentional learning-project limitation; implementation remains outside scope. |
| Description, assignee, and the in-memory task collection have no capacity limits. | Valid | `app/models.py` limits titles and tags but not those fields, and `app/storage.py` stores tasks in an unbounded process-local mapping. This remains a future hardening item. |
| Dependencies, the Python base image, and GitHub Actions references are mutable rather than fully pinned. | Valid | `requirements.txt` has no versions, Docker uses `python:3.11-slim`, and CI uses major action tags. A pinning policy is a future infrastructure decision. |
| The fixed frontend file path creates a path-traversal vulnerability. | False Positive | `FRONTEND_FILE` is constructed from `__file__` and constants, not from request input. No user-controlled path reaches `FileResponse`. |

The student was asked to perform a human browser security check by entering
literal HTML-like text into a task title and verifying that it displays as text
without script execution. The result is not claimed until the student reports
what happened.

## Corrected or rejected AI output

Earlier UI work first used a native browser alert for an invalid drag-and-drop
transition. The student asked for visible feedback and then corrected the
placement requirement to the center of the screen. The final implementation
uses the existing in-app toast rather than accepting the first AI suggestion as
finished. For this release, AI suggestions to add OpenAPI response metadata or
split dependency files were rejected as useful future work outside the agreed
scope.

During this final-project pass, an earlier AI pass deleted `add_tasks.py` and
`scripts/seed_tasks.py` as "leftover utility scripts" without first showing
that judgment call for approval, contradicting the explicit instruction to
surface ambiguous deletions before acting. On review, both scripts were
legitimate optional dev-seed tools (one seeds in-memory storage directly, the
other seeds over HTTP). The deletion was rejected: both files were restored
and documented in `README.md` instead of removed.

## Ownership statement

I reviewed the repository claims against the code and kept unverified evidence
separate from completed checks. I can explain why the final diff adds tests and
documentation without changing application behavior. I understand that the app
uses process-local storage, has no authentication, and is a course project
rather than a production deployment. I am responsible for the final branch,
the evidence it contains, and the decision to reject suggestions that expanded
the assignment scope.

## My AI-use rules

1. I do not share credentials, secrets, private data, or unredacted account
   details with an AI tool.
2. I verify repository claims against files or runtime evidence and label any
   missing human observation honestly.
3. I review the diff, keep changes within scope, and do not accept AI code until
   I can explain it and its verification.
