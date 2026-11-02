# API Gateway Developer Guide

**An independent, hands-on technical documentation project.**

This sample documents a small Inventory API accessed through Kong Gateway. It includes an executable local demo, a developer quickstart, an OpenAPI contract, authentication guidance, troubleshooting, and a verification checklist.

**Audience:** Developers integrating with an API gateway, technical support engineers, and documentation reviewers.

## Start here

1. [Run the gateway and make your first request](docs/quickstart.md)
2. [Explore the API reference](docs/api-reference.md)
3. [Understand API key authentication](docs/authentication.md)
4. [Troubleshoot common errors](docs/troubleshooting.md)
5. [Review the testing and verification plan](docs/verification.md)
6. [Read the documentation strategy and decisions](docs/documentation-strategy.md)

### Architecture

```text
Developer (curl)
      |
      | GET /inventory/items + apikey header
      v
Kong Gateway (localhost:8000)
      |  matches route, validates API key,
      |  strips /inventory prefix
      v
Inventory API (internal container:8080)
      |
      v
JSON response
```

The sample upstream API uses Python's standard library. The gateway is configured declaratively in DB-less mode, so it does not require an external database.

## Quick demo

Prerequisites: Docker Engine with Docker Compose and `curl`.

```bash
docker compose up -d --build
curl -i http://localhost:8000/inventory/items -H 'apikey: demo-local-only'
bash scripts/smoke-test.sh
docker compose down
```

The demo API key is intentionally public and valid **only for this local example**. Do not use it in production or expose the admin interface beyond localhost.

## What's in this project?

| Location | Purpose |
| --- | --- |
| `docs/` | Task-oriented guides, reference, troubleshooting, verification |
| `openapi.yaml` | API contract for requests, responses, and errors |
| `gateway/kong.yml` | Declarative Kong Gateway routing and API key policy |
| `sample-api/` | Minimal working upstream API (Python) |
| `scripts/smoke-test.sh` | End-to-end expected-status checks through Kong |
| `tests/test_server.py` | Local unit tests for the upstream API |
| `CHANGELOG.md` | Project maintenance notes |

## Validation status

- The Python upstream can be tested without Docker using `python -m unittest discover -s tests -v`.
- The complete gateway setup requires Docker Compose; follow the [verification guide](docs/verification.md) and record results before describing the gateway integration as tested.
- All response examples are illustrative until confirmed against a running environment.

## About the work

This is a **personal portfolio demonstration**, not an official Kong guide or documentation produced for Kong Inc. It was created to practice developer-oriented documentation and documentation-as-code workflows.

Author: Tenderoyashe Zhou

Official background reading: [Kong Gateway documentation](https://developer.konghq.com/gateway/) · [DB-less mode](https://developer.konghq.com/gateway/db-less-mode/) · [Key Auth](https://developer.konghq.com/plugins/key-auth/)
