#!/bin/bash
# Initialize Docker Swarm and create secrets for production deployment

set -e

echo "=== Initializing Docker Swarm ==="

# Check if already in swarm mode
if docker info --format '{{.Swarm.LocalNodeState}}' 2>/dev/null | grep -q "active"; then
    echo "Swarm is already active."
else
    docker swarm init
    echo "Swarm initialized."
fi

echo ""
echo "=== Creating Docker Secrets ==="

# Create secret_key (Flask session encryption key)
if docker secret inspect secret_key >/dev/null 2>&1; then
    echo "Secret 'secret_key' already exists, skipping."
else
    openssl rand -hex 32 | docker secret create secret_key -
    echo "Created secret: secret_key"
fi

# Create db_password (PostgreSQL password)
if docker secret inspect db_password >/dev/null 2>&1; then
    echo "Secret 'db_password' already exists, skipping."
else
    openssl rand -hex 16 | docker secret create db_password -
    echo "Created secret: db_password"
fi

echo ""
echo "=== Building Docker Image ==="
docker build -t forum-app:latest .

echo ""
echo "=== Swarm Setup Complete ==="
echo "Run './scripts/deploy-stack.sh' to deploy the application."
echo ""
docker secret ls
