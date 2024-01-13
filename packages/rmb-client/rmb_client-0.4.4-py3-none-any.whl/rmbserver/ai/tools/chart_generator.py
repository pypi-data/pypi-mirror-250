
from io import BytesIO
from datetime import timedelta

from rmbcommon.tools import gen_img_file_id
from rmbserver.ai.prompts.chart import (
    PROMPT_ANALYSE_CHART_QUESTION,
    PROMPT_GEN_CHART_DATA,
)
from rmbserver.ai.generations import ai_generate
from rmbserver.log import log
from rmbserver.store import oss_bucket
from rmbserver.ai.tools.charts.chart_pyplot import (
    gen_image,
    ChartLine,
    ChartPie,
    ChartBar,
)
from rmbserver.ai.tools.data_query import DataRetriever


class ChartGenerator:

    @staticmethod
    def analyse_chart(question: str) -> tuple:
        rst = ai_generate(
            "ANALYSE_CHART_QUESTION",
            PROMPT_ANALYSE_CHART_QUESTION,
            question=question,
        )
        chart_type = rst.get('chart_type')
        rewritten_question = rst.get('rewritten_question')
        log.info(f"图表类型：{chart_type}，重写后的问题：{rewritten_question}")
        return chart_type, rewritten_question

    @staticmethod
    def gen_chart_data(chart_type, query_results):
        if chart_type == 'line':
            data_sample = ChartLine.data_sample
            data_requires = ChartLine.data_requires
        elif chart_type == 'bar':
            data_sample = ChartBar.data_sample
            data_requires = ChartBar.data_requires
        elif chart_type == 'pie':
            data_sample = ChartPie.data_sample
            data_requires = ChartPie.data_requires
        else:
            raise ValueError(f"Unknown chart type: {chart_type}")

        chart_data = ai_generate(
            "GEN_CHART_DATA",
            PROMPT_GEN_CHART_DATA,
            chart_type=chart_type,
            data_sample=data_sample,
            data_requires=data_requires,
            query_results='\n'.join([str(r) for r in query_results]),
        )
        return chart_data

    @staticmethod
    def gen_and_save_chart(chart_type, chart_data):
        image_name = f"{gen_img_file_id()}.png"
        oss_path = f"images/{image_name}"
        image_file = BytesIO()

        gen_image(chart_type, chart_data, image_file_path=image_file)
        image_file.seek(0)
        # 确保文件已经关闭
        oss_bucket.put_object(oss_path, image_file)

        # 设置URL的过期时间（例如，1小时）
        expire_time = timedelta(hours=1)
        url = oss_bucket.sign_url('GET', oss_path, int(expire_time.total_seconds()))
        # log.debug(f"Chart Image 下载地址：{url}")
        return url

    @classmethod
    def run(cls, datasources, question):
        chart_type, rewritten_question = cls.analyse_chart(question)
        log.info(f"\n图表类型：{chart_type} "
                 f"\n原问题：{question}"
                 f"\n重写后的问题：{rewritten_question}")
        query_results = DataRetriever.get_query_result_by_question(
            datasources, rewritten_question
        )
        log.info(f"查询结果：{query_results}")
        chart_data = cls.gen_chart_data(chart_type, query_results)
        # log.info(f"图表数据：{chart_data}")
        chart_img_url = cls.gen_and_save_chart(chart_type, chart_data)
        log.info(f"图表图片下载地址：{chart_img_url}")
        return f"Chart Image 下载地址：{chart_img_url}"


if __name__ == '__main__':
    import json
    ChartGenerator.gen_and_save_chart('line', json.loads(ChartLine.data_sample))
    ChartGenerator.gen_and_save_chart('pie', json.loads(ChartPie.data_sample))