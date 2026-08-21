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

## Additional actual prompts

### P1 — Report the new-field validation failure

Features: Due dates and tags

Actual prompt: “Extra inputs are not permitted; Extra inputs are not permitted. I got this message when I wanted to add a task.”

Response summary: Inspected the live API schemas and found that port 8000 was still running the older backend, which did not recognize `due_date` or `tags`. The stale process was replaced with the updated backend, and a live task creation request using both fields succeeded.

Decision: Accepted. This was a runtime-process problem rather than an application-code defect, so the fix was to restart the correct backend without changing the feature contract.

### P2 — Test the backend changes

Features: Due dates and tags

Actual prompt: “Great, now let’s test the back end of the changes.”

Response summary: Ran nine focused due-date and tag tests, the full 27-test suite, and live HTTP checks for creation, normalization, invalid input, overdue filtering, completed-task exclusion, PATCH preservation, clearing, and combined filters. Temporary verification tasks were deleted afterward.

Decision: Accepted. The tests passed, and no production-code changes were required.

### P3 — Explain tag behavior

Feature: Tags

Actual prompt: “Explain what the tags do.”

Response summary: Explained that tags categorize tasks without affecting their status or priority. The response also described comma-separated input, tag chips, trimming, case-insensitive deduplication, limits, and tag filtering.

Decision: Accepted as a user-facing explanation. No implementation change was requested.

### P4 — Improve invalid-transition feedback

Feature: Existing task workflow

Actual prompt: “I think we can add a pop up message in case of invalid transition.”

Response summary: Replaced the native browser `alert()` used after rejected drag-and-drop transitions with an accessible in-app toast showing the backend business-rule message.

Decision: Edited after review. The first toast appeared in the bottom-right corner, but the user requested that it be centered.

### P5 — Center the transition popup

Feature: Existing task workflow

Actual prompt: “Can we make a pop up in the center of the screen?”

Response summary: Repositioned the transition toast in the center of the viewport and added a dedicated animation that preserves its centered transform.

Decision: Accepted. The full 27-test suite continued to pass.
