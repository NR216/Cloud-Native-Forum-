# Cloud-Native Forum

## Pending Items Before Final Submission

### Must Complete

- [ ] Add missing email information for team members whose email is still unavailable.
- [ ] Add the final `ai-session.md` file required by the deliverable.
- [ ] Add the final video demo link in the `## Video Demo` section.
- [ ] Replace the screenshot placeholders with actual visible screenshots in the README.

### Final Verification

- [ ] Confirm the live deployment URL remains accessible during grading.
- [ ] Proofread the README one final time for wording, consistency, and formatting.
- [ ] Confirm the instructor and TAs are added as collaborators if the GitHub repository remains private.
- [ ] If sensitive credentials are required for grading, send them to TA Yiren Zhao and add the exact text `Credentials sent to TA` in the Development Guide.

This is a stateful cloud-native anonymous discussion forum built with Flask, PostgreSQL, Redis, Docker, and Docker Swarm. It combines a student-oriented discussion product with deployment, persistence, monitoring, and operations work required for the course project.

## Team Information

| Name | Student Number | GitHub Username | Email |
| --- | --- | --- | --- |
| Yinghao Wang | 1012814750 | supperbon | TBD |
| Nairui Tian | 1012435330 | NR216 | n.tian@mail.utoronto.ca |
| Cunming Liu | 1012826248 | cunming666 | cunming.liu@mail.utoronto.ca |
| Ciliang Zhang | 1011618304 | EdisonZHANG123 | TBD |

Repository: https://github.com/NR216/Cloud-Native-Forum-.git

## Motivation

Many student discussion spaces are either too public, too fragmented, or not very suitable for honest academic conversation. We wanted to build a forum where users can ask questions, share project progress, discuss technical problems, and post anonymous feedback when needed, while still demonstrating cloud-native engineering practices instead of only building a simple web app.

Our main goal was to combine a useful campus-style discussion product with the operational side of modern cloud systems, including containers, orchestration, persistence, monitoring, backup, recovery, and controlled deployment.

## Objectives

We focused on the following objectives:

1. Build a stateful anonymous forum with user accounts, posts, replies, likes, reports, and an admin portal.
2. Store application state reliably with PostgreSQL and persistent Docker volumes.
3. Support real-time updates so new posts, replies, and likes appear without manual refresh.
4. Deploy the application using cloud-native tooling instead of a single local process.
5. Add monitoring, health checks, and operations tooling for a more production-oriented workflow.
6. Demonstrate multiple advanced course features beyond the core minimum requirements.

## Technical Stack

### Backend

- Flask 3.1
- Flask-SocketIO
- Flask-Session
- Flask-Limiter
- Gunicorn with Eventlet
- Psycopg2

### Data and Messaging

- PostgreSQL 16
- Redis 7

### Infrastructure and Deployment

- Docker
- Docker Compose
- Docker Swarm
- DigitalOcean deployment target

### Monitoring and Operations

- Prometheus
- Grafana
- Node Exporter
- PostgreSQL Exporter
- Backup and restore shell scripts
- Auto-scaling script for Swarm

### CI/CD and Testing

- GitHub Actions
- Pytest

## Features

### Core Forum Features

- User registration and login
- Dedicated admin login and admin dashboard
- Create, view, and delete posts
- Image upload support for posts
- Reply to posts
- Anonymous post support
- Anonymous reply support
- Like and unlike posts
- Report posts for admin review
- Role-based access control for admin-only actions

### Real-Time Features

- Live post broadcast with Socket.IO
- Live reply updates
- Live like count updates
- Live delete propagation for posts and replies

### Admin Features

- Admin dashboard with forum statistics
- User management
- Role toggling between user and admin
- Post moderation
- Report review and dismissal
- System status page with service information

### Reliability and Operations Features

- PostgreSQL persistent storage
- Redis-backed sessions
- Health endpoint
- Prometheus metrics endpoint
- Prebuilt Grafana dashboard
- Automated backup script
- Restore script
- Swarm deployment configuration with replicas and rolling updates
- Auto-scaling logic based on Prometheus metrics

## Course Requirement Mapping

### Core Technical Requirements

- Containerization: Docker and Docker Compose are used for local development and service orchestration.
- State Management: PostgreSQL stores persistent application data and uses Docker volumes.
- Deployment: The project has been deployed on DigitalOcean using Docker Swarm.
- Orchestration: Docker Swarm is used with replication, rolling updates, and service definitions in `docker-stack.yml`.
- Monitoring: Prometheus, Grafana, exporters, metrics, and health checks are included.

