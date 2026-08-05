"""
Ghost Strategies — Local Development Server with FRED/BLS CORS Proxy
Run this instead of 'python -m http.server' to get live API data locally.

Usage:
    python server.py

Then open http://localhost:8080 in your browser.
The dashboard calls /api/fred/... and /api/bls/... which this server proxies
to the real APIs, adding proper CORS headers to the response.
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.request
import urllib.error
import json
import sys
import os

PORT = 8080

class ProxyHandler(SimpleHTTPRequestHandler):
    """Serves static files AND proxies API requests to FRED/BLS."""

    def do_GET(self):
        # ── FRED Proxy: /api/fred?series_id=X&api_key=Y&... ──
        if self.path.startswith('/api/fred?') or self.path.startswith('/api/fred/?'):
            query = self.path.split('?', 1)[1] if '?' in self.path else ''
            url = f'https://api.stlouisfed.org/fred/series/observations?{query}'
            self._proxy_get(url)

        # ── BEA Proxy: /api/bea?UserID=X&... ──
        elif self.path.startswith('/api/bea?') or self.path.startswith('/api/bea/?'):
            query = self.path.split('?', 1)[1] if '?' in self.path else ''
            url = f'https://apps.bea.gov/api/data?{query}'
            self._proxy_get(url)

        # ── Stooq Proxy (daily price CSV): /api/stooq?s=smh.us&i=d&d1=...&d2=... ──
        elif self.path.startswith('/api/stooq?') or self.path.startswith('/api/stooq/?'):
            query = self.path.split('?', 1)[1] if '?' in self.path else ''
            url = f'https://stooq.com/q/d/l/?{query}'
            self._proxy_get(url, content_type='text/csv')

        # ── Static files (index.html, etc.) ──
        else:
            super().do_GET()

    def do_POST(self):
        # ── BLS Proxy: POST /api/bls ──
        if self.path == '/api/bls' or self.path == '/api/bls/':
            content_len = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_len)
            url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
            self._proxy_post(url, body)
        else:
            self.send_error(404)

    def _proxy_get(self, url, content_type='application/json'):
        """Forward a GET request and return the response with CORS headers."""
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'GhostStrategies-Terminal/1.0')
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def _proxy_post(self, url, body):
        """Forward a POST request and return the response with CORS headers."""
        try:
            req = urllib.request.Request(url, data=body, method='POST')
            req.add_header('Content-Type', 'application/json')
            req.add_header('User-Agent', 'GhostStrategies-Terminal/1.0')
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        """Custom log format."""
        if '/api/' in (args[0] if args else ''):
            sys.stderr.write(f"  [PROXY] {args[0]}\n")
        else:
            # Suppress static file logs for cleanliness
            pass


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  GHOST STRATEGIES — Local Development Server                ║
║                                                              ║
║  Dashboard:  http://localhost:{PORT}                          ║
║  FRED Proxy: http://localhost:{PORT}/api/fred?...             ║
║  BEA Proxy:  http://localhost:{PORT}/api/bea?...              ║
║  BLS Proxy:  http://localhost:{PORT}/api/bls  (POST)          ║
║                                                              ║
║  Press Ctrl+C to stop                                        ║
╚══════════════════════════════════════════════════════════════╝
""")

    server = HTTPServer(('', PORT), ProxyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
