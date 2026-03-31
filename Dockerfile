FROM python:3.12-slim AS base

WORKDIR /app

# Install system dependencies for psycopg2 and curl (healthcheck)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS production

COPY . .

EXPOSE 5000

# SocketIO requires eventlet worker class and exactly 1 worker per container.
# Horizontal scaling is achieved via multiple containers (Swarm replicas).
CMD ["gunicorn", \
     "--worker-class", "eventlet", \
     "-w", "1", \
     "--bind", "0.0.0.0:5000", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "wsgi:app"]
