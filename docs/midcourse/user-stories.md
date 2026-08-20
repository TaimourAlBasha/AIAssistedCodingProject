# Midcourse User Stories

## Feature 1: Due dates and overdue filtering

### Story 1: Create a task with a due date

As a user, I can assign an optional due date when creating a task.

Acceptance criteria:

- A valid `YYYY-MM-DD` value is accepted and returned unchanged.
- Omitting the field produces a task with `due_date: null`.
- An invalid calendar date receives HTTP 422.

### Story 2: Edit or clear a due date

As a user, I can replace or remove a task's due date.

Acceptance criteria:

- PATCH with a valid date replaces the existing date.
- PATCH with `null` clears the date.
- PATCH without `due_date` preserves the current date.
- Other task fields remain unchanged.

### Story 3: Recognize overdue work

As a user, I can clearly recognize overdue incomplete tasks.

Acceptance criteria:

- A task is overdue only when its due date is earlier than today.
- A task due today is not overdue.
- A task in `Done` is never overdue.
- The card uses accessible text as well as visual styling.

### Story 4: Filter overdue work

As a user, I can show only overdue tasks without losing the Kanban layout.

Acceptance criteria:

- A compact control enables the overdue filter.
- All three Kanban columns remain visible.
- Columns without matches show a clear empty state.

AI assumption review:

- Confirmed by the user on 2026-08-19: backend overdue filtering uses the server's local calendar date; browser styling uses the browser's local calendar date.
- AI assumption corrected by the user: **[PLACEHOLDER — approval was provided, but no correction was made; add a real correction only if one occurs.]**

## Feature 2: Tags and tag filtering

### Story 1: Create a task with tags

As a user, I can enter a simple comma-separated list of tags.

Acceptance criteria:

- Tags are trimmed and returned as a list of strings.
- Blank tag values receive HTTP 422.
- Valid tags appear as readable chips on the card.

### Story 2: Handle duplicate tags predictably

As a user, I do not get duplicate variants of the same tag.

Acceptance criteria:

- Duplicate comparison is case-insensitive.
- The first spelling and order are retained.
- The same behavior applies to POST and PATCH.
- A task has at most 5 tags, each no longer than 30 characters.

### Story 3: Edit or clear tags

As a user, I can replace or remove all tags.

Acceptance criteria:

- PATCH with a list replaces the existing tags.
- PATCH with `[]` clears the tags.
- PATCH without `tags` preserves the current list.
- Unrelated fields remain unchanged.

### Story 4: Filter by tag

As a user, I can filter tasks by tag alongside the overdue filter.

Acceptance criteria:

- Tag matching is case-insensitive.
- Tag and overdue filters combine using AND behavior.
- Clearing filters restores all tasks.
- No matches produce clear empty states.

AI assumption review:

- Confirmed by the user on 2026-08-19: maximum 5 tags, maximum 30 characters each, case-insensitive deduplication/filtering, and preservation of the first spelling.
- AI assumption corrected by the user: **[PLACEHOLDER — approval was provided, but no correction was made; add a real correction only if one occurs.]**
