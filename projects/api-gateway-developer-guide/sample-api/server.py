"""Minimal, dependency-free example upstream API. Data is not persisted."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

ITEMS = [
    {"id": 1, "name": "Notebook", "category": "stationery"},
    {"id": 2, "name": "Marker", "category": "stationery"},
]


class InventoryHandler(BaseHTTPRequestHandler):
    def respond(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/health":
            self.respond(200, {"status": "ok"})
        elif path == "/items":
            self.respond(200, {"items": ITEMS, "count": len(ITEMS)})
        else:
            self.respond(404, {"error": "not_found", "message": "Path not found"})

    def do_POST(self):
        if urlsplit(self.path).path != "/items":
            return self.respond(404, {"error": "not_found", "message": "Path not found"})
        if self.headers.get_content_type() != "application/json":
            return self.respond(415, {"error": "unsupported_media_type", "message": "Use application/json"})
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size <= 0 or size > 65536:
                return self.respond(400, {"error": "invalid_request", "message": "Body must be 1-65536 bytes"})
            data = json.loads(self.rfile.read(size))
        except (ValueError, json.JSONDecodeError):
            return self.respond(400, {"error": "invalid_json", "message": "Body must contain valid JSON"})
        if not isinstance(data, dict) or not isinstance(data.get("name"), str) or not data["name"].strip():
            return self.respond(400, {"error": "invalid_name", "message": "name is required"})
        category = data.get("category", "uncategorized")
        if not isinstance(category, str):
            return self.respond(400, {"error": "invalid_category", "message": "category must be a string"})
        # Demonstration only: the new item is returned, not saved.
        self.respond(201, {"id": 3, "name": data["name"].strip(), "category": category})


def main():
    port = int(os.environ.get("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), InventoryHandler)
    print(f"Inventory API listening on {port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
