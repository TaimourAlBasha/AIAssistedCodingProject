# Module 5 Setup Verification

## Guardrails

- Module 5 work is documentation-first and read-only by default.
- Application files will not change unless the user approves one specific,
  minimal fix.
- Repository claims must cite inspected files rather than generic framework
  assumptions.
- AI output is a draft to grade; student judgments and personal evidence will
  not be invented.
- Separate planning and context-comparison exercises require bounded or fresh
  threads.

## Project evidence smoke test

| Claim | Evidence file | Evidence summary | Confidence | Assumption to verify |
| --- | --- | --- | --- | --- |
| The project is a FastAPI Task Tracker with task, health, version, and frontend routes. | `app/main.py` | The file constructs `FastAPI` and declares `/`, `/health`, `/version`, `/tasks`, and `/tasks/{task_id}` handlers. | High | None. |
| Task requests use explicit status and priority enums and reject unknown fields. | `app/models.py` | `TaskStatus` and `TaskPriority` define the accepted values, while create and update models use `ConfigDict(extra="forbid")`. | High | None. |
| Tasks are stored only in process memory. | `app/storage.py` | `_tasks` is a module-level dictionary used by the create, read, update, delete, and filter functions. | High | Persistence outside this module is not present in the inspected backend files. |
| Status changes are restricted to three transition pairs. | `app/business_rules.py` | `VALID_TRANSITIONS` contains `ToDo` to `InProgress`, `InProgress` to `Done`, and `Done` to `InProgress`. | High | None. |
| The frontend is a single HTML file that calls the task API and provides modal, filtering, and drag-and-drop behavior. | `frontend/index.html` | The file contains `fetch` calls, modal controls, overdue and tag filters, draggable cards, drop handlers, and a transition-error toast. | High | Browser rendering was not tested during this read-only smoke test. |

## Recent-files smoke test

This check was captured before this evidence file was created. It used
filesystem modification metadata only, not Git history. Cache,
virtual-environment, dependency, and Git-internal directories were excluded.

| File | Modified time | What the file contains | Evidence confidence |
| --- | --- | --- | --- |
| `AGENTS.md` | 2026-08-26 19:54:42 | Repository-specific architecture, commands, business rules, Module 5 boundaries, and governance instructions. | High - the file was opened and reviewed. |
| `docs/module4/verification.md` | 2026-08-26 19:17:10 | Module 4 CI, Docker, test, documentation-review, AI-tool, and repository-root evidence. | High - the file was opened and reviewed. |
| `docs/module4/reflection.md` | 2026-08-26 17:37:31 | A reflection comparing the observed Copilot and Claude Code workflows while stating that Cursor was not used. | High - the file was opened and reviewed. |

## Files inspected for setup

- `README.md`
- `requirements.txt`
- `.github/workflows/ci.yml`
- `app/main.py`
- `app/models.py`
- `app/storage.py`
- `app/business_rules.py`
- `tests/test_models.py`
- `tests/test_storage.py`
- `tests/test_tasks.py`
- `frontend/index.html`
- `docs/module4/verification.md`
- `docs/module4/reflection.md`

## Limits and items to verify

- No test or application command was run for this setup exercise.
- `pyproject.toml` is not present; dependencies are listed in the unpinned
  `requirements.txt` file.
- Python 3.11 is the course and CI target. This smoke test did not verify the
  active local Python interpreter.
- The prompt library does not specify a Module 5 branch name.
- The existing mismatch between the nested Task Tracker repository and remote
  `main` still requires facilitator guidance before a normal pull request.
