import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """应用配置"""

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4"

    # 向量数据库
    vectorstore_type: str = "chroma"  # chroma, pinecone, weaviate
    chroma_persist_dir: str = "./vectorstore"
    pinecone_api_key: str = ""
    pinecone_environment: str = ""

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # 日志
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """获取配置（单例）"""
    return Settings()

# 使用
settings = get_settings()
print(f"使用模型: {settings.openai_model}")
