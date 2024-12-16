FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install psycopg2 pymongo influxdb-client prometheus_client

COPY tester.py .

CMD ["python", "tester.py"]
