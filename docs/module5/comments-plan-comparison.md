# Comments Plan Comparison and Critique

## Section critique

| Section | Label | Evidence | Minimal correction |
| --- | --- | --- | --- |
| Data Model | Right | The grounded plan places request and response models in `app/models.py`, uses the existing extra-field policy, UUID strings, UTC timestamps, and avoids changing `TaskResponse`. | Keep the separate-resource decision unless a product requirement demands embedded comments. |
| API Routes | Right | The two nested routes fit the route organization in `app/main.py` and distinguish a missing task from an empty comment list. | Document the chosen ordering in the eventual route docstring and tests. |
| Tests | Right | Test names follow the repository's model, storage, and TestClient split and cover happy path, validation, isolation, and missing parents. | Add the deletion-lifecycle test after that rule is decided. |
| Frontend Changes | Right | The plan names `frontend/index.html`, reuses its modal, `fetch`, `apiBase`, DOM creation, `textContent`, validation, and accessibility patterns. | Keep the known port-5500 API-base issue as a separate task. |
| Migration Notes | Right | The plan correctly identifies process-local storage, no database migration, reset isolation, task-response compatibility, and script impact. | Replace the open deletion note with the selected lifecycle rule before implementation. |
| Open Questions | Needs-Resequencing | The questions are real and repository-specific, but author semantics and task-deletion behavior affect the model, routes, storage, tests, and UI. | Resolve questions 1 and 2 before treating the earlier sections as implementation-ready. |

## Generic versus repo-grounded comparison

**Biggest difference:** The generic plan must consider database, document, and
in-memory possibilities, while the grounded plan can name the actual Pydantic
models, FastAPI route module, in-memory dictionary, pytest layout, and
single-file frontend.

**Plan I would hand to a teammate:** I would hand over the repo-grounded plan
after resolving task-deletion behavior and author semantics because its file
locations, test names, compatibility choice, and UI constraints match this
repository.

**When generic chat is enough:** A generic plan is useful for early feature
scope, vocabulary, and open-question discovery before a repository or
implementation approach has been selected.

## Human review verdict

The repo-grounded plan is more actionable, but it is not authorization to
implement comments. The lifecycle and author decisions are deliberately left
open because choosing them without product input would create hidden business
rules.
