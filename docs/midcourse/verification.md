# Midcourse Verification Record

## Baseline

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

Result: 16 passed, 2 deprecation warnings in 0.36s.

```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

Result: 15 tests passed. The pytest function in `test_tasks.py` is not discovered by `unittest`.

```powershell
.\venv\Scripts\python.exe -m compileall -q app tests scripts add_tasks.py
```

Result: PASS. Read-only live checks also returned `status=ok` from `/health` and HTTP 200 from `/`.

## Focused due-date checks

```powershell
.\venv\Scripts\python.exe -m pytest tests\test_tasks.py -k "due_date or overdue" -q
```

Result: 4 passed, 1 deselected, 1 warning in 1.30s. Coverage includes valid and invalid dates, overdue incomplete work, completed-task exclusion, and preservation/clearing during PATCH.

## Due-date Break Test

The condition `task.status != TaskStatus.DONE` in `is_task_overdue` was temporarily changed to `task.status == TaskStatus.DONE`.

```powershell
.\venv\Scripts\python.exe -m pytest tests\test_tasks.py::test_overdue_filter_includes_incomplete_and_excludes_completed_tasks -q
```

Mutated result: 1 failed in 1.19s. The returned ID belonged to the completed task instead of the expected incomplete task.

The correct condition was restored. Re-run result: 1 passed in 0.77s. No mutation remains.

## Focused tag checks

```powershell
.\venv\Scripts\python.exe -m pytest tests\test_tasks.py -k "tag or combines" -q
```

Result: 5 passed, 5 deselected, 1 warning in 0.67s. Coverage includes normalization/deduplication, blank rejection, updates and preservation, case-insensitive filtering, and combined filtering.

```powershell
.\venv\Scripts\python.exe -m pytest tests\test_models.py -q
```

Result after adding tag-limit checks: 10 passed in 0.23s.

## Tag Break Test

The comparison `task_tag.casefold() == comparison_tag` was temporarily changed to `task_tag == comparison_tag`.

```powershell
.\venv\Scripts\python.exe -m pytest tests\test_tasks.py::test_filter_tasks_by_tag_case_insensitively -q
```

Mutated result: 1 failed in 0.98s because the response was empty.

The case-insensitive comparison was restored. Re-run result: 1 passed in 0.78s. No mutation remains.

## Focused refactor behavior contract

Refactor: two duplicate frontend expressions for detecting active filters were replaced with `hasActiveFilters()`. The filter bar was also allowed to wrap responsively. No API or data behavior changed.

Before refactor:

- Full pytest suite: 25 passed, 2 warnings in 1.07s.
- Python compile check: PASS.
- Static frontend presence checks: all six required hooks/text values present.

After refactor:

- Full pytest suite: 25 passed, 2 warnings in 0.97s.
- Python compile check: PASS.
- The same six frontend presence checks passed.

Two tag-limit tests were added afterward; the final full-suite result is recorded during final verification.

## Final automated verification

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

Result: 27 passed, 2 existing deprecation warnings in 1.33s.

```powershell
.\venv\Scripts\python.exe -m compileall -q app tests scripts add_tasks.py
```

Result: PASS.

`git diff --check` reported no whitespace errors. Git inspection confirmed that `.env`, virtual environments, pytest caches, and Python bytecode remain ignored and are not tracked.

## Live HTTP smoke check

The updated app was started on isolated port 8001. Verified results:

- Health `ok` and root HTTP 200
- Created an overdue task with `[' API ', 'api', 'Backend']`
- Response normalized tags to `['API', 'Backend']`
- Combined `overdue=true&tag=api` filter returned the task
- PATCH cleared `due_date` and tags
- Smoke-test task was deleted afterward

## Frontend automation

There is no frontend test, lint, or build configuration. Node.js is not installed, so an attempted inline JavaScript syntax check could not run. Static source checks verified the due-date control, tag control, filters, overdue text, and filtered empty-state text.

After manual-review feedback, native drag-and-drop alerts were replaced with an accessible in-app transition toast. Static checks confirmed the toast element and display function are present and no `alert()` call remains. The full suite still passed with 27 tests; visual confirmation of the new toast remains manual.

## Manual checks still required

- Create a task with a due date and tags in the browser.
- Edit the date and tags, then clear the due date.
- Confirm overdue styling appears for past incomplete tasks only.
- Confirm a completed past-due task is not styled or filtered as overdue.
- Filter by overdue, tag, and both together.
- Confirm no-match filters retain all columns and clear empty states.
- Recheck create, edit, and drag/status transitions.
- Trigger an invalid drag transition and confirm the new popup is readable and disappears after five seconds.
- Verify DELETE through the API if desired; the frontend has no delete control.
- Inspect the browser console and Network panel for errors.

No browser behavior, console result, screenshot, or manual observation is claimed as verified here.
