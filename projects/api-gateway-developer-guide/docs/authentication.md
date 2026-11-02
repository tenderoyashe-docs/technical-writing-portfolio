# Authentication: API keys

The demo uses Kong Gateway's **Key Authentication** plugin to identify callers before requests reach the Inventory API.

## Use the demo key

\`\`\`bash
curl -i http://localhost:8000/inventory/items \
  -H 'apikey: demo-local-only'
\`\`\`

The key belongs to the \`developer-demo\` Consumer defined in \`gateway/kong.yml\`.

| Situation | Expected HTTP status | Next action |
| --- | --- | --- |
| Valid key | 200 | Continue |
| Missing \`apikey\` header | 401 | Add the header |
| Unknown or mistyped key | 401 | Check the exact value |
| Valid key, unknown upstream path | 404 | Check the path |

The plugin uses the request header, not an OAuth bearer token. The demo explicitly disables API-key lookup in query parameters and request bodies, and hides the credential before proxying upstream.

## Security note

\`demo-local-only\` is intentionally not secret: it is sample data committed for a local demonstration. Do not reuse it as a real credential. Production systems should use generated credentials, secrets management, TLS and appropriate rotation policies.

Read the [official Key Auth documentation](https://developer.konghq.com/plugins/key-auth/) for production considerations.
