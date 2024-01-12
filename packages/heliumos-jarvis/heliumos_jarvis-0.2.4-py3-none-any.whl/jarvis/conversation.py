from typing import (
    List,
    Optional, Dict, Any, Union,
)

from langchain.agents import AgentExecutor, Tool, Agent
from langchain.chains import LLMChain
from langchain.memory import ReadOnlySharedMemory
from langchain_core.memory import BaseMemory
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig, RunnableLambda, RunnableSerializable
from langchain_core.runnables.utils import Input, ConfigurableField
from langchain_core.tools import BaseTool
from langserve import RemoteRunnable
from pydantic.v1 import BaseModel
from jarvis import llm, embeddings
from jarvis.agents.conversation_agent import JarvisConversationalAgent
from jarvis.jarvis_configuration import settings
from jarvis.memories.vector_store import JarvisVectorStoreRetrieverMemory

from jarvis.prompts import PREFIX, SUFFIX, FORMAT_INSTRUCTIONS, SUFFIX_WITHOUT_HISTORY, REPHRASE_QUESTION_PROMPT
from jarvis.vectorstores.milvus import JarvisMilvus



class UsedToolInput(BaseModel):
    service_id: str
    usage_name: str
    usage_description: str
    configuration: Dict[str, Any]


class ConversationInput(BaseModel):
    input: str
    conversation_id: Optional[str] = None


class ConversationOutput(BaseModel):
    output: str


class ServiceInput(BaseModel):
    input: str


class ServiceOutput(BaseModel):
    output: str


class Conversation(RunnableSerializable[ConversationInput, ConversationOutput], BaseModel):
    character: str
    language: str
    used_tools: List[UsedToolInput]

    def _prepare_prompt(self, memory_required: bool, tools: List[BaseTool]) -> PromptTemplate:
        prompt = JarvisConversationalAgent.create_prompt(
            tools=tools,
            prefix=PREFIX.format(character=self.character),
            suffix=SUFFIX if memory_required else SUFFIX_WITHOUT_HISTORY,
            format_instructions=FORMAT_INSTRUCTIONS,
            input_variables=["input", "agent_scratchpad", "chat_history", "language"],
        )
        return prompt

    def _prepare_memory(self, input: Input) -> Union[JarvisVectorStoreRetrieverMemory, None]:
        conversation_id = input["conversation_id"]
        if conversation_id == None:
            return None

        vector_store = JarvisMilvus(
            embedding_function=embeddings,
            collection_name="JARVIS_MEMORY",
            drop_old=False,
            connection_args={
                "host": settings.MILVUS_HOST,
                "port": settings.MILVUS_PORT,
                "db_name": settings.MILVUS_DB,  # "default",
                "user": settings.MILVUS_USERNAME,  # "cdgouicgkz",
                "password": settings.MILVUS_PASSWORD,  # "YxX777FA0sT2rT4C",
            },
            partition_key="memory_id"
        )
        retriever = vector_store.as_retriever(
            searcg_type="mmr",
            search_kwargs={
                "k": 8,
                "fetch_k": 32,
                "expr": f"memory_id==\"{conversation_id}\"",
            },

        )
        history_memory = JarvisVectorStoreRetrieverMemory(
            memory_id=conversation_id,
            retriever=retriever,
            input_key="input",
            memory_key="chat_history",
            return_messages=True,
            exclude_input_keys=["language"],
        )
        return history_memory

    def _parse_tool_output(self, output: Dict[str, Any]):
        return output['output']

    def _prepare_tools(self) -> List[BaseTool]:
        # find the service url according to service_id
        tools = []
        for t in self.used_tools:
            # cong service registry 获取
            service = RemoteRunnable(url="http://localhost:8002/math") | RunnableLambda(self._parse_tool_output)
            _tool = Tool.from_function(
                func=lambda x: service.invoke({"input": x}, config=t.configuration),
                name=t.usage_name,  # 从配置里面获取
                description=t.usage_description + ".将完整的用户输入传递给该工具",  # 从配置里面获取
            )
            tools.append(_tool)
        return tools

    def _prepare_agent(self, prompt: PromptTemplate,
                       tools: List[BaseTool]) -> Agent:
        agent = JarvisConversationalAgent.from_llm_and_tools(
            llm=llm,
            tools=tools,
            verbose=True,
            early_stopping_method='force',
            prompt=prompt,
        )
        agent.llm_chain.verbose = True
        return agent

    def rephrase_input(self, input: Input, memory: BaseMemory) -> str:
        r_memory = ReadOnlySharedMemory(memory=memory)
        rephrase_question_chain = LLMChain(
            llm=llm,
            prompt=REPHRASE_QUESTION_PROMPT,
            verbose=True,
            memory=r_memory
            # callbacks=callbacks,
        )

        rephrase_question = rephrase_question_chain.invoke({
            "input": input["input"],
        })
        print(rephrase_question)
        new_input = rephrase_question["text"]
        return new_input

    def invoke(self, input: Input, config: Optional[RunnableConfig] = None) -> ConversationOutput:

        memory = self._prepare_memory(input)  # prepare memory
        # history = memory.load_memory_variables({"input": input["input"]})
        if memory is not None:
            new_input = self.rephrase_input(input, memory)
        else:
            new_input = input["input"]
        tools = self._prepare_tools()  # prepare tools
        prompt = self._prepare_prompt(memory_required=memory is not None, tools=tools)  # prepare prompt
        agent = self._prepare_agent(prompt, tools)  # prepare agent
        # prepare agent executor
        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=tools,
            verbose=True,
            memory=memory,
            handle_parsing_errors="respond to user: I can not answer the question for now",
        )

        rs = agent_executor.invoke(
            input={
                "input": new_input,
                "language": self.language,
            },
            config=config
        )
        return ConversationOutput(output=rs['output'])


conversation = Conversation(
    character="You are a friendly Assistant that having a conversation with a human. You NEVER \
answer that you are an AI language model. If you don't know the answer truthfully \
say you don't have an answer. Don't make up an answer.",
    language="Chinese",
    used_tools=[]
).configurable_fields(
    character=ConfigurableField(
        id="character",
        name="Character",
        description="Character is basic prompt for LLM",

    ),
    language=ConfigurableField(
        id="language",
        name="Language",
        description="Language for LLM",

    ),
    used_tools=ConfigurableField(
        id="used_tools",
        name="Used Tools",
        description="Tools for conversation",

    )
)
