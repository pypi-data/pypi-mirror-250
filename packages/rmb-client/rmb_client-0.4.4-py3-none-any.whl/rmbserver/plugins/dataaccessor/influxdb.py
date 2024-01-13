import pandas as pd
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.flux_table import FluxTable
from rmbserver.plugins.dataaccessor.da_base import BaseDataAccessor
from rmbserver.plugins.dataaccessor.da_register import register_data_accessor
from rmbserver.log import log
from rmbcommon.models import MetaData, DataSchema, DataTable, DataField, QueryResult


@register_data_accessor
class InfluxDBDataAccessor(BaseDataAccessor):
    __source_type__ = "InfluxDB"
    __access_config_keys_must__ = ['token', 'org', 'url']
    __access_config_keys_safe__ = ['url', 'org']
    __ignore_schemas__ = ['_monitoring', '_tasks']

    def _get_influxdb_client(self):
        # 构建InfluxDB客户端
        return InfluxDBClient(url=self.ds_access_config['url'],
                              token=self.ds_access_config['token'],
                              org=self.ds_access_config['org'])

    def retrieve_meta_data(self) -> MetaData:
        client = self._get_influxdb_client()
        metadata_object = MetaData(name=f"InfluxDB_{self.ds_access_config['url']}")

        try:
            buckets_api = client.buckets_api()
            buckets = buckets_api.find_buckets().buckets

            for bucket in buckets:
                if bucket.name in self.__ignore_schemas__:
                    continue
                bucket_name = bucket.name
                data_schema = DataSchema(
                    name=bucket_name,
                    metadata=metadata_object,
                    origin_desc=""
                )

                query_api = client.query_api()
                tables = query_api.query(f'import "influxdata/influxdb/schema" '
                                         f'schema.measurements(bucket: "{bucket_name}")')

                for table in tables:
                    for record in table.records:
                        measurement_name = record.get_value()
                        data_table = DataTable(
                            name=measurement_name,
                            origin_desc="",
                            schema=data_schema
                        )

                        # 示例，获取每个 measurement 的 fields 和 tags
                        fields_query = (f'import "influxdata/influxdb/schema" '
                                        f'schema.fieldKeys(bucket: "{bucket_name}", '
                                        f'predicate: (r) => r._measurement == "{measurement_name}")')
                        tags_query = (f'import "influxdata/influxdb/schema" '
                                      f'schema.tagKeys(bucket: "{bucket_name}", '
                                      f'predicate: (r) => r._measurement == "{measurement_name}")')

                        fields = query_api.query(fields_query)
                        tags = query_api.query(tags_query)

                        for field in fields:
                            for r in field.records:
                                data_field = DataField(
                                    name=r.get_value(),
                                    origin_desc="",
                                    table=data_table
                                )
                                data_table.add_field(data_field)

                        for tag in tags:
                            for r in tag.records:
                                data_field = DataField(
                                    name=r.get_value(),
                                    origin_desc="",
                                    table=data_table
                                )
                                data_table.add_field(data_field)

                        data_schema.add_table(data_table)

                metadata_object.add_schema(data_schema)

        except Exception as e:
            log.error(f"An error occurred: {e}", exc_info=True)
        finally:
            client.close()

        return metadata_object

    def query(self, struc_query, meta_data: MetaData):
        # TODO: 待实现
        # flux_query = struc_query.content
        # log.debug(f"执行Flux查询语句：{flux_query}")
        #
        # if not isinstance(flux_query, str):
        #     raise TypeError(f"flux_query must be a string, not {type(flux_query)}")
        #
        # client = self._get_influxdb_client()
        # query_api = client.query_api()
        # result = query_api.query(flux_query)
        #
        # # 将结果转换为 DataFrame
        # df = pd.DataFrame([record.values for table in result for record in table.records])

        df = pd.DataFrame()
        return QueryResult(query=struc_query, result=df)