### Advanced Features Implemented

This project implements more than the required minimum of two advanced features:

1. Real-time communication with Flask-SocketIO and Redis.
2. Security mechanisms including authentication, RBAC, secrets-based production configuration, and rate limiting.
3. CI/CD with GitHub Actions.
4. Backup and recovery scripts.
5. Auto-scaling support for the application service.

## System Architecture

The application follows a multi-service architecture:

- `app`: Flask forum application served by Gunicorn/Eventlet.
- `postgres`: Primary relational database.
- `redis`: Session and message-queue backend.
- `prometheus`: Metrics collection.
- `grafana`: Monitoring dashboards.
- `node-exporter`: Host-level metrics.
- `postgres-exporter`: PostgreSQL metrics.
- `backup`: Periodic database backup service in Swarm deployment.
- `auto-scaler`: Prometheus-driven scaling worker in Swarm deployment.

At the application level, the Flask app is organized into Blueprints for authentication, posts, replies, likes, reports, admin, health, and metrics.

## User Guide

### Main User Flow

1. Register a new account on the forum.
2. Log in as a normal user.
3. Create a post with or without an image.
4. Choose whether to publish the post anonymously.
5. View other posts, reply, and like content.
6. Report inappropriate posts if needed.

### Admin Flow

1. Open the dedicated admin portal.
2. Log in with an admin account.
3. Review platform statistics.
4. Manage users and roles.
5. Moderate posts and reports.
6. Inspect system status and monitoring links.

### Example Local URLs

- Forum home: `http://localhost:5001`
- Health check: `http://localhost:5001/health`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

All major features can be accessed through the web navigation interface.

## Development Guide

### Prerequisites

- Docker
- Docker Compose
- Python 3.12+ if running outside containers

### Local Development with Docker Compose

1. Clone the repository.
2. Create a local `.env` file or update environment variables as needed.
3. Start the stack:

```bash
docker compose up -d --build
```

4. Open the forum in the browser.
5. Stop the stack when finished:

```bash
docker compose down
```

### Local Python Setup (Optional)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python wsgi.py
```

### Running Tests

```bash
pytest tests -v
```

Credentials sent to TA

## Deployment Information

- Live deployment URL: `http://137.184.164.255:5000`
- Target production environment: a DigitalOcean Droplet (Toronto region) using Docker Swarm.
- Public monitoring endpoints:
  - Prometheus: `http://137.184.164.255:9090`
  - Grafana: `http://137.184.164.255:3000`

### Docker Swarm Deployment

The production configuration in `docker-stack.yml` includes:

- a replicated Flask app service with 3 replicas
- PostgreSQL and Redis for stateful runtime data
- Prometheus, Grafana, node-exporter, and postgres-exporter for observability
- a scheduled backup service
- an auto-scaler service
- named volumes for persistent data
- external Docker Swarm secrets for production-only credentials
- demo seed content loaded from `migrations/seed_demo.sql` when `LOAD_DEMO_SEED=true`

### Production Stack Summary

The production deployment uses a single DigitalOcean Droplet running Docker Swarm
in single-node mode. The stack includes:

- `forum_app` with 3 replicas
- `forum_postgres` for persistent relational data
- `forum_redis` for sessions and Socket.IO backend
- `forum_prometheus` for metrics collection
- `forum_grafana` for dashboards
- `forum_node-exporter` for host-level metrics
- `forum_postgres-exporter` for PostgreSQL metrics
- `forum_backup` for scheduled backups
- `forum_auto-scaler` for metric-driven scaling logic

### Persistent Data

The production deployment uses named Docker volumes for:

- `postgres-data`
- `redis-data`
- `prometheus-data`
- `grafana-data`
- `backup-data`
- `uploads-data`

These volumes preserve application state across container restarts and redeployments.

### Swarm Initialization

```bash
./scripts/init-swarm.sh
```

### Stack Deployment

```bash
./scripts/deploy-stack.sh
```

### Deployment Flow

The intended production deployment flow is:

1. SSH into the DigitalOcean Droplet.
2. Initialize Docker Swarm with `./scripts/init-swarm.sh`.
3. Build the application image as `forum-app:latest`.
4. Ensure the required external Docker Swarm secrets exist before deployment.
5. Deploy the stack with `./scripts/deploy-stack.sh`.
6. Verify service health, public endpoints, and replica status.

### Backup and Restore

Backup and restore scripts are provided in:

- `scripts/backup.sh`
- `scripts/restore.sh`

### Demo Data

