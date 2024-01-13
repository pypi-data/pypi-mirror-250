

PROMPT_ANALYSE_CHART_QUESTION = """
您是一名优秀的业务分析师。请分析用户的问题，判断使用哪种Chart更有利于信息的展示，并对问题重写，用于告诉数据分析师你需要哪些数据用来生成图表。

分析结果以下面的格式返回：
{"chart_type": bar, "rewritten_question": "重写后的问题"}

其中 chart_type 必须从这些值中选择： bar, line, pie

问题：{{ question }}

分析结果：
"""


PROMPT_GEN_CHART_DATA = """
根据用户的问题、查到的数据来生成渲染{{ chart_type }}图所需要的数据。

生成{{ chart_type }}图需要的数据格式为：
{{ data_sample }}

要求：
{{ data_requires }} 


查询到的数据： {{ query_results }}


{{ chart_type }}图需要的数据：
"""
