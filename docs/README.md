# Cloudberry documentation

| Document | Audience | Purpose |
|----------|----------|---------|
| [../README.md](../README.md) | Everyone | Install, config, CLI, field deployment |
| [../CONTRIBUTING.md](../CONTRIBUTING.md) | Contributors | Dev setup, tests, PR workflow |
| [../SECURITY.md](../SECURITY.md) | Everyone | Vulnerability reporting, deployment security |
| [../CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) | Contributors | Community standards |
| [../CHANGELOG.md](../CHANGELOG.md) | Maintainers | Release notes |
| [../LICENSE](../LICENSE) | Everyone | MIT license |
| [migration-v3.md](migration-v3.md) | Field operators | Upgrade guide from v2 / piberry |
| [field/secrets-reference.md](field/secrets-reference.md) | Field operators | Historical secrets (not loaded by app) |
| [aws-iam-policy.json](aws-iam-policy.json) | Operators | Minimal S3 IAM policy |
| [sudoers-cloudberry-shutdown](sudoers-cloudberry-shutdown) | Field operators | Passwordless shutdown for WittyPi |
| [github-repo-settings.md](github-repo-settings.md) | Maintainers | GitHub About/topics/release checklist |

## Contributing to docs

- User-facing changes: update `README.md` and `CHANGELOG.md`.
- Config keys: update `config.ini.example` and README config table.
- Field hardware: add files under `docs/field/` and list them in `docs/field/README.md`.
