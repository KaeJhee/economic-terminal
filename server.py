"""
Ghost Strategies — Local Development Server with FRED/BLS CORS Proxy
Run this instead of 'python -m http.server' to get live API data locally.

Usage:
    python server.py

Then open http://127.0.0.1:8080 in your browser.
The dashboard calls /api/fred, /api/bea, /api/stooq, and POST /api/bls, which
this server proxies. It binds to 127.0.0.1 only and does not serve .git or
the private spec files.
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.request
import urllib.error
import urllib.parse
import json
import sys
import os

PORT = 8080
BIND = '127.0.0.1'
ALLOWED_ORIGINS = {'http://localhost:8080', 'http://127.0.0.1:8080'}
PRIVATE_FILES = {
    'economic-terminal-kickoff-prompt.md',
    'news-analysis-tab-build-spec.md',
    'model-bench-terminal-build-spec.md',
    'portfolio.md',
}


class ProxyHandler(SimpleHTTPRequestHandler):
    """Serves static files AND proxies API requests to FRED/BLS."""

    def _is_private_path(self):
        raw = urllib.parse.unquote(self.path.split('?', 1)[0]).replace('\\', '/')
        parts = [p for p in raw.split('/') if p and p not in ('.', '..')]
        if self._name_blocked(parts):
            return True
        translated = os.path.realpath(self.translate_path(self.path))
        root = os.path.realpath(os.getcwd())
        if translated != root and not translated.startswith(root + os.sep):
            return True
        rel = os.path.relpath(translated, root)
        return self._name_blocked(rel.split(os.sep))

    @staticmethod
    def _name_blocked(parts):
        if any(p == '.git' or p.startswith('.git') for p in parts):
            return True
        name = parts[-1].lower() if parts else ''
        if name in PRIVATE_FILES:
            return True
        if name.endswith('.md') and 'build-spec' in name:
            return True
        return False

    def _cors_headers(self):
        origin = self.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            self.send_header('Access-Control-Allow-Origin', origin)
            self.send_header('Vary', 'Origin')

    def do_GET(self):
        if self.path.startswith('/api/fred?') or self.path.startswith('/api/fred/?'):
            query = self.path.split('?', 1)[1] if '?' in self.path else ''
            url = f'https://api.stlouisfed.org/fred/series/observations?{query}'
            self._proxy_get(url)
        elif self.path.startswith('/api/bea?') or self.path.startswith('/api/bea/?'):
            query = self.path.split('?', 1)[1] if '?' in self.path else ''
            url = f'https://apps.bea.gov/api/data?{query}'
            self._proxy_get(url)
        elif self.path.startswith('/api/stooq?') or self.path.startswith('/api/stooq/?'):
            query = self.path.split('?', 1)[1] if '?' in self.path else ''
            url = f'https://stooq.com/q/d/l/?{query}'
            self._proxy_get(url, content_type='text/csv')
        elif self._is_private_path():
            self.send_error(404, 'Not found')
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/bls' or self.path == '/api/bls/':
            content_len = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_len)
            url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
            self._proxy_post(url, body)
        else:
            self.send_error(404)

    def _proxy_get(self, url, content_type='application/json'):
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'GhostStrategies-Terminal/1.0')
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Cache-Control', 'private, no-store')
                self._cors_headers()
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'private, no-store')
            self._cors_headers()
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self._cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def _proxy_post(self, url, body):
        try:
            req = urllib.request.Request(url, data=body, method='POST')
            req.add_header('Content-Type', 'application/json')
            req.add_header('User-Agent', 'GhostStrategies-Terminal/1.0')
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Cache-Control', 'private, no-store')
                self._cors_headers()
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'private, no-store')
            self._cors_headers()
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self._cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self._cors_headers()
        self.end_headers()

    def log_message(self, format, *args):
        try:
            message = format % args
        except Exception:
            message = ' '.join(str(a) for a in args)
        if '/api/' in message:
            sys.stderr.write(f"  [PROXY] {message}\n")


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  GHOST STRATEGIES — Local Development Server                ║
║                                                              ║
║  Dashboard:  http://127.0.0.1:{PORT}                          ║
║  FRED Proxy: http://127.0.0.1:{PORT}/api/fred?...             ║
║  BEA Proxy:  http://127.0.0.1:{PORT}/api/bea?...              ║
║  BLS Proxy:  http://127.0.0.1:{PORT}/api/bls  (POST)          ║
║                                                              ║
║  Bound to {BIND} only. Press Ctrl+C to stop.                 ║
╚══════════════════════════════════════════════════════════════╝
""")

    server = HTTPServer((BIND, PORT), ProxyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
