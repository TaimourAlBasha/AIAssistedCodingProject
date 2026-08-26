# Comments on Tasks - Repository-Grounded Plan

This is a design document only. It does not authorize implementation.

## Data Model

Add comment request and response models beside the task models in
`app/models.py`, following the existing split between client-supplied fields
and server-generated response fields.

- A create model should accept `author` and `body` only.
- Both fields should be stripped before validation.
- `author` must contain 1-100 characters after trimming.
- `body` must contain 1-2000 characters after trimming.
- Extra request fields should be rejected, matching `TaskCreate` and
  `TaskUpdate`.
- A response model should add server-generated `id`, `task_id`, and
  `created_at` fields.
- Identifiers should follow the existing string UUID convention in
  `app/storage.py`.
- Timestamps should use timezone-aware UTC values, matching task creation.

Keep comments as a separate resource rather than adding a comments list to
`TaskResponse`. This preserves the current task response contract used by
`app/main.py`, `tests/`, and `frontend/index.html`.

For the current in-memory architecture, comment storage belongs in
`app/storage.py`. A separate dictionary keyed by comment ID, plus task-based
lookup functions, fits the existing module pattern. The storage reset used by
tests would also need to clear comments.

## API Routes

Add the smallest route set to `app/main.py`:

| Method and path | Request | Success response | Error cases |
| --- | --- | --- | --- |
| `POST /tasks/{task_id}/comments` | Comment create model containing `author` and `body` | HTTP 201 with the comment response model | HTTP 404 when the task does not exist; HTTP 422 for model validation |
| `GET /tasks/{task_id}/comments` | No request body | HTTP 200 with a list of comment response models | HTTP 404 when the task does not exist |

Before either operation, use `storage.get_task_by_id` to distinguish a missing
task from a task with no comments. Return an empty list for an existing task
that has no comments. Return comments in a documented stable order; oldest
first matches append and display order.

Do not add edit or delete routes until comment ownership and mutability are
decided. Do not add authentication as part of this feature plan.

## Tests

Follow the existing division between model tests in `tests/test_models.py`,
storage tests in `tests/test_storage.py`, and API tests using the `client`
fixture in `tests/test_tasks.py`.

### Happy path

- `test_create_comment_returns_generated_fields_and_utc_timestamp`
- `test_list_comments_for_task_returns_oldest_first`
- `test_comments_are_scoped_to_their_parent_task`
- `test_existing_task_without_comments_returns_empty_list`

### Validation

- `test_create_comment_strips_author_and_body`
- `test_create_comment_rejects_blank_author`
- `test_create_comment_rejects_author_over_100_characters`
- `test_create_comment_rejects_blank_body`
- `test_create_comment_rejects_body_over_2000_characters`
- `test_create_comment_rejects_extra_fields`

### Edge cases

- `test_create_comment_for_missing_task_returns_404`
- `test_list_comments_for_missing_task_returns_404`
- `test_comment_ids_are_unique`
- `test_storage_reset_clears_comments`
- Add a deletion-lifecycle test after the team resolves whether task deletion
  cascades to comments.

## Frontend Changes

The frontend is entirely in `frontend/index.html`, so no framework or new
frontend build system is needed. Extend the existing task modal with a comments
section that appears when editing an existing task; a task must exist before a
comment can be posted.

The section should provide:

- A loading state while comments are fetched.
- An empty state for a task with no comments.
- A chronological list using DOM creation and `textContent`, matching the
  current safe rendering approach for task values.
- Author and body controls with visible validation messages.
- A disabled submit state during the POST request.
- An error state that preserves the entered text when submission fails.
- Focus management and an accessible status message for successful or failed
  submission.

Use the existing `apiBase` and `fetch` conventions. Do not redesign the board
or introduce a frontend framework. The known port-5500 API-base issue should be
handled separately rather than hidden inside comments work.

## Migration Notes

- There is no database migration because `app/storage.py` is process-local
  memory.
- Existing tasks require no conversion if comments remain a separate resource.
- Restarting the backend will remove comments, just as it removes tasks.
- `_reset()` must clear comment state so tests remain isolated.
- Decide and test what happens to comments when `delete_task` removes a parent.
- `add_tasks.py` and `scripts/seed_tasks.py` do not need comment changes for the
  minimum feature because comments are optional and neither script is part of
  the application runtime.
- README would need endpoint and limitation updates only if implementation is
  later approved.

## Open Questions

1. Should deleting a task delete its comments immediately, or should deletion
   be rejected while comments exist?
2. Is a client-supplied author acceptable for this no-auth learning project, or
   should the UI use a fixed demonstration name?
3. Are comments immutable in the first version, or are edit and delete routes
   required?
4. Should comments display oldest-first or newest-first?
5. Should task cards show a comment count without embedding comment bodies?
6. At what count would pagination become necessary for in-memory storage?
7. Should comment limits share constants with task validation or remain
   comment-specific constants in `app/models.py`?

The task-deletion rule and author semantics must be decided before
implementation because they affect storage functions, route contracts, tests,
and UI wording.

## Files read

- `AGENTS.md`
- `README.md`
- `app/models.py`
- `app/main.py`
- `app/storage.py`
- `app/business_rules.py`
- `tests/test_models.py`
- `tests/test_storage.py`
- `tests/test_tasks.py`
- `frontend/index.html`
- `add_tasks.py`
- `scripts/seed_tasks.py`

## Assumptions to verify

- Create and list are the intended minimum comment operations.
- Comments should not be embedded in every task response.
- Oldest-first ordering is acceptable.
- The task-deletion and author rules remain undecided.
- No comment implementation is authorized by this plan.
