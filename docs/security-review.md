# Task Tracker Security Review

## Scope and method

This Module 5 review was a static, read-only inspection of the Task Tracker.
It covered backend routes, validation, business rules, in-memory storage, tests,
frontend rendering and API calls, local configuration, dependencies, Docker,
CI, and development scripts. No application code was changed, and no runtime
security scanner was used.

## Graded findings

| ID | Severity | Grade | File / location | Finding | Evidence and grading reason | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| SEC-01 | Medium outside course scope | Valid | `app/main.py:77-228`; `README.md` current limitations | Task routes have no authentication or authorization, so any client that can reach the API can read, create, modify, or delete tasks. | No route uses an identity or permission dependency. README confirms that the absence of authentication is intentional for this learning project. It is therefore a real production risk and a documented course-scope limitation, not a defect to implement in Module 5. | Keep out of current scope and create a future architecture/security backlog item before any shared or production use. |
| SEC-02 | Low in the current learning context | Valid | `app/models.py:61-67`, `app/models.py:110-116`, `app/storage.py:14`, `app/storage.py:39` | Descriptions and assignees have no length limits, and the in-memory task collection has no capacity limit. | The code explicitly limits titles and tags but places no comparable bound on these fields or on the number of stored tasks. A reachable client could consume increasing process memory. The severity is reduced because this is a local, non-production learning project with process-local data. | Define reasonable description, assignee, request-size, and collection limits before broader use; add focused validation tests when implemented. |
| SEC-03 | Low | Valid | `requirements.txt:1-6`, `Dockerfile:3`, `Dockerfile:17`, `.github/workflows/ci.yml:15-21` | Python packages, Docker base images, and GitHub Actions use mutable or unpinned references. | `requirements.txt` contains no versions, Docker uses `python:3.11-slim` without a digest, and CI actions use major-version tags. Exact builds cannot be reconstructed from these files alone, and dependency vulnerability status cannot be established reliably. | Add a documented dependency-update and pinning approach in a later infrastructure task. |

## Manual scan record

The student has not supplied an independent manual finding for this review.
No "You-only" result is claimed. The following areas remain suitable for the
student's own inspection:

- Whether initial task creation can bypass the status-transition workflow.
- Whether the frontend selects the correct API origin when served on port 5500.
- Whether the broad exception in `scripts/seed_tasks.py` hides a useful error.
- Whether the tag-filter query should have a backend length limit.

These are review questions, not graded findings in this document.

## Reconciliation

| Agreement | AI-only | You-only |
| --- | --- | --- |
| None claimed because no independent student scan was supplied. | SEC-01: intentional absence of authentication and authorization. | None claimed. |
|  | SEC-02: unbounded fields and in-memory collection. |  |
|  | SEC-03: mutable and unpinned dependency references. |  |

The AI review found concrete issues in access control, resource limits, and
supply-chain reproducibility. Its coverage cannot be meaningfully compared with
student coverage until an independent manual observation is recorded.

## Top-three security backlog

| Rank | Finding | Why it matters | Suggested owner | Next action |
| --- | --- | --- | --- | --- |
| 1 | Define an authentication and authorization boundary before shared use. | Without an identity boundary, every reachable client has full task access. | Course/project owner with backend owner | Record intended users and permissions before designing or implementing authentication outside Module 5. |
| 2 | Bound user-controlled fields and memory growth. | Unbounded input and task count can increase process memory and response size. | Backend owner | Agree on limits, add model and API tests, and then implement the smallest validated constraints. |
| 3 | Establish reproducible dependency references. | Unpinned packages and mutable image/action tags make builds harder to reproduce and audit. | DevOps/project owner | Choose a course-appropriate pinning and update policy before changing dependency files. |

## Controls confirmed during review

- Task status and priority values use explicit enums.
- Unknown request fields are rejected.
- Titles and tags have validation limits.
- Status changes through PATCH use explicit transition rules.
- Task identifiers are generated with UUID4.
- The frontend renders user-controlled task values with `textContent`; the
  observed `innerHTML` assignment only clears a container with a fixed empty
  string.
- The frontend file path is fixed and is not built from request input.
- CORS lists two explicit localhost origins rather than a wildcard origin.
- `.env` is ignored by Git and excluded from the Docker build context.
- No tracked credential, private-key, token, cache, or virtual-environment file
  was identified by the targeted repository scan.
- The Docker runtime uses the non-root `app` user and copies only application
  runtime directories.
- CI grants read-only repository-content permission, runs tests without failure
  suppression, and contains no deployment step.
- No broad exception handling was found in the running application. The broad
  exception in `scripts/seed_tasks.py` is limited to a development script.

## Files inspected

- `AGENTS.md`
- `README.md`
- `app/main.py`
- `app/models.py`
- `app/storage.py`
- `app/business_rules.py`
- `tests/test_models.py`
- `tests/test_storage.py`
- `tests/test_tasks.py`
- `frontend/index.html`
- `requirements.txt`
- `.env.example`
- `.gitignore`
- `.dockerignore`
- `Dockerfile`
- `.github/workflows/ci.yml`
- `add_tasks.py`
- `scripts/seed_tasks.py`
- Git's tracked-file list

## Assumptions and limits

- This review did not run the test suite, start the application, fuzz inputs,
  scan container layers, or query a vulnerability database.
- Dependency vulnerabilities cannot be confirmed or ruled out because versions
  are unpinned and no dependency scanner was run.
- The application is evaluated as a learning project, not as a production
  service.
- Authentication, a database, deployment, and production hardening remain
  outside Module 5 implementation scope.
- The grading above is an AI-assisted draft. The student must review it and add
  any independent manual observation before claiming a completed manual scan.
