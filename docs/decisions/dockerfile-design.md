# Dockerfile Design Decision

## Context

The Task Tracker is a learning-project FastAPI application that runs on Python
3.11 and serves both its API and vanilla JavaScript frontend. Module 4 requires
a reproducible container image without adding deployment, authentication, or a
database. The image must start Uvicorn on port 8000, support the existing
`/health` endpoint, avoid development reload mode, and run without root
privileges.

## Decision

Use a multi-stage Docker build based on `python:3.11-slim` for both stages. The
builder stage creates a virtual environment at `/opt/venv` and installs the
packages from `requirements.txt`. The runtime stage copies that environment and
only the `app/` and `frontend/` directories required to run the application.

The runtime image creates a system user and group named `app`, changes ownership
of the application files, and switches to `USER app` before starting the
service. Uvicorn listens on `0.0.0.0:8000` without `--reload`. Docker also checks
the existing `/health` route to report container health.

The `.dockerignore` file excludes Git metadata, environment files, virtual
environments, Python caches, test and coverage output, JavaScript dependencies,
build artifacts, and common editor or operating-system files from the Docker
build context.

## Alternatives Considered

### Single-stage image

A single-stage image would be shorter, but it would mix dependency installation
with the final runtime setup and make it easier to retain build-only files.

### Running as root

Using the base image's default root user would require less configuration, but
the application does not need root privileges. A dedicated `app` user provides
a safer runtime default.

### Development server with reload enabled

Running Uvicorn with `--reload` would be useful during local source editing, but
it is unnecessary in this self-contained image and would introduce development
behavior into the container runtime.

### Copying the entire repository

Using `COPY . .` would be simpler, but it could include tests, documentation,
local configuration, or other files that the application does not need. The
selected design explicitly copies only the backend and frontend runtime files.

## Trade-offs

The multi-stage file is longer than a minimal single-stage Dockerfile, but its
builder and runtime responsibilities are clearer. Using the slim image reduces
the base-image footprint, although troubleshooting tools commonly found in
larger images are not available by default.

All packages in `requirements.txt` are installed into the copied virtual
environment. As a result, development and test packages such as pytest and
httpx are also present in the runtime image. Splitting runtime and development
requirements could reduce the image contents, but that would change the
project's current dependency-management approach and is outside this decision.

## Consequences

- The same Python 3.11 family is used during dependency installation and at
  runtime.
- The container exposes and serves the application on port 8000.
- The application process runs as the non-root `app` user.
- Docker can monitor the application through `GET /health`.
- Local secrets and environment files are excluded from the build context.
- The image contains only the installed environment, backend, and frontend
  application files needed at runtime.
- The container is intended for course verification, not as a claim of
  production hardening or deployment readiness.

## Open Questions

- Should runtime and development dependencies be separated in a later module?
- Should dependency versions be pinned to improve reproducibility?
- Should a future deployment environment require additional health-check or
  observability behavior?

I would do this differently by separating runtime and development dependencies
if minimizing the final image became a project requirement.
