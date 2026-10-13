# Security

## Reporting a vulnerability

Use GitHub private vulnerability reporting (Security tab → Report a vulnerability) instead of opening a
public issue: https://github.com/juandsep/llm-router/security/advisories/new

Include the affected version or commit, the impact, and the smallest reproduction you have.
Expect an initial reply within a few days. This is a personal project with no support SLA — say so if you
need one.

## Scope

In scope: this repository's code, workflows and dependencies.
Out of scope: third-party services, infrastructure the project does not own, and issues that require an
already-compromised environment.

## Controls already in place

- `gitleaks` and `detect-secrets` scan every commit (pre-commit) and every push (CI).
- CodeQL runs on push, pull request and weekly.
- `pip-audit` and Dependabot report vulnerable dependencies.
- Actions are pinned to commit SHAs, and `zizmor` fails the commit when a workflow is unsafe.
- Workflows default to `permissions: contents: read` and ask for more per job.

## Rotating a leaked secret

Rotate first — assume a pushed secret is already public. Then clean the history and re-run the scanners.
Deleting the commit is not remediation.
