# AI Interaction Record

This file documents three representative AI interactions that meaningfully influenced the project, as required by the
course handout. In all cases, the AI was used as an assistant for drafting, planning, or review, and all final
decisions and verification were performed by the team.

## Session 1: Debugging Docker Swarm deployment and configuration

### Prompt

```text
Please review our Docker Swarm deployment plan for a Flask-based cloud-native forum that uses PostgreSQL, Redis,
Prometheus, Grafana, a backup service, and an auto-scaling script. We want to keep the current architecture, but we
need help checking whether the stack configuration is reasonable for service replication, secrets usage, health checks,
and monitoring integration.
```

### AI Response

```text
The response suggested checking several parts of the Swarm configuration more carefully, including secret handling for
production-only credentials, health checks for the application service, placement rules for stateful services, and the
relationship between the app service and monitoring components. It also suggested tightening the deployment structure
so that PostgreSQL and Redis remained stateful services while the Flask app stayed replicated.
```

### What Your Team Did With It

The response was useful because it helped us review the deployment structure at a high level and identify which parts
of the Swarm configuration needed closer attention, especially around secrets, health checks, and service roles.

However, not every suggestion was suitable for our final setup. One suggested direction did not fully match the way our
project handled runtime configuration and service integration, so we did not apply it directly.

We verified the final configuration manually by checking the actual `docker-stack.yml`, container logs, service
behavior, secret usage, and deployment results before keeping any changes.

## Session 2: Reviewing monitoring and observability setup

### Prompt

```text
Help us review the monitoring and observability part of our project. We are using Prometheus, Grafana, a health
endpoint, and application metrics, and we want to make sure the implementation and the report description are aligned.
Please point out anything unclear or inconsistent in how we describe metrics, dashboards, alerts, and monitoring
links.
```

### AI Response

```text
The response highlighted the need to explain the monitoring stack more clearly, especially the relationship between
the application metrics endpoint, Prometheus scraping, Grafana dashboards, and the public monitoring links. It also
recommended making the README wording more explicit so the monitoring flow could be understood without reading the
source code first.
```

### What Your Team Did With It

This interaction was useful because it helped us improve the clarity of the monitoring-related explanation in the final
documentation and made us double-check that the described observability flow actually matched the deployed system.

Some suggestions were still too generic and did not automatically fit our exact implementation, so we only kept the
parts that matched the real Prometheus, Grafana, and health-check setup in the repository.

We verified the final wording and configuration by comparing the AI suggestions against the actual monitoring files,
application endpoints, and the deployed service behavior before updating the README.

## Session 3: Refining the README and final submission materials

### Prompt

```text
Please review our README for the final course project submission. We want help improving wording, organizing the user
guide and screenshots, checking consistency between the documented features and the repository contents, and making
sure the final report sections are clear and well structured.
```

### AI Response

```text
The response suggested improving the structure of the final README, tightening the wording of the user guide, placing
screenshots closer to the relevant usage steps, and making sure project features, deployment notes, and individual
contributions were described consistently. It also suggested keeping the high-level AI summary in the README while
placing the detailed interaction record in a separate `ai-session.md` file.
```

### What Your Team Did With It

This interaction was useful because it helped us organize the final report more clearly and catch places where the
README wording did not fully match the repository contents or the intended submission structure.

Not all wording suggestions were kept. Some recommendations were too general, and some structural suggestions did not
match how we ultimately wanted to present the user guide and supporting screenshots.

We checked the repository files, screenshots, feature implementation, and final course requirements manually before
keeping any documentation changes.
