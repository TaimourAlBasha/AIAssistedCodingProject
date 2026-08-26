# AI Governance Worksheet

## What I shared with AI

| Item shared | Risk | Reason | Safer future version | Ambiguity to resolve |
| --- | --- | --- | --- | --- |
| Task Tracker source code and tests | Low | This is a public learning-project repository with no proprietary business logic or production data. | Share only the files needed for the current task and exclude unrelated workspace content. | Reclassify if the repository later becomes private or gains non-public logic. |
| GitHub repository URL, branch names, commit IDs, and CI links | Low | These values identify a public course repository and its development history but are not credentials. | Share the repository and run links only when they are needed as evidence. | Confirm visibility before treating any future repository as public. |
| Terminal errors and test output | Medium | The technical error text was useful, but absolute Windows paths exposed a user and organization context. | Replace the identifying portions with generic user and workspace labels before pasting. | Check every future log for names, email addresses, tokens, and internal hostnames. |
| Docker and GitHub Actions configuration | Low | The files contain course infrastructure configuration and no deployed environment or secret values. | Share the smallest relevant Dockerfile or workflow section instead of the entire configuration. | Reclassify if secrets, private registries, or deployment targets are added later. |
| Claude Code `/status` output | High | The live screen included a work email address, organization name, and session metadata. The final documentation intentionally omitted those personal values. | Record only the version, login type, and repository working directory; redact email, organization, session IDs, and peer addresses. | Decide whether even the organization name is necessary evidence before sharing it. |
| Feature requirements and manual browser observations | Low | These described toy-project behavior and contained no credentials, customer records, or production data. | Keep examples synthetic and avoid real names or business records in task content. | Reclassify if future examples come from real users or internal work. |

## What I received from AI

| Contribution | How it was checked | Decision |
| --- | --- | --- |
| Due-date and tag implementation across models, storage, routes, tests, and frontend | Focused tests, full pytest runs, controlled break tests, live HTTP checks, and manual browser checks | Accepted after verification. |
| Invalid-transition feedback toast | Full test suite plus manual browser review; the first position was changed after user feedback | Edited, then accepted. |
| CI workflow | Local pytest, intentional green-red-green GitHub Actions runs, and restored green run | Accepted. |
| Multi-stage Dockerfile and `.dockerignore` | Image build, `/health`, Docker health status, image user inspection, and runtime `whoami` | Accepted with the unpinned dependency trade-off documented. |
| README, docstrings, and Module 4 documentation | Claim-versus-reality audit, diff review, and `git diff --check` | Edited where claims needed correction, then accepted. |
| Module 5 security findings | Static file evidence and explicit grading as Valid, False Positive, or Noise | Retained as an AI-assisted draft pending an independent student manual observation. |

## Generated block ownership trace

The selected generated block is `Dockerfile`. It was chosen because it affects
dependency installation, runtime contents, process privileges, networking, and
health reporting.

