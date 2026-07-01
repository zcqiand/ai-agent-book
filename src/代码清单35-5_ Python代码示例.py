from langsmith import traceable
from langchain_openai import ChatOpenAI
from langchain.callbacks.tracers import LangChainTracer
from langchain.callbacks.manager import CallbackManager
import os

# 设置 LangSmith 环境变量
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "rag-production"

# 创建带追踪的 LLM
llm = ChatOpenAI(
    model="gpt-4",
    callback_manager=CallbackManager([LangChainTracer()])
)

# 使用 @traceable 装饰追踪函数
@traceable(name="rag_query")
def rag_query(question: str, top_k: int = 5):
    """RAG 查询（自动追踪）"""
    # 1. 检索
    docs = vectorstore.similarity_search(question, k=top_k)

    # 2. 构建上下文
    context = "\n\n".join([doc.page_content for doc in docs])

    # 3. 生成回答
    response = llm.invoke(f"上下文:\n{context}\n\n问题: {question}")

    return {
        "answer": response.content,
        "sources": docs
    }

# 使用
result = rag_query("公司的年假政策是什么？")
