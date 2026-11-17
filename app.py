"""Loopback-only research viewer. Run: python app.py."""
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import parse_qs, urlparse
from experiment import evaluate


def page(result):
    # Shared axes preserve visual magnitude differences and camera drift.
    values = result["truth"] + [v for v in result["observed"] if v is not None]
    low, high = min(values), max(values)
    def points(series):
        return " ".join(f"{i * 900 / (len(series)-1):.2f},{220-(v-low)*200/max(high-low,1):.2f}"
                        for i, v in enumerate(series) if v is not None)
    summary = {k: v for k, v in result.items() if k not in ("truth", "observed")}
    return f'''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Equine gait methods sandbox</title>
<style>body{{font:17px system-ui;max-width:1000px;margin:40px auto;padding:16px;background:#f3f6f8;color:#182937}}label{{display:inline-block;margin:12px}}button{{padding:10px}}svg{{background:white;width:100%}}pre{{white-space:pre-wrap}}.notice{{border-left:5px solid #b65c00;padding:16px;background:#fff1d8}}</style>
<h1>Equine gait methods sandbox</h1><p class="notice">Synthetic engineering experiment · No horse video analyzed · No clinical interpretation</p>
<p>Explore vertical signal distortion from additive tracking noise and camera roll. Units are arbitrary scene units. Stride boundaries are known, not detected.</p>
<form><label>Noise standard deviation <input aria-label="Noise standard deviation" name="noise" type="number" min="0" max="20" step="0.1" value="{result['config']['noise']}"></label>
<label>Camera roll (degrees) <input name="roll" type="number" min="-30" max="30" step="0.5" value="{result['config']['roll']}"></label><button>Run experiment</button></form>
<h2>Reference and measurement</h2><p>Teal: reference; orange: simulated measurement. Horizontal axis: frame; vertical axis: scene units (auto scaled).</p>
<svg viewBox="0 0 900 240" role="img" aria-label="Reference and measured vertical trajectories"><polyline fill="none" stroke="#087e8b" points="{points(result['truth'])}"/><polyline fill="none" stroke="#bd5900" points="{points(result['observed'])}"/></svg>
<h2>Reproducible run record</h2><p>Bias is signed measured minus reference; MAE is mean absolute error over retained strides. These are simulation errors, not clinical accuracy.</p><pre>{escape(json.dumps(summary, indent=2))}</pre></html>'''


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            query = parse_qs(urlparse(self.path).query)
            result = evaluate(noise=float(query.get("noise", [0.5])[0]),
                              roll=float(query.get("roll", [0])[0]))
            body = page(result).encode()
            self.send_response(200)
        except (ValueError, OverflowError):
            body = b"Invalid parameters: noise 0-20; roll -30 to 30."
            self.send_response(400)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print("Research viewer: http://127.0.0.1:8000 (Ctrl-C to stop)")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
