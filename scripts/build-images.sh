#!/usr/bin/env bash

set -e

echo "Building FastAPI image..."
podman build \
    -t localhost/nlab-api:0.1.0 \
    -f app/backend/Dockerfile \
    app/backend

echo "Building Nginx image..."
podman build \
    -t localhost/nlab-nginx:0.1.0 \
    -f infra/nginx/Dockerfile \
    .

echo "Both images built successfully."