| Line(s) | What it does | Why it is there | What could break if removed or changed | Do I own this yet? |
| --- | --- | --- | --- | --- |
| 1 | Selects the modern Dockerfile frontend syntax. | It makes the intended Dockerfile syntax explicit. | Newer syntax features may parse differently if the directive is removed in another build environment. | Confirm I can explain that this is a parser directive, not a runtime image. |
| 3 | Starts a builder stage from Python 3.11 slim. | It matches the course Python family and separates dependency installation from runtime assembly. | Changing the Python family could make installed packages incompatible with the runtime stage. | Confirm I understand why both stages must use compatible Python versions. |
| 5-6 | Disables pip's version check and package cache. | It reduces unnecessary output and cached installer data during the build. | The build would usually still work if removed, but could use more space and produce extra output. | Understandable from the environment-variable names; verify if troubleshooting pip behavior. |
| 8-10 | Uses `/build` and copies only `requirements.txt` before installation. | Dependency installation can remain cached when application files change. | Copying the full repository first would invalidate the dependency layer more often and enlarge the build context. | Confirm I understand Docker layer caching before changing copy order. |
| 12-14 | Creates `/opt/venv`, upgrades pip, and installs project requirements. | The virtual environment can be copied as one dependency unit into the runtime stage. | Removing installation leaves Uvicorn and FastAPI unavailable; changing paths breaks the runtime `PATH`. | Confirm I can trace `/opt/venv` into lines 19 and 28. |
| 17 | Starts a clean Python 3.11 slim runtime stage. | Build-time working files are not carried into the final stage. | Using an incompatible or non-Python runtime would prevent the copied environment from running. | Confirm I can distinguish builder contents from runtime contents. |
| 19-21 | Places the copied virtual environment first on `PATH` and configures Python runtime output. | Commands resolve to installed dependencies, bytecode files are avoided, and logs are unbuffered. | Without the `PATH`, `uvicorn` may not resolve; buffered logs can delay container output. | Confirm I understand that these variables affect runtime, not dependency installation. |
| 23 | Sets `/app` as the runtime working directory. | Python imports and relative frontend paths are resolved from the application location. | A different directory could break imports or the frontend file lookup. | Confirm by relating this path to the two copy instructions. |
| 25-26 | Creates a system group and non-root user named `app`. | The API does not need root privileges. | Removing these lines while keeping `USER app` prevents startup; removing all three lines would run the service as root. | Owned after verifying `docker exec tt-dev whoami` returned `app`. |
| 28 | Copies the built virtual environment from the builder. | Runtime dependencies become available without rerunning pip in the final stage. | Missing or incompatible files would prevent imports and startup. | Confirm I understand that test packages are also copied because requirements are not split. |
| 29-30 | Copies only backend and frontend runtime files and assigns them to `app`. | The runtime does not need tests, Git metadata, or course documentation. | Omitting either directory breaks the API or frontend; wrong ownership could block access. | Owned after inspecting the runtime file needs and non-root user. |
| 32 | Switches subsequent runtime activity to `app`. | It enforces non-root execution. | Removing it weakens the container security posture. | Owned and verified by both image inspection and `whoami`. |
| 34 | Documents that the container listens on port 8000. | It communicates the intended container port to users and tooling. | The service can still listen without `EXPOSE`, but expected metadata and usage become less clear. | Confirm I understand that `EXPOSE` does not publish the port by itself. |
| 36-37 | Polls `/health` and reports container health. | Docker can distinguish a running process from a responsive application. | An incorrect route, timeout, or missing Python environment would mark a healthy service unhealthy. | Owned after the container reported `healthy` and `/health` returned `ok`. |
| 39 | Starts Uvicorn on all container interfaces at port 8000 without reload. | Binding to `0.0.0.0` makes the mapped port reachable, and omitting reload avoids development behavior. | Binding only to loopback prevents host access; a wrong import path prevents startup. | Owned after the mapped `/health` request succeeded. |

## Three personal AI usage rules

| Rule category | Draft rule | Evidence from my work | What was still vague? | Revised rule |
| --- | --- | --- | --- | --- |
| What I will never paste | I will never paste secrets or sensitive data into an AI tool. | The Claude status output contained personal account and organization details that did not belong in repository documentation. | "Sensitive data" alone does not define what to remove. | I will never paste passwords, API tokens, private keys, `.env` values, customer data, or unredacted personal account details; I will redact emails, session IDs, and identifying path segments before sharing logs. |
| What I will always verify | I will verify AI suggestions before accepting them. | The project used pytest, browser checks, HTTP checks, Docker health and user checks, CI green-red-green proof, break tests, and documentation claim audits. | "Verify" does not say which evidence is required. | Before accepting an AI change, I will inspect its diff and run the smallest relevant automated check; I will also perform a browser or runtime check when behavior cannot be proven by tests. |
| How I will record contributions | I will document important AI help. | The prompt log records prompts, response summaries, and accept/edit/reject decisions; verification files separate automated and manual evidence. | "Important" could be interpreted inconsistently. | For every submitted AI-assisted feature, infrastructure change, or review, I will record the prompt or task, the AI contribution, my accept/edit/reject decision, and the verification evidence in `docs/`. |

## Governance conclusion

The project evidence shows that the safest workflow was not simply accepting
generated output. It was limiting the shared context, reviewing the actual
diff, testing behavior, recording decisions, and keeping personal or account
details out of final artifacts.
