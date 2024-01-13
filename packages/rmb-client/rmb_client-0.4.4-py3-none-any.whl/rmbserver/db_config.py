import sys
from py2neo import Graph
from qdrant_client import QdrantClient
from pymongo import MongoClient
from urllib.parse import quote_plus
from rmbserver import config
from rmbserver.log import log

from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

def get_graph_db():
    # 存储IDC元数据的图数据库
    try:
        log.info(f"连接Neo4j数据库：{config.neo4j_address}")
        return Graph(
            config.neo4j_address,
            name=config.neo4j_dbname,
            user=config.neo4j_username,
            password=config.neo4j_password
        )
    except Exception as e:
        log.error(f"连接Neo4j数据库失败：{e}")
        sys.exit(1)


def get_vector_db():
    try:
        if config.qdrant_address:
            log.info(f"连接Qdrant数据库服务：{config.qdrant_address}")
            return QdrantClient(
                url=config.qdrant_address
            )
        else:
            log.info(f"连接本地Qdrant数据库文件：{config.qdrant_local_file_path}")
            return QdrantClient(
                path=config.qdrant_local_file_path
            )
    except Exception as e:
        log.error(f"连接Qdrant数据库失败：{e}")
        sys.exit(1)



def get_mongo_db():
    try:
        log.info(f"连接MongoDB数据库：{config.mongodb_address}")

        # 检查是否仅提供了用户名而没有提供密码
        if config.mongodb_username and not config.mongodb_password:
            mongo_uri = "mongodb://%s@%s" % (
                quote_plus(config.mongodb_username),
                config.mongodb_address
            )
        elif config.mongodb_username and config.mongodb_password:
            # 如果提供了用户名和密码，则使用这两者构建URI
            mongo_uri = "mongodb://%s:%s@%s" % (
                quote_plus(config.mongodb_username),
                quote_plus(config.mongodb_password),
                config.mongodb_address
            )
        else:
            # 如果没有提供用户名和密码，则不在URI中包含它们
            mongo_uri = "mongodb://%s" % config.mongodb_address

        return MongoClient(mongo_uri)
    except Exception as e:
        log.error(f"连接MongoDB数据库失败：{e}")
        sys.exit(1)


class TSLogDBHelper:
    def __init__(self):
        try:
            self.client = InfluxDBClient(
                url=config.influxdb_address,
                token=config.influxdb_token,
                org=config.influxdb_org
            )

            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
            self.is_connected = True
            log.info(f"连接InfluxDB数据库：{config.influxdb_address}")
        except Exception as e:
            log.error(f"连接InfluxDB数据库失败：{e}")
            self.is_connected = False

    def w(self, data: dict):
        if not self.is_connected:
            return None
        try:
            return self.write_api.write(
                config.influxdb_bucket,
                config.influxdb_org,
                data,
            )
        except Exception as e:
            log.error(f"写入InfluxDB数据库失败：{e}")
            return None


# Service
service_graph_db = get_graph_db()

# Meta
meta_graph_db = service_graph_db
meta_vector_db = get_vector_db()

# Chat
chat_mongodb = get_mongo_db()
chat_mongodb_db = chat_mongodb[config.mongodb_dbname]


# TS Log
ts_log_db = TSLogDBHelper()