When `LOAD_DEMO_SEED=true`, the application initialization path loads demo forum
content from `migrations/seed_demo.sql`. That seed file defines the demo users,
posts, replies, and likes used during grading and demo walkthroughs.

### Secret Handling

Production-sensitive values are intentionally not stored in the GitHub repository.
The production stack expects external Docker Swarm secrets for:

- `secret_key`
- `db_password`
- `admin_password`
- `grafana_admin_password`

The application reads these values at runtime from `/run/secrets/...`, while
development defaults remain in `.env.example` and `docker-compose.yml`.

### Deployment Notes

- The project is intended to remain online during grading.
- Production secrets should be created before Swarm deployment.
- Monitoring services should be enabled during demo and evaluation.
- Sensitive access credentials are intentionally kept out of the GitHub repository.
- SSH access information, admin login information, and monitoring login details
  should be retrieved from the separate credentials package sent to the TA.

## Source Code Contents

The repository includes the following required implementation artifacts:

- application source code
- Dockerfile
- Docker Compose configuration
- Docker Swarm stack configuration
- database schema in `migrations/init.sql`
- monitoring configuration for Prometheus and Grafana
- backup, restore, deployment, and auto-scaling scripts
- test suite for key routes
- environment template in `.env.example`

## AI Usage Summary

We did not use AI to generate the whole project. Most of the implementation and debugging work was still done manually. We mainly used AI when we were stuck on a few specific technical problems that were taking too long to resolve by trial and error.

The most useful cases were:

- troubleshooting Docker and Docker Swarm configuration details, especially around multi-service deployment structure and secrets-related setup
- debugging monitoring and observability integration, including health checks, metrics exposure, and Prometheus/Grafana configuration alignment
- checking edge cases in backend integration when connecting routes, templates, image uploads, and real-time updates
- refining parts of the final documentation structure so the README matched the course deliverable requirements more closely

One concrete example was deployment debugging: AI suggested configuration ideas for Docker and monitoring integration, but one of the suggested directions was not fully correct for the final setup. The team checked container logs, service behavior, and runtime tests, then adjusted the configuration manually to match the actual project requirements.

All final code, configuration, and documentation decisions were reviewed and adjusted by the team before being kept in the project.

Detailed interaction records will be added in `ai-session.md`.

## Individual Contributions

The project was completed collaboratively by all four team members. The list below reflects the final division of work after we rebalanced responsibilities so that each member owned a meaningful part of the system.

### Yinghao Wang

- Contributed deployment support scripts for the final project workflow.
- Added and maintained repository support files such as `.gitignore`.
- Assisted with deployment packaging through `deploy-stack.sh`.
- Supported the final repository structure used for project delivery.

### Nairui Tian

- Implemented and maintained `base.html`, the shared layout required by all forum pages.
- Built and refined the main homepage and user-facing forum presentation flow.
- Implemented the health check endpoint and metrics system for service observability.
- Improved deployment security by replacing hard-coded credentials with safer configuration paths.
- Completed anonymous reply support during final integration.
- Consolidated and finalized the project README according to the course deliverable requirements.

### Cunming Liu

- Took primary ownership of the database-integrated backend application layer.
- Implemented the database-backed post, reply, and like systems in Python.
- Contributed substantial backend route logic for the core discussion workflow.
- Supported Docker-related integration alongside the application backend.
- Will prepare and record the final demo video for submission.

### Ciliang Zhang

- Took primary responsibility for the Swarm deployment core in `docker-stack.yml`.
- Worked on CI/CD and automated testing support.
- Contributed backup-related operational scripts and deployment support.
- Helped validate the project through testing and deployment-oriented configuration.
- Will compile and submit the final AI interaction record.

## Lessons Learned

1. Building a cloud-native application is not only about writing features; deployment, persistence, monitoring, and operations take significant engineering effort.
2. Real-time features become much easier to justify when they are paired with a concrete user interaction model such as a discussion forum.
3. Secrets management and configuration hygiene matter more as soon as the project moves from a local demo to a replicated deployment.
4. Monitoring dashboards were useful not only for performance visibility, but also for debugging integration problems during development.
5. Persistent storage design must be considered early, especially when uploads and multi-replica behavior are involved.
6. Documentation can lag behind implementation very quickly, so it must be treated as part of the project instead of an afterthought.

## Screenshots

- Screenshot 1: TBD
- Screenshot 2: TBD
- Screenshot 3: TBD
- Screenshot 4: TBD
- Screenshot 5: TBD

## Video Demo

- Video demo link: https://youtu.be/LiqNHpgbzjs
