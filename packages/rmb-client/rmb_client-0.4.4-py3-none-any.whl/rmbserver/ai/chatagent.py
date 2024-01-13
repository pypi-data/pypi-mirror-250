from functools import wraps
import httpx

from langchain.agents import (
    # AgentType,
    Tool,
    # initialize_agent,
)
from langchain.agents import AgentExecutor, ConversationalAgent
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from rmbserver import config
from rmbserver.log import log
from rmbserver.ai.prompts.agent import (
    PROMPT_AGENT_PREFIX,
    PROMPT_AGENT_SUFFIX,
    PROMPT_AGENT_FORMAT_INSTRUCTIONS,
)

from rmbserver.exceptions import BIQAError
from rmbserver.analysis.chat import Chat
from rmbserver.ai.tools import DataRetriever, ChartGenerator, ExcelGenerator


# 记录 LLM 日志的三方服务 Portkey
# from langchain.utilities import Portkey
# PORTKEY_API_KEY = "1aqtCtfA6WrZyNhO2PdOk0iQtjg="
# TRACE_ID = "rmbserver"
#
# openai_headers = Portkey.Config(
#     api_key=PORTKEY_API_KEY,
#     trace_id=TRACE_ID,
# )


def handle_biqa_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BIQAError as e:
            error_type = e.__class__.__name__
            return f"查询失败，原因是 {error_type}: {e}"
    return wrapper


class ChatAgentManager:

    def __init__(self, chat: Chat):
        self.chat = chat
        self.agent = self.create_agent()

    @handle_biqa_error
    def tool_data_query(self, question: str) -> str:
        return DataRetriever.run(self.chat.datasources, question)

    @handle_biqa_error
    def tool_execl_generator(self, question: str) -> str:
        return ExcelGenerator.run(self.chat.datasources, question)

    @handle_biqa_error
    def tool_chart_generator(self, question: str) -> str:
        return ChartGenerator.run(self.chat.datasources, question)

    @property
    def tools(self):
        return [
            Tool(
                name="DataQuery Tool",
                description="Useful for when you need to query to a private database using natural language."
                            "If you only need to query results from table data ,"
                            " then you need to select this tool.",
                func=self.tool_data_query,
            ),
            # Tool(
            #     name="question integrity check",
            #     description="check if the bi question is complete before answering",
            #     func=self.tool_check_question_integrity,
            # ),
            Tool(
                name="ExcelGenerator Tool",
                description="Useful for when you need to generate an Excel file using natural language. "
                            "If it involves processing table data, then you need to select this tool "
                            "to save the processed data.",
                func=self.tool_execl_generator,
            ),
            Tool(
                name="ChartGenerator Tool",
                description="Useful for when you need to generate chart using "
                            "natural language from a private database. ",
                func=self.tool_chart_generator,
            ),
        ]

    @property
    def agent_prompt(self):
        prompt = ConversationalAgent.create_prompt(
            self.tools,
            prefix=PROMPT_AGENT_PREFIX,
            suffix=PROMPT_AGENT_SUFFIX,
            format_instructions=PROMPT_AGENT_FORMAT_INSTRUCTIONS,
        )
        return prompt

    def create_agent(self, ):
        kwargs = {
            "model": config.openai_model_name,
            "openai_api_key": config.openai_api_key,
            "verbose": True,
            # "default_headers": openai_headers,
            # Agent 里面不能用JSON输出，ReAct output parser 要跟着改
            # "model_kwargs": {
            #     "response_format": {"type": "json_object"},
            # },
        }
        if config.openai_proxy:
            kwargs["http_client"] = httpx.Client(
                proxies=config.openai_proxy,
            )

        llm = ChatOpenAI(**kwargs)

        # memory
        memory = ConversationBufferMemory(memory_key="chat_history")

        for msg in self.chat.messages(limit=30):
            if msg.role == 'human':
                memory.chat_memory.add_user_message(str(msg.content))
            elif msg.role == 'ai':
                memory.chat_memory.add_ai_message(str(msg.content))
            else:
                log.warning(f"Unknown message role: {msg}")

        # Re-define Agent Prompt
        llm_chain = LLMChain(llm=llm, prompt=self.agent_prompt)

        agent = ConversationalAgent(
            llm_chain=llm_chain,
            tools=self.tools,
        )

        chat_agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            memory=memory,
            verbose=True,
        )

        # # Direct create agent executor
        # chat_agent_executor = initialize_agent(
        #     self.tools,
        #     llm,
        #     agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        #     verbose=True,
        #     memory=memory,
        #     # output_parser=ReActSingleInputOutputParser(),
        #     # output_parser=ConvoOutputParser(),
        # )

        return chat_agent_executor

    def query(self, question: str) -> str:
        response = self.agent.invoke({"input": question})["output"]
        # log.debug(f"\nHuman: {question} \nAI: {response}")
        return response
