import threading

from langchain_openai import ChatOpenAI
from snowflake import SnowflakeGenerator

from jarvis.embeddings.openai import JarvisOpenAIEmbeddings
from jarvis.jarvis_configuration import settings


llm = ChatOpenAI(
    openai_api_base=f"http://{settings.INFERENCE_MODEL_HOST}:{settings.INFERENCE_MODEL_PORT}/v1",
    openai_api_key="EMPTY",
    model="gpt-3.5-turbo",
    temperature=0.5,
    top_p=0.3,
    default_headers={"x-heliumos-appId": "general-inference"},
    tiktoken_model_name="gpt-3.5-turbo",
    verbose=True,
)
embeddings = JarvisOpenAIEmbeddings(
    openai_api_base=f"http://{settings.EMBEDDING_MODEL_HOST}:{settings.EMBEDDING_MODEL_PORT}/v1",
    openai_api_key="EMPTY",
    default_headers={"x-heliumos-appId": "text-embedding"},
    model="text-embedding-ada-002",
    # chunk_size=512,
    # tiktoken_model_name="text-embedding-ada-002"
)

gen = SnowflakeGenerator(2)
lock = threading.Lock()
