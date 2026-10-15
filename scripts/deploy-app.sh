#!/usr/bin/env bash

set -e

echo "Removing existing application containers..."
podman rm -f nlab-api nlab-nginx 2>/dev/null || true

echo "Starting FastAPI..."
podman run -d \
    --name nlab-api \
    --pod nlab-app \
    --env-file .env \
    -e TEMPLATE_DIR=/data/network/templates \
    -v "$PWD/data/network/templates:/data/network/templates:ro" \
    localhost/nlab-api:0.1.0

echo "Starting Nginx..."
podman run -d \
    --name nlab-nginx \
    --pod nlab-app \
    localhost/nlab-nginx:0.1.0

echo "Application deployment completed."
