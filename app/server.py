"""A tiny HTTP service for practicing support and incident-response workflows.

Start with `python3 -m app.server`; DEMO_FAIL_MODE=1 makes health checks fail.
"""
import json
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

START = time.monotonic()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/healthz':
            failing = os.getenv('DEMO_FAIL_MODE', '0') == '1'
            self.respond(503 if failing else 200, {"status": "down" if failing else "ok", "component": "sample-web-service"})
        elif self.path == '/':
            self.respond(200, {"service": "sample-web-service", "uptime_seconds": round(time.monotonic() - START, 1)})
        else:
            self.respond(404, {"error": "not_found"})

    def respond(self, status, payload):
        data = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        # Include a timestamp and HTTP status in container logs.
        print(json.dumps({"event": "http_request", "time": time.time(), "message": format % args}), flush=True)


def run(host='0.0.0.0', port=8080):
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f'Sample service listening on {host}:{port}', flush=True)
    httpd.serve_forever()

if __name__ == '__main__':
    run(host=os.getenv('HOST', '0.0.0.0'), port=int(os.getenv('PORT', '8080')))
