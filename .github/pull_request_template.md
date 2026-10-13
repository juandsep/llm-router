## What and why

<!-- The change and the reason. One paragraph. -->

## How it was verified

<!-- Commands you ran and what they returned. "It works" is not verification. -->

- [ ] `make check` passes (lint + types + tests with coverage gate)
- [ ] `make docker-build` passes if the image, deps or entrypoint changed
- [ ] No secrets, tokens or `.env` values added
- [ ] Branch cut from `dev` and targeting `dev` (only `dev` merges into `main`)
- [ ] Data and model artifacts are not committed (they are fetched or produced)
- [ ] Documentation updated if behavior or configuration changed

## Risk

<!-- What breaks if this is wrong, and how to roll it back. -->
