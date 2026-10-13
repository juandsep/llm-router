# llm-router

[![CI](https://github.com/juandsep/llm-router/actions/workflows/ci.yml/badge.svg)](https://github.com/juandsep/llm-router/actions/workflows/ci.yml)
[![CodeQL](https://github.com/juandsep/llm-router/actions/workflows/codeql.yml/badge.svg)](https://github.com/juandsep/llm-router/actions/workflows/codeql.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A personal LLM gateway. A fine-tuned [Laya](https://github.com/NandhaKishorM/laya)
reads each prompt and decides whether it is easy, mid or hard, then the gateway
sends it to a cheap, middle or best model, so only hard prompts pay for the
best one.

**Status:** F0 only. The stock Laya scores 5/10 zero-shot on hand-labelled
prompts and puts almost everything in mid, so fine-tuning (F2) is the core of
the project. Phases, decisions and the tier map are in [PLAN.md](PLAN.md).

```bash
uv sync
uv run python scripts/zero_shot.py   # zero-shot baseline, downloads the checkpoints on first run
```

## Quickstart

```bash
make bootstrap   # environment + hooks
make check       # lint, types, tests with coverage gate
```

## Layout

```
src/llm_router/   package code (imported by everything else)
tests/             tests, one file per behavior area
docs/              contributing, security, model notes
.github/           workflows, dependabot, templates, rulesets
```

## Commands

| Command | What it does |
|---|---|
| `make bootstrap` | Create the environment and install the git hooks |
| `make check` | Lint + types + tests with the coverage gate (what CI runs) |
| `make format` | Apply automatic fixes |
| `make audit` | Dependency vulnerabilities against OSV.dev |
| `make docker-build` | Build the image the way CI does |

## Contributing

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md). Short version: branch from `dev`, open a PR, keep the
checks green, and only `dev` merges into `main`.
