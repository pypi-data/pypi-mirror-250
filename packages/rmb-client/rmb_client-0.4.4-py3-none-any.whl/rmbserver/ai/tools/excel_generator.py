from rmbcommon.models import QueryResult
from rmbcommon.tools import gen_excel_file_id
from io import BytesIO
from rmbserver.store import oss_bucket
from datetime import timedelta
from rmbserver.log import log
from rmbserver.ai.tools.data_query import DataRetriever


class ExcelGenerator:

    @staticmethod
    def save_results_to_excel_on_oss(results: list[QueryResult]):
        # 生成临时Excel文件
        file_name = f"{gen_excel_file_id()}.xlsx"
        excel_file = BytesIO()
        for i, data in enumerate(results):
            log.info(f"\n将查询结果写入Excel文件的Sheet{i + 1}：{data}")
            data.result.to_excel(
                excel_file, sheet_name=f'Sheet{i + 1}', index=False)
        excel_file.seek(0)

        # 上传到OSS
        oss_bucket.put_object(file_name, excel_file)

        # 设置URL的过期时间（例如，1小时）
        expire_time = timedelta(hours=1)
        url = oss_bucket.sign_url('GET', file_name, int(expire_time.total_seconds()))
        return url

    @classmethod
    def run(cls, datasources, question):
        query_results = DataRetriever.get_query_result_by_question(
            datasources, question
        )
        # 如果返回的行数过少，则直接返回结果不再生成文件
        if len(query_results) == 1 and query_results[0].row_count < 5:
            rst = '不需要生成文件，结果比较少，可以直接返回：'
            rst += '\n'.join([str(r) for r in query_results])
            log.info(rst)
            return rst

        url = cls.save_results_to_excel_on_oss(query_results)
        return f"您可以从下面地址下载处理好的数据：{url}"
