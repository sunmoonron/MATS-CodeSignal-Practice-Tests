import unittest
import json
import http.client
from urllib.parse import urlparse

from simple_http_server import ItemsApp, start_server, stop_server

def http_request(base_url, method, path, body_obj=None, headers=None):
    headers = dict(headers or {})
    parsed = urlparse(base_url)
    conn = http.client.HTTPConnection(parsed.hostname, parsed.port, timeout=2)

    body = None
    if body_obj is not None:
        body = json.dumps(body_obj).encode("utf-8")
        headers.setdefault("Content-Type", "application/json")
        headers["Content-Length"] = str(len(body))

    conn.request(method, path, body=body, headers=headers)
    resp = conn.getresponse()
    raw = resp.read().decode("utf-8")
    conn.close()

    obj = None
    if raw:
        obj = json.loads(raw)
    return resp.status, dict(resp.getheaders()), obj

class TestHTTPServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = ItemsApp()
        cls.server, cls.thread, cls.base = start_server(cls.app)

    @classmethod
    def tearDownClass(cls):
        stop_server(cls.server)

    def test_level1_health(self):
        status, headers, obj = http_request(self.base, "GET", "/health")
        self.assertEqual(status, 200)
        self.assertEqual(obj, {"status": "ok"})

    def test_level2_create_and_get(self):
        status, headers, obj = http_request(self.base, "POST", "/items", {"name": "apple", "qty": 2})
        self.assertEqual(status, 201)
        self.assertIn("id", obj)
        item_id = obj["id"]

        status, headers, obj = http_request(self.base, "GET", f"/items/{item_id}")
        self.assertEqual(status, 200)
        self.assertEqual(obj["name"], "apple")
        self.assertEqual(obj["qty"], 2)

        status, headers, obj = http_request(self.base, "GET", "/items/999999")
        self.assertEqual(status, 404)
        self.assertEqual(obj["error"], "not_found")

    def test_level3_list_and_filter(self):
        # create more items
        http_request(self.base, "POST", "/items", {"name": "banana", "qty": 1})
        http_request(self.base, "POST", "/items", {"name": "carrot", "qty": 5})

        status, headers, obj = http_request(self.base, "GET", "/items")
        self.assertEqual(status, 200)
        self.assertIn("items", obj)
        ids = [it["id"] for it in obj["items"]]
        self.assertEqual(ids, sorted(ids))

        status, headers, obj = http_request(self.base, "GET", "/items?min_qty=2")
        self.assertEqual(status, 200)
        self.assertTrue(all(it["qty"] >= 2 for it in obj["items"]))

    def test_level4_invalid_json_and_delete(self):
        # invalid json: send bytes not JSON
        parsed = urlparse(self.base)
        conn = http.client.HTTPConnection(parsed.hostname, parsed.port, timeout=2)
        conn.request("POST", "/items", body=b"{not json", headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        raw = resp.read().decode("utf-8")
        conn.close()
        self.assertEqual(resp.status, 400)
        self.assertEqual(json.loads(raw), {"error": "invalid_json"})

        # create and delete
        status, headers, obj = http_request(self.base, "POST", "/items", {"name": "to-delete", "qty": 0})
        item_id = obj["id"]
        status, headers, obj = http_request(self.base, "DELETE", f"/items/{item_id}")
        self.assertEqual(status, 204)
        self.assertEqual(obj, None)

        status, headers, obj = http_request(self.base, "DELETE", f"/items/{item_id}")
        self.assertEqual(status, 404)
        self.assertEqual(obj["error"], "not_found")

        status, headers, obj = http_request(self.base, "GET", "/nope")
        self.assertEqual(status, 404)
        self.assertEqual(obj["error"], "not_found")

if __name__ == "__main__":
    unittest.main()
