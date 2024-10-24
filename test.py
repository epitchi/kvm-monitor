from main import create_influxdb_point
from modules import disk
import os
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

influx_url = os.getenv("INFLUX_URL")
influx_token = os.getenv("INFLUX_TOKEN")
influx_org = os.getenv("INFLUX_ORG")
influx_bucket = os.getenv("INFLUX_BUCKET")

client = influxdb_client.InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
write_api = client.write_api(write_options=SYNCHRONOUS)


module_name = "disk"

data = module_name.collect_data();

if isinstance(data, list):
    # If collect data return multiple records
    for record in data:
        point = create_influxdb_point(module_name, record)
        write_api.write(bucket=influx_bucket, org=influx_org, record=point)
        print(f"writing record for {module_name} finished.")

else:
    point = create_influxdb_point(module_name, data)
    write_api.write(bucket=influx_bucket, org=influx_org, record=point)
    print(f"writing record for {module_name} finished.")