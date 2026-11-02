# Quickstart: send your first request through an API gateway

**Goal:** Route a request through Kong Gateway to an upstream API and receive JSON.

**Time:** Approximately 10 minutes, assuming Docker images are already available.

## Prerequisites

- Docker Engine and Docker Compose v2
- `curl`
- Local ports `8000` and `8001` available

Run commands from the directory containing `docker-compose.yml`.

## 1. Start the local services

```bash
docker compose up -d --build
docker compose ps
```

This starts two containers: an Inventory API and Kong Gateway. The upstream API listens inside the Docker network; Kong's proxy is available at `localhost:8000`. The Admin API binds to localhost port `8001` for debugging only.

## 2. Confirm the gateway is available

```bash
curl -i http://localhost:8001/services
```

Expect HTTP `200` with a service named `inventory-upstream`. If the gateway is still starting, retry after a few seconds.

## 3. Request inventory data

```bash
curl -i http://localhost:8000/inventory/items \
  -H 'apikey: demo-local-only'
```

Expected HTTP `200 OK` with an `items` array and `count` field.

## 4. Create a sample item

```bash
curl -i -X POST http://localhost:8000/inventory/items \
  -H 'apikey: demo-local-only' \
  -H 'Content-Type: application/json' \
  -d '{"name":"Desk Lamp","category":"lighting"}'
```

Expected HTTP `201 Created`. The sample server does **not persist** created items.

## 5. Check authentication

```bash
curl -i http://localhost:8000/inventory/items
```

Expect HTTP `401 Unauthorized`: the API key is missing. Read [authentication](authentication.md) for why this happens.

## 6. Run the smoke checks

```bash
bash scripts/smoke-test.sh
```

Checks include authorized and unauthorized access, item creation and missing paths. See [verification](verification.md).

## 7. Stop the demo

```bash
docker compose down
```

## How routing works

The gateway matches the `/inventory` prefix, checks the `apikey` header, strips `/inventory`, and forwards the remaining path to the upstream API. For example, `/inventory/items` becomes `/items` inside the upstream service.

For the complete contract, see the [API reference](api-reference.md). If a request fails, go to [troubleshooting](troubleshooting.md).
