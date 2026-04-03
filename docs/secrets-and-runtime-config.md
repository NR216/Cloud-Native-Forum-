# Secrets and Runtime Configuration

This document describes how production-sensitive configuration is handled
without exposing live secret values in the repository.

## Production Secret Sources

The production stack relies on external Docker Swarm secrets rather than
committing secret values to Git:

| Secret name | Used by | Purpose |
| --- | --- | --- |
| `secret_key` | Flask app | Session signing / secret key |
| `db_password` | PostgreSQL, Flask app, postgres-exporter, backup service | Database authentication |
| `admin_password` | Flask app | Default admin account password |
| `grafana_admin_password` | Grafana | Grafana admin login |

These secrets are referenced in [`docker-stack.yml`](../docker-stack.yml) and
created outside the repository before stack deployment.

## How Secrets Are Loaded

- [`app/config.py`](../app/config.py) reads runtime secrets from `/run/secrets/<name>`
  and falls back to environment variables only when the secret file is absent.
- [`scripts/init-swarm.sh`](../scripts/init-swarm.sh) creates the expected Swarm
  secret objects during initial setup if they do not already exist.
- The production PostgreSQL password is injected through `POSTGRES_PASSWORD_FILE`
  rather than a hard-coded value.

## Development vs Production

The repository keeps only non-sensitive templates and development defaults:

- [`/.env.example`](../.env.example) contains placeholders such as `change-me`
- [`docker-compose.yml`](../docker-compose.yml) uses development-friendly defaults
- GitHub Actions test values are scoped to CI and are not production secrets

Production-only secret values are intentionally excluded from GitHub.

## Operational Credentials Kept Out of Git

The following should remain outside the repository:

- SSH login passwords or private keys
- live application admin passwords
- live Grafana passwords
- DigitalOcean account tokens
- Docker Hub access tokens
- current Swarm secret values

## Safe Repository References

It is still safe to document the following in the repository:

- public service URLs
- service names and roles
- deployment flow and command sequence
- which secret names are required
- which files or services consume each secret
