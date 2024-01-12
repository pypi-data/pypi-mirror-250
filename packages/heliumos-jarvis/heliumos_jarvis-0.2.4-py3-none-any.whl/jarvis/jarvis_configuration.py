from pydantic_settings import BaseSettings


class JarvisSettings(BaseSettings):
    INFERENCE_MODEL_HOST: str = "localhost"
    INFERENCE_MODEL_PORT: str = "17880"

    EMBEDDING_MODEL_HOST: str = "localhost"
    EMBEDDING_MODEL_PORT: str = "17880"

    MILVUS_HOST: str = ""
    MILVUS_PORT: str = ""
    MILVUS_USERNAME: str = ""
    MILVUS_PASSWORD: str = ""
    MILVUS_DB: str = ""

    POSTGRES_HOST: str = ""
    POSTGRES_PORT: str = ""
    POSTGRES_USERNAME: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""


settings = JarvisSettings()
print(settings)
