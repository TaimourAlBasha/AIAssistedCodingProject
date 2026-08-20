# Mini-ADR: Due Dates and Tags

## Status

Approved for implementation on 2026-08-19.

## Context

The application uses Pydantic models, FastAPI routes, in-memory task storage, and a single vanilla-JavaScript frontend. The two features should extend these conventions without adding persistence technology, migrations, or a frontend framework.

## Decision

### Due dates

- Represent `due_date` as Python `date | None`.
- Serialize it as an ISO calendar date (`YYYY-MM-DD`).
- Accept it in POST and PATCH payloads.
- Use `null` in PATCH to clear it; omission preserves the current value.
- Compute overdue state rather than storing it: a task is overdue when it has a due date earlier than the server's current local date and its status is not `Done`.

### Tags

- Represent `tags` as `list[str]`, defaulting to an empty list.
- Trim whitespace and reject blank values.
- Allow at most 5 tags with at most 30 characters per tag.
- Deduplicate case-insensitively while preserving the first spelling and input order.
- Use `[]` to clear tags; omission in PATCH preserves them.

### Filtering

- Extend `GET /tasks` with optional `overdue` and `tag` query parameters.
- Match tags case-insensitively.
- Combine simultaneous filters with AND behavior.
- The frontend sends query parameters and retains all Kanban columns and empty states.

## Alternatives considered

- Arbitrary date strings were rejected because they weaken normal Pydantic validation.
- A stored `is_overdue` field was rejected because it becomes stale as dates and statuses change.
- Tag objects, IDs, colors, autocomplete, and management screens were rejected as outside scope.
- A database and migrations were rejected because the current project intentionally uses in-memory storage.
- A frontend framework was rejected because the existing page can support both features directly.

## Consequences

- The implementation stays small and uses current project conventions.
- Task data still disappears when the backend process stops.
- Server and browser local dates can briefly disagree near midnight if they are in different time zones; this was accepted for the learning-project scope.
