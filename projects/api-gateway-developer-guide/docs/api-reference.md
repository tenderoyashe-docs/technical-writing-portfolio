# Inventory API reference

**Base URL (via gateway):** `http://localhost:8000`

All documented endpoints require the header `apikey: demo-local-only`.

See [OpenAPI specification](../openapi.yaml) for the machine-readable contract.

## GET /inventory/health

Returns a simple readiness response from the upstream service.

```bash
curl -i http://localhost:8000/inventory/health -H 'apikey: demo-local-only'
```

HTTP `200`:

```json
{"status":"ok"}
```

## GET /inventory/items

Lists the static items loaded by the sample server.

```bash
curl -i http://localhost:8000/inventory/items -H 'apikey: demo-local-only'
```

HTTP `200`:

```json
{
  "items": [
    {"id": 1, "name": "Notebook", "category": "stationery"},
    {"id": 2, "name": "Marker", "category": "stationery"}
  ],
  "count": 2
}
```

## POST /inventory/items

Validates the JSON payload and returns a sample created item. **The item is not persisted.**

```bash
curl -i -X POST http://localhost:8000/inventory/items \
  -H 'apikey: demo-local-only' \
  -H 'Content-Type: application/json' \
  -d '{"name":"Desk Lamp","category":"lighting"}'
```

HTTP `201`:

```json
{"id":3,"name":"Desk Lamp","category":"lighting"}
```

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | Yes | Non-empty item name |
| `category` | string | No | Defaults to `uncategorized` |

## Errors

| Status | Source | Typical cause |
| --- | --- | --- |
| 400 | Upstream | Invalid JSON, missing name, invalid category, or invalid body size |
| 401 | Gateway | Missing or unrecognized API key |
| 404 | Gateway or upstream | Unmatched route or missing API path |
| 415 | Upstream | POST request without `application/json` |
| 502/503 | Gateway | Upstream unavailable or unhealthy (depends on failure mode) |

Upstream errors use `{"error":"code","message":"description"}`. Gateway errors follow Kong's own response format, which may differ.

## Related guides

- [Quickstart](quickstart.md)
- [Authentication](authentication.md)
- [Troubleshooting](troubleshooting.md)
