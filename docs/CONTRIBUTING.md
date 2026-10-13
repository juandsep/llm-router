# Contributing

## Branches

`main` is production. `dev` is the integration branch. Every change goes through a pull request.

```
feat/<topic>  ──PR──>  dev  ──PR──>  main  ──tag v*──>  release
fix/<topic>
chore/<topic>
```

- Cut topic branches from `dev`, never from `main`.
- Only `dev` merges into `main`, and only through a release PR (`.github/PULL_REQUEST_TEMPLATE/release.md`).
- `dev` and `main` are protected by rulesets (`.github/rulesets/`): no direct pushes, no force pushes,
  required checks must pass. If a push is rejected, you are on the wrong branch — that is the rule working.

## Commits

Conventional Commits, imperative, English, one logical change per commit:

```
feat(scoring): add batch endpoint
fix(config): stop silently defaulting to the latest model version
chore(ci): pin codeql-action
```

## Local commands

```bash
make bootstrap   # environment + git hooks (idempotent)
make check       # exactly what CI runs: lint, types, tests with the coverage gate
make docker-build
```

Install the hooks once; they run on every commit. Bypassing them with `--no-verify` is a review finding,
not a shortcut. If a hook is wrong, fix the hook in `.pre-commit-config.yaml`.

## Coverage

The floor lives in `pyproject.toml` (`[tool.coverage.report] fail_under`). Measure the real number before
changing it, and never lower it in the same PR that reduces coverage without saying so in the description.

## Secrets

Never commit a token, key or `.env` file. Local values go in `.env` (gitignored); CI values go in
GitHub Environments, and cloud auth uses OIDC so no long-lived cloud secret exists at all.

If a secret leaks: rotate it first, then clean the history. Assume anything pushed is public.

## Releases

1. Merge the release PR into `main`.
2. Tag it: `git tag v0.1.0 && git push origin v0.1.0` (the tag must match `version` in `pyproject.toml`).
3. `release.yml` runs tests, publishes the image to GHCR with provenance and SBOM, and creates the Release.
