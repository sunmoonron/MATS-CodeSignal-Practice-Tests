from __future__ import annotations
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import json
import threading

class ItemsApp:
    """
    Implement a tiny JSON API using http.server.

    Endpoints:
      Level 1:
        GET /health -> 200 {"status":"ok"}

      Level 2:
        POST /items JSON {"name":str, "qty":int} -> 201 {"id":int}
        GET /items/<id> -> 200 item JSON or 404 {"error":"not_found"}

      Level 3:
        GET /items -> 200 {"items":[...]} sorted by id asc
        GET /items?min_qty=2 filters items with qty >= min_qty

      Level 4:
        Invalid JSON on POST -> 400 {"error":"invalid_json"}
        Unknown route -> 404 {"error":"not_found"}
        DELETE /items/<id> -> 204 if deleted else 404 {"error":"not_found"}
    """
    def __init__(self):
        raise NotImplementedError

    def handle(self, method: str, path: str, query: dict[str, list[str]], body_bytes: bytes | None):
        """
        Return (status:int, headers:dict[str,str], response_obj:any or None).
        If response_obj is None, handler may send no body.
        """
        raise NotImplementedError


def make_handler(app: ItemsApp):
    class Handler(BaseHTTPRequestHandler):
        def _read_body(self) -> bytes:
            n = int(self.headers.get("Content-Length", "0") or "0")
            return self.rfile.read(n) if n > 0 else b""

        def _send_json(self, status: int, obj, headers: dict[str, str] | None = None):
            body = b""
            if obj is not None:
                body = json.dumps(obj).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            if headers:
                for k, v in headers.items():
                    self.send_header(k, v)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if body:
                self.wfile.write(body)

        def _dispatch(self, method: str):
            parsed = urlparse(self.path)
            path = parsed.path
            query = parse_qs(parsed.query)
            body = self._read_body() if method in ("POST", "PUT", "PATCH") else None
            status, headers, obj = app.handle(method, path, query, body)
            self._send_json(status, obj, headers)

        def do_GET(self):
            self._dispatch("GET")

        def do_POST(self):
            self._dispatch("POST")

        def do_DELETE(self):
            self._dispatch("DELETE")

        def log_message(self, fmt, *args):
            # silence test output
            return

    return Handler


def start_server(app: ItemsApp, host: str = "127.0.0.1", port: int = 0):
    """
    Returns (server, thread, base_url).
    Binds to port=0 by default (ephemeral free port).
    """
    server = ThreadingHTTPServer((host, port), make_handler(app))
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    host2, port2 = server.server_address
    base_url = f"http://{host2}:{port2}"
    return server, t, base_url


def stop_server(server):
    server.shutdown()
    server.server_close()
