import os

# 是否开启debug模式
DEBUG = True


# 读取Neo4j 数据库环境变量
# Graph 存储的是 Meta Data
neo4j_username = os.environ.get("NEO4J_USERNAME", 'neo4j')
neo4j_password = os.environ.get("NEO4J_PASSWORD", 'Pass1234')
neo4j_dbname = os.environ.get("NEO4J_DBNAME", 'leletest')
neo4j_address = os.environ.get("NEO4J_ADDRESS", 'bolt://127.0.0.1:32768')

# 读取 MongoDB 环境变量
# MongoDB 存储的是 Chat History
mongodb_username = os.environ.get("MONGODB_USERNAME", '')
mongodb_password = os.environ.get("MONGODB_PASSWORD", '')
mongodb_address = os.environ.get("MONGODB_ADDRESS", 'localhost:32773')
mongodb_dbname = os.environ.get("MONGODB_DBNAME", 'lele_test')


# 读取Qdrant环境变量  如果 qdrant_address 为空，则使用本地文件
qdrant_address = os.environ.get("QDRANT_ADDRESS", 'http://localhost:32772')

# influxdb 环境变量
influxdb_address = os.environ.get("INFLUXDB_ADDRESS", 'https://influxdb.infra.datamini.cn')
influxdb_token = os.environ.get("INFLUXDB_TOKEN", 'datamini126godatamini126go')
influxdb_org = os.environ.get("INFLUXDB_ORG", 'org-datamini')
influxdb_bucket = os.environ.get("INFLUXDB_BUCKET", 'bkt-rmb')


# 生成文件的存储位置
oss_access_key_id = os.environ.get("OSS_ACCESS_KEY_ID", '')
oss_access_key_secret = os.environ.get("OSS_ACCESS_KEY_SECRET", '')
oss_endpoint = os.environ.get("OSS_ENDPOINT", 'oss-cn-shanghai.aliyuncs.com')
oss_bucket_name = os.environ.get("OSS_BUCKET_NAME", 'tablebot-gen-files')

# 用户上传文件的存储位置

oss_ugc_endpoint = os.environ.get("OSS_UGC_ENDPOINT", 'oss-cn-shanghai.aliyuncs.com')
oss_ugc_bucket_name = os.environ.get("OSS_UGC_BUCKET_NAME", 'tablebot-user-files')


openai_api_key = os.environ.get("OPENAI_API_KEY", '')
openai_proxy = os.environ.get("OPENAI_PROXY", 'http://127.0.0.1:8001')

# ServerTokens
server_tokens = os.environ.get("RMB_SERVER_TOKENS", 'token1')
