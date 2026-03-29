#!/usr/bin/env python3
"""
Auto-scaling monitor for Docker Swarm.
Queries Prometheus metrics and adjusts the number of app replicas accordingly.
"""

import os
import time
import logging
import subprocess

import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [AutoScaler] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
PROMETHEUS_URL = os.environ.get('PROMETHEUS_URL', 'http://prometheus:9090')
SERVICE_NAME = os.environ.get('SERVICE_NAME', 'forum_app')
MIN_REPLICAS = int(os.environ.get('MIN_REPLICAS', '2'))
MAX_REPLICAS = int(os.environ.get('MAX_REPLICAS', '10'))
CHECK_INTERVAL = int(os.environ.get('CHECK_INTERVAL', '30'))
COOLDOWN_SECONDS = int(os.environ.get('COOLDOWN_SECONDS', '120'))

# Thresholds
SCALE_UP_RPS_PER_REPLICA = float(os.environ.get('SCALE_UP_RPS', '50'))
SCALE_DOWN_RPS_PER_REPLICA = float(os.environ.get('SCALE_DOWN_RPS', '10'))
SCALE_UP_LATENCY_THRESHOLD = float(os.environ.get('SCALE_UP_LATENCY', '1.0'))

last_scale_time = 0


def query_prometheus(query):
    """Execute a PromQL query and return the numeric result."""
    try:
        resp = requests.get(
            f'{PROMETHEUS_URL}/api/v1/query',
            params={'query': query},
            timeout=10
        )
        resp.raise_for_status()
        result = resp.json()['data']['result']
        if result:
            return float(result[0]['value'][1])
    except Exception as e:
        logger.warning(f'Prometheus query failed: {e}')
    return None


def get_current_replicas():
    """Get the current number of replicas for the service."""
    try:
        output = subprocess.check_output(
            ['docker', 'service', 'inspect', SERVICE_NAME,
             '--format', '{{.Spec.Mode.Replicated.Replicas}}'],
            text=True, timeout=10
        )
        return int(output.strip())
    except Exception as e:
        logger.error(f'Failed to get current replicas: {e}')
        return None


def scale_service(replicas):
    """Scale the Docker Swarm service to the specified number of replicas."""
    try:
        subprocess.run(
            ['docker', 'service', 'scale', f'{SERVICE_NAME}={replicas}'],
            check=True, timeout=30
        )
        logger.info(f'Scaled {SERVICE_NAME} to {replicas} replicas')
        return True
    except Exception as e:
        logger.error(f'Failed to scale service: {e}')
        return False


def check_and_scale():
    """Main scaling logic: check metrics and scale up/down if needed."""
    global last_scale_time

    # Respect cooldown period
    if time.time() - last_scale_time < COOLDOWN_SECONDS:
        logger.debug('In cooldown period, skipping check')
        return

    current = get_current_replicas()
    if current is None:
        return

    # Query metrics
    request_rate = query_prometheus(
        'sum(rate(flask_request_total[2m]))'
    )
    avg_latency = query_prometheus(
        'histogram_quantile(0.95, sum(rate(flask_request_duration_seconds_bucket[2m])) by (le))'
    )

    logger.info(
        f'Metrics - replicas: {current}, '
        f'request_rate: {request_rate:.2f}/s, '
        f'p95_latency: {avg_latency:.3f}s'
        if request_rate is not None and avg_latency is not None
        else f'Metrics - replicas: {current}, some metrics unavailable'
    )

    # Scale up conditions
    should_scale_up = False
    if request_rate is not None and request_rate > SCALE_UP_RPS_PER_REPLICA * current:
        logger.info(f'Scale up trigger: high request rate ({request_rate:.1f} > {SCALE_UP_RPS_PER_REPLICA * current:.1f})')
        should_scale_up = True
    if avg_latency is not None and avg_latency > SCALE_UP_LATENCY_THRESHOLD:
        logger.info(f'Scale up trigger: high latency ({avg_latency:.3f}s > {SCALE_UP_LATENCY_THRESHOLD}s)')
        should_scale_up = True

    if should_scale_up and current < MAX_REPLICAS:
        new_count = min(current + 1, MAX_REPLICAS)
        if scale_service(new_count):
            last_scale_time = time.time()
        return

    # Scale down conditions
    if (request_rate is not None
            and request_rate < SCALE_DOWN_RPS_PER_REPLICA * current
            and current > MIN_REPLICAS):
        if avg_latency is None or avg_latency < SCALE_UP_LATENCY_THRESHOLD * 0.5:
            new_count = max(current - 1, MIN_REPLICAS)
            logger.info(f'Scale down: low utilization ({request_rate:.1f} < {SCALE_DOWN_RPS_PER_REPLICA * current:.1f})')
            if scale_service(new_count):
                last_scale_time = time.time()


def main():
    logger.info(f'Auto-scaler started for service: {SERVICE_NAME}')
    logger.info(f'Config: min={MIN_REPLICAS}, max={MAX_REPLICAS}, interval={CHECK_INTERVAL}s, cooldown={COOLDOWN_SECONDS}s')

    while True:
        try:
            check_and_scale()
        except Exception as e:
            logger.error(f'Unexpected error: {e}')
        time.sleep(CHECK_INTERVAL)


if __name__ == '__main__':
    main()
