import time
import json
import psycopg2
from pymongo import MongoClient
from influxdb_client import InfluxDBClient, WriteOptions
from prometheus_client import Gauge, start_http_server

# Prometheus metrics
write_time_metric = Gauge("write_time", "Time taken to write data (ms)")
read_time_metric = Gauge("read_time", "Time taken to read data (ms)")
aggregation_time_metric = Gauge("aggregation_time", "Time taken to aggregate data (ms)")

# Start Prometheus metrics server
start_http_server(8000)

# Load test data
with open('/app/data/donnees_petit.json', 'r') as f:
    data = json.load(f)

# PostgreSQL functions
def test_postgres():
    conn = psycopg2.connect(host="postgres", dbname="metrics", user="admin", password="admin")
    cur = conn.cursor()

    # Create table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP,
        temperature REAL,
        humidity INT,
        wind_speed REAL
    )
    """)
    conn.commit()

    # Write data
    start = time.time()
    for entry in data:
        cur.execute("INSERT INTO sensor_data (timestamp, temperature, humidity, wind_speed) VALUES (%s, %s, %s, %s)",
                    (entry['date'], entry['temperature_reelle'], entry['humidite'], entry['vent']))
    conn.commit()
    write_time = (time.time() - start) * 1000
    write_time_metric.set(write_time)

    # Read data
    start = time.time()
    cur.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 100")
    rows = cur.fetchall()
    read_time = (time.time() - start) * 1000
    read_time_metric.set(read_time)

    # Aggregate data
    start = time.time()
    cur.execute("SELECT AVG(temperature) FROM sensor_data")
    avg_temp = cur.fetchone()[0]
    aggregation_time = (time.time() - start) * 1000
    aggregation_time_metric.set(aggregation_time)

    cur.close()
    conn.close()

# MongoDB functions
def test_mongodb():
    client = MongoClient("mongodb://mongodb:27017/")
    db = client.metrics
    collection = db.sensor_data

    # Write data
    start = time.time()
    for entry in data:
        collection.insert_one(entry)
    write_time = (time.time() - start) * 1000
    write_time_metric.set(write_time)

    # Read data
    start = time.time()
    list(collection.find().sort("date", -1).limit(100))
    read_time = (time.time() - start) * 1000
    read_time_metric.set(read_time)

    # Aggregate data
    start = time.time()
    avg_temp = collection.aggregate([{"$group": {"_id": None, "avgTemp": {"$avg": "$temperature_reelle"}}}])
    aggregation_time = (time.time() - start) * 1000
    aggregation_time_metric.set(aggregation_time)

    client.close()

# InfluxDB functions
def test_influxdb():
    client = InfluxDBClient(url="http://influxdb:8086", token="admin", org="admin", bucket="metrics")
    write_api = client.write_api(write_options=WriteOptions(batch_size=1))

    # Write data
    start = time.time()
    for entry in data:
        point = {
            "measurement": "sensor_data",
            "time": entry['date'],
            "fields": {
                "temperature": entry['temperature_reelle'],
                "humidity": entry['humidite'],
                "wind_speed": entry['vent']
            }
        }
        write_api.write(bucket="metrics", record=point)
    write_time = (time.time() - start) * 1000
    write_time_metric.set(write_time)

    # Read data
    start = time.time()
    query = 'from(bucket:"metrics") |> range(start: -1h)'
    tables = client.query_api().query(query)
    read_time = (time.time() - start) * 1000
    read_time_metric.set(read_time)

    # Aggregate data
    start = time.time()
    query = 'from(bucket:"metrics") |> range(start: -1h) |> mean()'
    tables = client.query_api().query(query)
    aggregation_time = (time.time() - start) * 1000
    aggregation_time_metric.set(aggregation_time)

    client.close()

# Run tests
print("Testing PostgreSQL...")
test_postgres()

print("Testing MongoDB...")
test_mongodb()

print("Testing InfluxDB...")
test_influxdb()
