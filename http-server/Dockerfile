FROM python:3.9-slim

WORKDIR /app

RUN pip install flask prometheus-client

COPY server_http.py .

CMD ["python", "server_http.py"]
