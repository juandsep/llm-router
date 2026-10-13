## Release

<!-- dev -> main. This PR must be a merge commit or squash of an already-reviewed dev. -->

## Evidence

- Coverage: <!-- paste the number from the CI run -->
- Checks in green: <!-- CI, CodeQL, gitleaks -->
- Version in `pyproject.toml`:

## After merge

- [ ] Tag `v<version>` from `main` (this is what triggers `release.yml`)
- [ ] Image published to GHCR with provenance and SBOM
- [ ] Release notes reviewed (`--generate-notes` output)

## Rollback

<!-- Previous tag to redeploy, or the revert PR. -->
