# Security Policy

## Supported versions

| Version | Supported          |
| ------- | ------------------ |
| 3.0.x   | :white_check_mark: |
| < 3.0   | :x:                |

## Reporting a vulnerability

If you discover a security issue, please **do not** open a public GitHub issue.

Email **hello@adamsimms.xyz** with:

- A description of the vulnerability
- Steps to reproduce
- Impact assessment (e.g. credential exposure, remote code execution)
- Any suggested fix, if you have one

We will acknowledge receipt and work on a fix as soon as possible. For credential leaks, assume rotation is required immediately.

### GitHub private vulnerability reporting

This is a **public** repository. You may also use GitHub’s [private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository) if enabled under **Settings → Code security → Private vulnerability reporting**.

Email remains supported for reporters who prefer not to use GitHub.

## Security best practices for deployments

### AWS credentials

- Never commit `secrets.env`, `config.ini`, or AWS keys to git.
- Use `secrets.env` (see `.env.example`) or environment variables when possible.
- Scope IAM permissions to a single bucket — see [docs/aws-iam-policy.json](docs/aws-iam-policy.json).
- Rotate any credentials that were ever committed to older versions of this repository.

### Local files

- `setup.sh` sets `secrets.env` and `config.ini` to mode `600`. Keep them owner-readable only.
- Log files in `logs/` may contain paths and upload metadata; restrict access on shared systems.

### S3 access

- Keep `make_public = false` unless you explicitly need public objects.
- Many buckets disable ACLs; prefer bucket policies or pre-signed URLs (see README).
- Review bucket policies and block public access settings in AWS.

### Shutdown hook

- `shutdown_after` and `--shutdown` require passwordless `sudo` for `shutdown -h now`.
- Only install [docs/sudoers-cloudberry-shutdown](docs/sudoers-cloudberry-shutdown) for the dedicated Pi user on field devices.
- Do not grant broader sudo access than necessary.

### Dependencies

- Dependabot opens PRs for pip and GitHub Actions updates.
- Review dependency updates before merging, especially on production Pis.

## Known limitations

- Cloudberry is designed for single-user, single-device field deployment — not multi-tenant or internet-exposed services.
- Preflight checks validate connectivity but do not perform full security auditing.
- Historical commits before v3.0.0 may have contained credentials in `config.ini` — rotate keys if unsure.
