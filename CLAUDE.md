# Working rules

- KISS: the simplest, most native solution first. No abstraction without a second caller.
- Never push to `main` or `dev`. Cut `feat/`, `fix/` or `chore/` from `dev`, open a PR into
  `dev` (squash). Release = PR `dev` → `main`, then tag `vX.Y.Z`. See docs/CONTRIBUTING.md.
- Run `make check` and `uv run pre-commit run --all-files` before every commit.
- English everywhere. Project status lives in PLAN.md, not in the README.
- Secrets never in the repository or on the command line; names only in docs.

# Commands

```bash
make bootstrap                      # uv sync --locked + pre-commit hooks
make check                          # ruff, mypy, pytest with the coverage floor (what CI runs)
uv run pre-commit run --all-files
make audit                          # pip-audit against OSV.dev
```

# Infra

- Terraform in `infra/`, state in a versioned GCS bucket (`backend "gcs"`).
- Apply only from a reviewed plan: `terraform plan -out=tfplan`, show it, then `terraform apply tfplan`.
- Services are deployed by GitHub Actions, not by Terraform.
