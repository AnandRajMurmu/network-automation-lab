#!/usr/bin/env bash

set -euo pipefail

BASE_URL="http://127.0.0.1:8080"
DEVICE_ID=""

cleanup() {
    if [[ -n "$DEVICE_ID" ]]; then
        curl --silent --show-error \
            -X DELETE "$BASE_URL/api/devices/$DEVICE_ID" \
            -o /dev/null || true
    fi
}

trap cleanup EXIT

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
echo "OpenAPI schema passed."

echo "Testing database connection..."
curl --fail --silent --show-error "$BASE_URL/api/db-health"
echo

echo "Testing device inventory..."
curl --fail --silent --show-error "$BASE_URL/api/devices"
echo

echo "Testing single-device lookup..."
curl --fail --silent --show-error "$BASE_URL/api/devices/1"
echo

echo "Testing device creation..."
CREATE_RESPONSE=$(curl --fail --silent --show-error \
    -X POST "$BASE_URL/api/devices" \
    -H "Content-Type: application/json" \
    -d '{
        "hostname": "TEST-CRUD",
        "management_ip": "192.168.30.99",
        "device_type": "switch",
        "location": "Smoke Test"
    }')

echo "$CREATE_RESPONSE"

DEVICE_ID=$(printf '%s' "$CREATE_RESPONSE" |
    python -c 'import json, sys; print(json.load(sys.stdin)["id"])')

echo "Created test device ID: $DEVICE_ID"

echo "Testing device update..."
UPDATE_RESPONSE=$(curl --fail --silent --show-error \
    -X PUT "$BASE_URL/api/devices/$DEVICE_ID" \
    -H "Content-Type: application/json" \
    -d '{
        "hostname": "TEST-CRUD",
        "management_ip": "192.168.30.99",
        "device_type": "switch",
        "location": "Smoke Test Updated",
        "status": "active"
    }')

echo "$UPDATE_RESPONSE"

if ! printf '%s' "$UPDATE_RESPONSE" |
    grep -q '"location":"Smoke Test Updated"'; then
    echo "ERROR: Device update verification failed."
    exit 1
fi

echo "Device update passed."

echo "Testing device deletion..."
DELETE_RESPONSE=$(curl --fail --silent --show-error \
    -X DELETE "$BASE_URL/api/devices/$DEVICE_ID")

echo "$DELETE_RESPONSE"
DEVICE_ID=""

echo "Testing deleted-device response..."
STATUS_CODE=$(curl --silent --show-error \
    -o /dev/null \
    -w '%{http_code}' \
    "$BASE_URL/api/devices/999999")

if [[ "$STATUS_CODE" != "404" ]]; then
    echo "ERROR: Expected HTTP 404, received $STATUS_CODE."
    exit 1
fi

echo "Missing-device response passed."

echo "All API smoke tests passed."
