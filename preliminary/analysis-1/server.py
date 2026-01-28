#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import datetime
import os

class LoggingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        timestamp = datetime.datetime.now().isoformat()

        log_line = f"[{timestamp}] Connection from: {client_ip}"
        print(log_line, flush=True)

        response = f"""<!DOCTYPE html>
<html>
<head>
<title>IP Logging Demo</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }}
code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }}
.ip {{ font-size: 2em; color: #d63031; }}
</style>
</head>
<body>
<h1>What IP does the server see?</h1>
<p class="ip"><code>{client_ip}</code></p>
<hr>
<p><strong>Is that your real IP?</strong></p>
<p>If this is behind Docker bridge NAT or a load balancer without proper config,
multiple different visitors will all appear as the same internal IP.</p>
<p>Check the server logs - everyone shows up as the same address.</p>
</body>
</html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(response.encode())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), LoggingHandler)
    print(f"Server starting on port {port}...", flush=True)
    server.serve_forever()
