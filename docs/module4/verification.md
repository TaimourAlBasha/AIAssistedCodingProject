# Module 4 Verification

This record separates verified evidence from work that still requires user
input or repository coordination. It does not claim results that were not
observed.

## Deliverable checklist

| Requirement | Status | Evidence |
| --- | --- | --- |
| Claude Code installation | Complete | `claude --version` returned `2.1.240 (Claude Code)` on 2026-08-26. |
| Claude Code `/status` | Complete | On 2026-08-26, `/status` reported version 2.1.240, an interactive Claude Team session, and the exact `task-tracker-api` directory as its working directory. |
| `CLAUDE.md` | Complete | It records the stack, course run and test commands, architecture, implemented transition rules, UI and CORS notes, and do-not rules. |
| CI workflow | Complete | `.github/workflows/ci.yml` uses Python 3.11, installs `requirements.txt`, and runs `pytest -v` on pushes and pull requests without suppressing failures. |
| CI green/red/green proof | Complete | The three runs and the reversible test-only change are recorded below. |
| Docker build | Complete | Image `task-tracker:dev` was built as `sha256:027cc02f6304f30100932c786b633eaef714f69b286089504d2018d54df46118`. |
| Docker health check | Complete | Runtime verification returned a health response with `status` equal to `ok`, and Docker reported the container as `healthy`. |
| Docker non-root user | Complete | Runtime `whoami` returned `app`; a later image inspection also reported configured user `app`. |
| Current test suite | Complete | `pytest -v` completed with 28 passed and 2 warnings on 2026-08-26. |
| Documentation claim review | Complete | The claim-versus-reality results are recorded below. |
| AI review triage | Complete | Supported findings and their current disposition are recorded below. |
| Docker technical note | Complete | `docs/decisions/dockerfile-design.md` documents the selected design, alternatives, trade-offs, consequences, and open questions. |
| README link | Complete | README links to the Docker technical note and this verification record. |
| Git inclusion of new documentation | Missing | README is modified and both `docs/decisions/` and `docs/module4/` are untracked until the user reviews and commits them. |
| Copilot, Cursor, and Claude Code reflection | Complete | `docs/module4/reflection.md` compares the observed Copilot and Claude Code workflows and states honestly that Cursor was not used or evaluated. |
| Pull-request base | Missing | `mid-course-project` and `origin/main` have no merge base. Local inspection shows that remote `main` represents the parent `VS Code` repository and records `task-tracker-api` as a Git link, while the feature branch contains the Task Tracker files at its root. The facilitator must confirm which layout to submit. |

## CI green, red, and green evidence

1. Initial green run: <https://github.com/TaimourAlBasha/AIAssistedCodingProject/actions/runs/32967665545>
2. Intentional red run: <https://github.com/TaimourAlBasha/AIAssistedCodingProject/actions/runs/32967754366>
3. Restored green run: <https://github.com/TaimourAlBasha/AIAssistedCodingProject/actions/runs/32967857184>

Commit `37404eb` intentionally changed only the expected `/version` value in
`tests/test_tasks.py` from `0.1.0` to `9.9.9`. Commit `d22a864` restored the
correct expectation. Production application code was not broken for this
demonstration.

## Documentation claim-versus-reality log

| Documentation claim | Code or runtime reality | Resolution |
| --- | --- | --- |
| `POST /tasks` returns HTTP 201. | The route declares HTTP 201. | Keep the claim. |
| `DELETE /tasks/{task_id}` returns HTTP 204. | The route declares HTTP 204 and returns no response body. | Keep the claim. |
| Route docstrings describe not-found HTTP 404 responses. | The handlers raise HTTP 404, but generated OpenAPI does not explicitly list the route-specific 404 responses. | Keep the runtime claim; consider adding response metadata later if OpenAPI completeness becomes required. |
| PATCH validation failures return HTTP 422. | Pydantic validation and status-transition rules both return HTTP 422, but the business-rule response uses a string `detail` that differs from the generated validation-error schema. | Keep the status-code claim and avoid claiming one response shape for every 422 case. |

## AI review triage

| Finding | Disposition | Reason |
| --- | --- | --- |
| The frontend uses `window.location.origin` when served from port 5500, although the backend is expected on port 8000. | Open | This is supported by `frontend/index.html`; changing it is separate from the documentation work. |
| Route tests do not cover all three allowed status-transition pairs. | Open | Current tests cover rejection of `InProgress` to `ToDo`, but do not directly prove every allowed pair through PATCH. |
| OpenAPI response metadata does not fully describe 404 and both forms of 422. | Open | Runtime behavior exists, but the generated API contract is less specific. |
| Runtime image contains pytest and httpx. | Accepted trade-off | The course Dockerfile installs the single current `requirements.txt`; dependency splitting is recorded as a future question in the Docker decision note. |

## AI tool evidence for reflection

### GitHub Copilot

The user reported using Copilot while turning the local project folder into a
Git repository and connecting it to GitHub. The work included initializing Git,
renaming the initial branch to `main`, adding the remote, staging and committing
the project, and attempting the first push. When the push failed because the
SSH remote could not authenticate with the available GitHub credentials,
Copilot helped identify authentication as the issue and switch the remote to
HTTPS. This was a repository setup and troubleshooting workflow rather than an
application-code change.

### Cursor

The user confirmed that Cursor was not used for this project. This record does
not claim any Cursor results or assign it advantages that were not observed.

### Claude Code

Claude Code version 2.1.240 was installed, authenticated with a Claude Team
account, and launched from the Task Tracker repository. Its `/status` screen
confirmed an interactive session whose working directory was the exact
`task-tracker-api` repository. No application files were edited by Claude Code
during this setup verification.

## Remaining manual evidence

- Confirm the correct Git repository root and base branch with the facilitator
  before creating a pull request against `origin/main`.

## Repository-root confirmation request

Send the following question to the facilitator before changing Git history:

> The GitHub `main` branch represents my parent `VS Code` repository and stores
> `task-tracker-api` as a Git link at commit `98ef2ab`. My
> `mid-course-project` branch was pushed from the nested Task Tracker repository,
> so it has no merge base with `origin/main` and contains the app files directly
> at the branch root. For Module 4, should I submit the Task Tracker as a
> standalone repository with its files at the root, or preserve the parent
> repository and update the `task-tracker-api` Git link?
