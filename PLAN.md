# PLAN

Goal: TODO: one line describing llm-router

This file is the single source of truth for project status. The README links here instead
of repeating it. Each phase is one short-lived branch cut from `dev`, one pull request, one
concern.

## Phases

- [x] **F0 · Foundations**: repo, uv, lockfile, pre-commit, pytest, CI (gh-project-standard).
- [ ] **F1 · Data**: source and license, fetch script, processed format. Data is fetched, never committed.
- [ ] **F2 · Core**: the model or service logic, with its evaluation.
- [ ] **F3 · API**: `/health`, `/ready`, `/metrics`, API key, rate limit.
- [ ] **F4 · Infra and deploy**: Terraform, `dev` → staging, tag `v*` → production.
- [ ] **F5 · Monitoring**: metrics, Grafana dashboard, cloud alerts (p99, 5xx), drift if ML.
- [ ] **F6 · Demo and docs**: public demo, architecture diagrams, results in the README.

## Pending

Status (2026-10-12): F0 done. Next, in order:

- [ ] F1

## Decisions

- **<Topic>: <choice>.** <Why, and what was rejected.>

## Success metrics

- <Metric and threshold.>
