import http.server
from prometheus_client import start_http_server, Counter
import random

APP_PORT = 8000
METRICS_PORT = 8001
REQUEST_COUNT= Counter("app_request_count", "Total All Http Request Count",["app_name", "endpoint"])
RANDOM_REQUEST_COUNT= Counter("app_random_count", "Increment counter by random")

class HandleRequests(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        REQUEST_COUNT.labels("prom_python_app", self.path).inc()
        random_val = random.random() * 10
        RANDOM_REQUEST_COUNT.inc(random_val)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>First Application</title></head><body style='color: #333; margin-top: 30px;'><center><h2>Welcome to our first Prometheus-Python application.</center></h2></body></html>", "utf-8"))
        self.wfile.close()

if __name__ == "__main__":
    print(f"Running server on: {APP_PORT}")
    start_http_server(METRICS_PORT)
    server = http.server.HTTPServer(('localhost', APP_PORT), HandleRequests)
    server.serve_forever()