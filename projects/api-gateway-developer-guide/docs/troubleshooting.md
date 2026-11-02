# Troubleshooting API gateway requests

Use this guide after following the [quickstart](quickstart.md).

## 401 Unauthorized

**Symptom:** \`GET /inventory/items\` returns 401.

**Likely cause:** Missing, mistyped or unknown API key.

1. Confirm you sent the \`apikey\` header.
2. Check the local key is exactly \`demo-local-only\`.
3. Retry:

   \`\`\`bash
   curl -i http://localhost:8000/inventory/items -H 'apikey: demo-local-only'
   \`\`\`

**Do not** attempt to fix a 401 by changing the upstream Python app: authentication is enforced at the gateway.

## 404 Not Found

**Symptom:** An endpoint returns 404.

1. Check the exact proxy path: \`/inventory/items\`.
2. If Kong returns \`no Route matched\`, check \`gateway/kong.yml\` for the route prefix.
3. If the response contains \`"error":"not_found"\`, the request reached the upstream API but the upstream path does not exist.

The route uses \`strip_path: true\`, so \`/inventory/items\` maps to upstream \`/items\`.

## 502 Bad Gateway or 503 Service Unavailable

**Symptom:** Kong cannot proxy to the Inventory API.

1. Check both containers: \`docker compose ps\`.
2. Review upstream logs: \`docker compose logs inventory-api\`.
3. Review gateway logs: \`docker compose logs gateway\`.
4. Verify the upstream service URL is \`http://inventory-api:8080\` and both services use the same Compose network.
5. Retry once containers are healthy.

The exact 5xx status can vary with the failure mode.

## Connection refused on localhost:8000

The gateway might not be running or another process might own the port.

\`\`\`bash
docker compose ps
docker compose logs gateway
\`\`\`

Check port binding conflicts and restart if needed.

## 400 Invalid request

For \`POST /inventory/items\`, check that the request body is valid JSON with a non-empty string \`name\`, and that the \`Content-Type\` header is \`application/json\`.

## When to escalate

Capture the command with secrets redacted, timestamp, HTTP status, sanitized response, affected path, and relevant container logs. **Never copy production API keys into a support ticket.**

## Preventing repeat issues

If an error recurs, update the relevant guide with a reproducible example, note the affected version, and add a smoke test where feasible.
