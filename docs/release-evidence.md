# Final Project Release Evidence

## Release scope

- Branch: `final-project`
- Baseline commit: `d21772a`
- Product scope: no new product feature; work is limited to cleanup, tests,
  release documentation, review, and verification.
- Repository layout: the Task Tracker files are at this branch's root. The
  unrelated `origin/main` history represents a parent workspace, so this branch
  is submitted directly instead of being merged into that history.

## Local application baseline

On 2026-08-26, the untouched branch was started from the repository root with:

```powershell
uvicorn app.main:app --reload --port 8000
```

Automated HTTP evidence:

| Check | Result |
| --- | --- |
| `GET http://127.0.0.1:8000/health` | HTTP 200 with `status` equal to `ok` and a UTC timestamp |
| `GET http://127.0.0.1:8000/` | HTTP 200, `text/html`, and Task Tracker content |

Frontend check (manual, by the student, 2026-08-26): opened
`http://127.0.0.1:8000/` in a browser and exercised the board directly rather
than relying on the HTTP checks above. Verified: creating tasks; drag-and-drop
movement between status columns; setting tags, due date, assignee, and
priority; the overdue filter; the tag/status filters; valid status
transitions; and that invalid transitions are rejected with visible feedback
in the UI. The Kanban board and create/edit flow work as documented.

## Backend tests

The untouched baseline command was:

```powershell
.\venv\Scripts\python.exe -m pytest -v
```

It collected 28 tests and reported 28 passed in 1.20 seconds. The final change
adds direct coverage for `/health` and all three allowed PATCH status
transitions.

Final command and result, run after the diff was complete:

```powershell
.\venv\Scripts\python.exe -m pytest -v
```

32 passed, 3 warnings, in 0.38 seconds. The added tests are
`test_health_returns_ok_with_timezone_aware_timestamp` and the three
parametrized cases of `test_patch_accepts_each_supported_status_transition`.

The local virtual environment uses Python 3.12.7. The course target is Python
3.11, which is exercised by both CI and the Docker image.

Two pre-existing Starlette deprecation warnings remain: one concerns
TestClient's httpx integration and one concerns the HTTP 422 constant name.
They do not hide or convert failures.

## CI evidence

The workflow at `.github/workflows/ci.yml` runs on `push` and `pull_request`,
uses Python 3.11, installs `requirements.txt`, and runs `pytest -v`.

- Initial green run: <https://github.com/TaimourAlBasha/AIAssistedCodingProject/actions/runs/32967665545>
- Intentional red run: <https://github.com/TaimourAlBasha/AIAssistedCodingProject/actions/runs/32967754366>
- Restored green run: <https://github.com/TaimourAlBasha/AIAssistedCodingProject/actions/runs/32967857184>

The red run changed only one test expectation and was reversed in the next
commit. The workflow has no `continue-on-error`, `|| true`, `--exit-zero`, test
output pipe, deployment step, or elevated write permission.

- Final `final-project` branch run (commit `044b639`): Success, 17s —
  <https://github.com/TaimourAlBasha/AIAssistedCodingProject/actions/runs/33006548631>

## Docker evidence

Commands used from the repository root on 2026-08-26:

```powershell
docker build -t task-tracker:final .
docker run --detach --name tt-final --publish 8001:8000 task-tracker:final
Invoke-WebRequest http://127.0.0.1:8001/health -UseBasicParsing
docker inspect tt-final --format '{{.State.Health.Status}}|{{.Config.User}}|{{json .Config.Cmd}}'
docker exec tt-final whoami
docker rm --force tt-final
```

| Check | Evidence |
| --- | --- |
| Image build | Passed; image manifest `sha256:07e62f0a728a684f007feaf66a638644f2f429f4f868ac698681a4ea4b80579f` |
| Mapped health request | HTTP 200 with `status` equal to `ok` |
| Docker health | `healthy` |
| Runtime user | Docker configuration and `whoami` both returned `app` |
| Runtime command | `uvicorn app.main:app --host 0.0.0.0 --port 8000` |
| Secret handling | Dockerfile contains no secret values; `.dockerignore` excludes `.env` and `.env.*`; runtime copies only the installed environment, `app/`, and `frontend/` |

Host port 8001 was used only to avoid conflicting with the local server already
running on 8000. README uses the normal `8000:8000` mapping.

## Documentation claim verification

| Documentation claim | Repository or runtime evidence | Resolution |
| --- | --- | --- |
| Local startup uses `uvicorn app.main:app --reload --port 8000`. | The command started the app, and both `/` and `/health` returned HTTP 200. | Keep. |
| `POST /tasks` returns HTTP 201 and `DELETE /tasks/{id}` returns HTTP 204. | `create_task` and `delete_task_route` declare those status codes in `app/main.py`; route tests cover both contracts. | Keep. |
| PATCH accepts only `ToDo -> InProgress`, `InProgress -> Done`, and `Done -> InProgress`. | `VALID_TRANSITIONS` in `app/business_rules.py` contains exactly those pairs; focused route tests now exercise each pair. | Keep. |
| The Docker process runs as non-root user `app`. | Dockerfile switches to `USER app`; live `docker exec tt-final whoami` returned `app`. | Keep. |
| `.env.example` configures the application port and environment. | `app/main.py` loads dotenv but does not read `PORT` or `APP_ENV`; startup uses the command-line port. | Corrected README to label the values illustrative and unused. |

## Final clean checks

Performed on 2026-08-26 after the diff above was complete:

- Full suite: 32 passed (see Backend tests). No test was changed to hide an
  application defect.
- Independent Docker re-verification (separate from the build above): rebuilt
  the image, ran it on a free host port, confirmed `GET /health` returned
  HTTP 200 with `status: ok`, and confirmed `docker exec ... whoami` returned
  `app`. Verification container removed afterward.
- Placeholder scan (`TODO`, `TBD`, `PLACEHOLDER`, `FIXME`) across `README.md`,
  `AGENTS.md`, and `docs/*.md`: no matches other than the legitimate `ToDo`
  task-status value.
- Tracked-artifact scan: `.env` has never been committed in this repository's
  history; no assignment PDF is tracked; `.gitignore` and `.dockerignore` both
  exclude `.env`, `venv/`, and caches.
- `add_tasks.py` and `scripts/seed_tasks.py`: initially removed as unreviewed
  leftovers by an earlier pass, then restored after re-reading them. Both are
  legitimate optional dev-seed utilities (`scripts/seed_tasks.py` seeds
  in-memory storage directly; `add_tasks.py` seeds over HTTP and needs the
  `requests` package, not in `requirements.txt`). Both are now documented in
  `README.md`'s Project structure section rather than deleted.
- Diff review: the tracked changes are limited to `README.md`, `AGENTS.md`,
  `docs/ai-playbook.md`, `tests/test_tasks.py`, and the two new files in
  `docs/`. `app/` and `frontend/` are unchanged.

`final-project` was pushed to `origin` and its GitHub Actions run passed (see
CI evidence above). The repository's `main` branch previously pointed at an
unrelated commit containing a mistakenly committed `venv/` (860 files) and a
broken, unregistered submodule reference for this project instead of its
history. `main` was updated to point at the same commit as `final-project`
(`0013728`) so the default branch reflects the real, current application
instead of that stray content.
