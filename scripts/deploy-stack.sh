#!/bin/bash
# Deploy the forum application stack to Docker Swarm

set -e

echo "=== Building Docker Image ==="
docker build -t forum-app:latest .

echo ""
echo "=== Deploying Stack ==="
docker stack deploy -c docker-stack.yml forum

echo ""
echo "=== Stack Deployed ==="
echo "Waiting for services to start..."
sleep 5

docker stack services forum

echo ""
echo "Application: http://localhost:5000"
echo "Prometheus:   http://localhost:9090"
echo "Grafana:      http://localhost:3000 (admin/admin)"
