import os

# 设置 API Key
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "my-agent-project"  # 项目名称

# 可选：设置端点（如果你使用自托管）
# os.environ["LANGCHAIN_ENDPOINT"] = "http://localhost:8000"
