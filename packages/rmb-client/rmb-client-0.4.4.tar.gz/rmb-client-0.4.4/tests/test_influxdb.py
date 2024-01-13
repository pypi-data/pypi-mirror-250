from rmbclient.rmb import ReliableMetaBrain as RMB
from rmbserver import config

rmb = RMB()

print(rmb.datasources)

try:
    ds = rmb.datasources.register(
        ds_type="InfluxDB",
        ds_name="InfluxDB",
        ds_access_config={
            "url": config.influxdb_address,
            "token": config.influxdb_token,
            "org": config.influxdb_org
        }
    )
except:
    ds = rmb.datasources.get(name="InfluxDB")

print(ds.meta.get("runtime"))


