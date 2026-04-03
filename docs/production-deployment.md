# Production Deployment Notes

This document contains non-sensitive information about the production deployment.
It is safe to keep in the GitHub repository because it does not include passwords,
private keys, or other live secrets.

## Environment Summary

- Cloud provider: DigitalOcean
- Region: Toronto (`tor1`)
- Host type: single Ubuntu Droplet
- Orchestration: Docker Swarm (single-node deployment)
- Live forum URL: `http://137.184.164.255:5000`
- Public monitoring URLs:
  - Prometheus: `http://137.184.164.255:9090`
  - Grafana: `http://137.184.164.255:3000`

## Production Stack

The current production stack is defined in [`docker-stack.yml`](../docker-stack.yml)
and includes the following services:

| Service | Replicas / Mode | Purpose |
| --- | --- | --- |
| `forum_app` | 3 replicas | Flask application |
| `forum_postgres` | 1 replica | PostgreSQL database |
| `forum_redis` | 1 replica | Redis sessions and Socket.IO backend |
| `forum_prometheus` | 1 replica | Metrics collection |
| `forum_grafana` | 1 replica | Monitoring dashboards |
| `forum_node-exporter` | global | Host-level metrics |
| `forum_postgres-exporter` | 1 replica | PostgreSQL metrics exporter |
| `forum_backup` | 1 replica | Hourly database backup job |
| `forum_auto-scaler` | 1 replica | Prometheus-driven scaling worker |

## Persistent Data

The deployment uses named Docker volumes for:

- `postgres-data`
- `redis-data`
- `prometheus-data`
- `grafana-data`
- `backup-data`
- `uploads-data`

These volumes preserve application state across container restarts and redeploys.

## Deployment Flow

The production deployment is designed to follow this flow:

1. Initialize Docker Swarm on the server with [`scripts/init-swarm.sh`](../scripts/init-swarm.sh).
2. Build the application image as `forum-app:latest`.
3. Create required external Docker Swarm secrets before deploying the stack.
4. Deploy the stack with [`scripts/deploy-stack.sh`](../scripts/deploy-stack.sh).
5. Verify health checks, service replicas, and public endpoints.

## Demo Data

When `LOAD_DEMO_SEED=true`, the application initialization path loads demo
content from [`migrations/seed_demo.sql`](../migrations/seed_demo.sql).
That file defines the seeded forum users, posts, replies, and likes used for
demo and grading-friendly exploration.

## Operations Endpoints

- App home: `http://137.184.164.255:5000`
- Admin login page: `http://137.184.164.255:5000/admin/login`
- Health endpoint: `http://137.184.164.255:5000/health`
- Metrics endpoint: `http://137.184.164.255:5000/metrics`
- Prometheus: `http://137.184.164.255:9090`
- Grafana: `http://137.184.164.255:3000`

## Backup and Restore

The repository includes:

- [`scripts/backup.sh`](../scripts/backup.sh) for periodic database backups
- [`scripts/restore.sh`](../scripts/restore.sh) for restoration from a selected backup

## What Is Intentionally Excluded

This document does not include:

- SSH passwords or private keys
- application admin passwords
- Grafana login passwords
- Docker Hub credentials
- DigitalOcean API tokens
- live Docker Swarm secret values
