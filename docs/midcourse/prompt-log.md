# Prompt Log

This log records prompts actually supplied during the project. The feature entries are labeled excerpts because they came from one detailed master prompt, not separate user messages.

## Due-date feature

### D1 — Data and update contract

Actual prompt excerpt: “Add an optional `due_date` to tasks… Accept `due_date` during task creation and updates… Allow the due date to be cleared…”

Response summary: Proposed Pydantic `date | None`, ISO serialization, PATCH omission for preservation, and `null` for clearing.

Decision: Accepted by the user without edits on 2026-08-19.

### D2 — Overdue behavior and filtering

Actual prompt excerpt: “Define a task as overdue when it has a due date earlier than today and is not in the project’s completed status. Add an overdue filter…”

Response summary: Proposed computed overdue state, `Done` exclusion, and `GET /tasks?overdue=true`.

Decision: Accepted. A server-local date assumption was explicitly surfaced and confirmed.

### D3 — Verification and Break Test

Actual prompt excerpt: “Temporarily introduce a small, controlled defect… Confirm and record that the test fails… Restore the correct implementation.”

Response summary: The completed-status predicate was temporarily reversed. The focused test failed, the predicate was restored, and the test passed.

Decision: Accepted and executed; no mutation remains.

## Tag feature

### T1 — Representation and validation

Actual prompt excerpt: “Add tags to tasks using the simplest representation… Normalize tags… Reject blank tag values… Prevent duplicates…”

Response summary: Proposed `list[str]`, trimming, blank rejection, case-insensitive deduplication, and first-spelling preservation.

Decision: Accepted by the user without edits.

### T2 — Limits and filtering

Actual prompt excerpt: “Apply modest limits… Support filtering tasks by tag through the existing task-list endpoint.”

Response summary: Proposed 5 tags, 30 characters per tag, and case-insensitive exact tag filtering that combines with overdue filtering using AND.

Decision: Accepted and covered by focused tests.

### T3 — Frontend interaction and Break Test

Actual prompt excerpt: “Use a simple interaction… Render tags as readable chips… Add a compact tag-filter control… Perform at least two genuine Break Tests…”

Response summary: Implemented comma-separated entry, chips, Apply/Clear filters, and a controlled case-sensitivity mutation detected by the focused test.

Decision: Accepted and executed; no mutation remains.

## Genuine weak prompt and stronger rewrite

Weak prompt actually received: “approved”

Why it was weak: It did not explicitly name which assumptions were approved or whether Git branching and implementation were also authorized.

Stronger rewrite (recommended afterward; not claimed as an actual user message): “I approve the server-local overdue rule and the proposed tag limits/deduplication rule. Continue implementation on `mid-course-project`, but keep correction placeholders where I have not actually corrected an AI assumption.”

Response summary: The approval was interpreted using the immediately preceding review request, then implementation proceeded with both assumptions documented.

Decision: The original approval was accepted in context; the stronger wording is retained as a learning example.

## Additional prompt placeholders

- User-authored due-date prompt added later: **[PLACEHOLDER]**
- User-authored tag prompt added later: **[PLACEHOLDER]**

## Manual-review follow-up

Actual prompt: “I think we can add a pop up message in case of invalid transition.”

Response summary: Replaced native drag-and-drop `alert()` calls with a styled, accessible in-app toast that displays the backend business-rule detail and network failures.

Decision: The user's review changed the frontend behavior. Static checks confirmed the toast element and function are present and no native `alert()` call remains; the full backend suite still passed.
