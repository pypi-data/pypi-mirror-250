from rmbserver.brain.datasource import DataSource
from rmbcommon.models import StrucQuery, QueryResult

from rmbserver.ai.generations import ai_generate
from rmbserver.ai.prompts.agent import (
    PROMPT_CHOOSE_DATASOURCE,
    PROMPT_GEN_STRUC_QUERY,
    PROMPT_GEN_DISTINCT_QUERIES,
    PROMPT_CORRECT_CONSTANT_VALUE,
)

from rmbserver.exceptions import (
    QAErrorNoMatchDataSource,
    QAErrorInsufficientData,
    QAErrorIncompleteQuestion,
    InvalidStrucQuery,
)
from rmbserver.log import log


class DataRetriever:

    @staticmethod
    def choose_a_data_source(datasources, question: str) -> DataSource:
        ds_summary = ""
        for ds in datasources:
            ds_summary += f"{ds.type}数据源[{ds.name}][{ds.id}]包含以下数据表：\n"
            ds_summary += ds.brain_meta.to_table(level='table')

        choice_datasource = ai_generate(
            "CHOOSE_DATASOURCE",
            PROMPT_CHOOSE_DATASOURCE,
            template_format="jinja2",
            question=question,
            datasources_summary=ds_summary
        )["choice_datasource_id"]
        if choice_datasource:
            return DataSource.get(choice_datasource)
        else:
            raise QAErrorNoMatchDataSource(
                f"从你选择的数据源（{','.join([ds.name for ds in datasources])}）"
                f"中无法回答问题【{question}】。"
            )

    @staticmethod
    def correct_constant_value(data_source, meta_data, struc_queries):
        """
        struc_queries = [
                    {
                      "content': "SELECT score FROM students WHERE name = :stu_name",
                      "params": {
                        "stu_name": {
                          "field_full_name": "exam_db.students.name",
                          "value": "张三",
                      },
                    }
               ]
        """
        field_full_names = []
        for query in struc_queries["structure_queries"]:
            params = query.get("params", {})
            for param_name, param_info in params.items():
                field_name = param_info.get('field_full_name', None)
                if field_name:
                    field_full_names.append(field_name)

        if field_full_names:
            log.info(f"需要使用绑定变量查询，对绑定的变量值的准确性进行检查...")
            # 如果有字段是绑定变量，则生成对这些字段的查询语句
            dist_values_queries = ai_generate(
                "GEN_DISTINCT_QUERIES",
                PROMPT_GEN_DISTINCT_QUERIES,
                datasource_prompt=data_source.accessor.PROMPT_GEN_STRUC_QUERY,
                field_full_names=field_full_names,
                top_n_values=100,  # 最大100(不能超过 model/excel.py 中的最大值）
            )

            # 执行这些查询语句，获取结果
            dist_values = {}
            for _field, _query in dist_values_queries.items():
                rst = data_source.accessor.query(StrucQuery(_query), meta_data)
                dist_values[_field] = [r[0] for r in rst.rows]

            # 根据原语句和部分字段的结果，来修正这些语句
            corrected_struc_queries = ai_generate(
                "CORRECT_CONSTANT_VALUE",
                PROMPT_CORRECT_CONSTANT_VALUE,
                struc_queries=struc_queries,
                dist_values=dist_values,
            )
            if corrected_struc_queries == struc_queries:
                log.info(f"查询语句中的变量值正确，无需修正。")
            else:
                log.info(f"对查询语句中的变量值进行了修正：\n"
                         f"原语句：\n"
                         f"{struc_queries}\n"
                         f"新语句:\n"
                         f"{corrected_struc_queries}\n")
            return corrected_struc_queries
        else:
            log.info("没有使用绑定变量，无需检查变量值。")
            return struc_queries

    @classmethod
    def query_to_a_data_source(
            cls,
            data_source: DataSource,
            question: str
    ) -> list[QueryResult]:

        meta_data = data_source.brain_meta

        output = ai_generate(
            "GEN_STRUC_QUERY",
            PROMPT_GEN_STRUC_QUERY,
            datasource_prompt=data_source.accessor.PROMPT_GEN_STRUC_QUERY,
            bi_question=question,
            meta_data=meta_data.to_dict_for_agent(),
        )
        if output.get("possible_missing_table", None):
            log.warning(f"从{data_source.name}[{data_source.id}]中查询：{question}，")
            raise QAErrorInsufficientData(
                f"在{data_source.name}[{data_source.id}]中查询{question}，"
                f"缺失这些信息: {output['possible_missing_table']}")
        elif output.get("need_feedback", None):
            log.warning(f"问题不完整：{question}|{output['need_feedback']}")
            raise QAErrorIncompleteQuestion(output['need_feedback'])

        output.pop("possible_missing_table", None)
        output.pop("need_feedback", None)
        # 检查查询语句中的常量的值是否正确
        corrected_output = cls.correct_constant_value(
            data_source,
            meta_data,
            output,
        )

        # 从生成的内容中提取 Query 语句
        struc_queries = []
        for query in corrected_output["structure_queries"]:
            content = query["content"]
            params = query.get("params", None)
            struc_queries.append(
                StrucQuery(content, params)
            )

        results = [data_source.accessor.query(query, meta_data)
                   for query in struc_queries]
        log.info(f"\n数据源：{data_source}"
                 f"\n问题：{question}"
                 f"\n查询结果：{results}")
        return results

    @classmethod
    def get_query_result_by_question(cls, datasources, question: str) -> list[QueryResult]:
        # choose a data source
        if len(datasources) == 1:
            data_source = datasources[0]
        else:
            data_source = cls.choose_a_data_source(datasources, question)

        # query to a data source
        # 如果出现生成的语句不合法，则进行重试
        max_retries = 2
        for attempt in range(1, max_retries + 1):
            try:
                return cls.query_to_a_data_source(data_source, question)
            except InvalidStrucQuery as e:
                if attempt == max_retries:
                    log.error(f"查出错误，超过最大重试次数{max_retries}，报错退出")
                    raise
                log.warning(f"查询报错，第{attempt}次重试..")

    @classmethod
    def run(cls, datasources, question):
        results = cls.get_query_result_by_question(
            datasources, question
        )
        results_str = '\n'.join([str(r) for r in results])
        return results_str
