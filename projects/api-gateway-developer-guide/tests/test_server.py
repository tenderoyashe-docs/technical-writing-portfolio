"""Tests the upstream API only (not Kong Gateway)."""
import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "sample-api"))
from server import InventoryHandler  # noqa: E402


class UpstreamTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), InventoryHandler)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request(self, path, method="GET", body=None, headers=None):
        url = f"http://127.0.0.1:{self.port}{path}"
        data = json.dumps(body).encode() if body is not None else None
        req = Request(url, data=data, headers=headers or {}, method=method)
        try:
            with urlopen(req) as res:
                return res.status, json.load(res)
        except HTTPError as exc:
            return exc.code, json.load(exc)

    def test_health(self):
        code, payload = self.request("/health")
        self.assertEqual((code, payload["status"]), (200, "ok"))

    def test_list_items(self):
        code, payload = self.request("/items")
        self.assertEqual(code, 200)
        self.assertEqual(payload["count"], 2)

    def test_create_item(self):
        code, payload = self.request(
            "/items", "POST", {"name": "Desk Lamp", "category": "lighting"},
            {"Content-Type": "application/json"}
        )
        self.assertEqual(code, 201)
        self.assertEqual(payload["name"], "Desk Lamp")

    def test_missing_name(self):
        code, payload = self.request(
            "/items", "POST", {"category": "lighting"},
            {"Content-Type": "application/json"}
        )
        self.assertEqual(code, 400)
        self.assertEqual(payload["error"], "invalid_name")

    def test_unknown_route(self):
        code, payload = self.request("/missing")
        self.assertEqual(code, 404)
        self.assertEqual(payload["error"], "not_found")


if __name__ == "__main__":
    unittest.main()
