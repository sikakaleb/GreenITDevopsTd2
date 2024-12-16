from flask import Flask, request
from prometheus_client import start_http_server, Gauge

app = Flask(__name__)
http_size_metric = Gauge('http_total_size', 'Total HTTP data size in bytes')

total_size_http = 0

@app.route('/data', methods=['POST'])
def receive_data():
    global total_size_http
    body_size = len(request.data)
    headers_size = sum(len(k) + len(v) for k, v in request.headers.items())
    total_size = body_size + headers_size
    total_size_http += total_size
    http_size_metric.set(total_size_http)
    print(f"HTTP Request Size: {total_size} bytes (Headers: {headers_size}, Body: {body_size})")
    return "Received", 200

if __name__ == "__main__":
    start_http_server(8001)  # Expose metrics on port 8001
    app.run(host='0.0.0.0', port=5000)
