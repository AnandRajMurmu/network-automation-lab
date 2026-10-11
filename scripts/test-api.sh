#!/usr/bin/env bash

set -e

BASE_URL="http://127.0.0.1:8080"

echo "Testing API health..."
curl --fail --silent --show-error "$BASE_URL/api/health"
echo

echo "Testing API root..."
curl --fail --silent --show-error "$BASE_URL/api/"
echo

echo "Testing OpenAPI schema..."
curl --fail --silent --show-error \
    "$BASE_URL/api/openapi.json" \
    -o /dev/null

echo "All API smoke tests passed."
