#!/usr/bin/env bash
set -euo pipefail
BASE_URL="\${BASE_URL:-http://localhost:8000}"
KEY="demo-local-only"

assert_status() {
  local expected="$1" method="$2" path="$3"
  shift 3
  local actual
  actual=$(curl -sS -o /dev/null -w '%{http_code}' -X "$method" "$BASE_URL$path" "$@")
  if [[ "$actual" != "$expected" ]]; then
    echo "FAIL $method $path: expected $expected, received $actual" >&2
    exit 1
  fi
  echo "PASS $method $path -> $actual"
}

assert_status 200 GET /inventory/health -H "apikey: $KEY"
assert_status 200 GET /inventory/items -H "apikey: $KEY"
assert_status 401 GET /inventory/items
assert_status 401 GET /inventory/items -H "apikey: incorrect"
assert_status 201 POST /inventory/items -H "apikey: $KEY" -H "Content-Type: application/json" -d '{"name":"Desk Lamp"}'
assert_status 400 POST /inventory/items -H "apikey: $KEY" -H "Content-Type: application/json" -d '{"category":"lighting"}'
assert_status 404 GET /inventory/does-not-exist -H "apikey: $KEY"

echo "Gateway smoke tests passed."
