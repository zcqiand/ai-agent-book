from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

# 初始化 LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# 初始化搜索工具
search = DuckDuckGoSearchAPIWrapper()

# 定义多个搜索任务
def search_news(query, source):
    """模拟从不同新闻源搜索"""
    results = search.run(f"{query} site:{source}")
    return f"[{source}] {results[:200]}..."

# 并行执行多个搜索
parallel_search = RunnableParallel(
    zhihu=lambda: search_news("AI大模型最新进展", "zhihu.com"),
    twitter=lambda: search_news("AI大模型最新进展", "twitter.com"),
    news=lambda: search_news("AI大模型最新进展", "news.google.com"),
)

# 执行并行搜索
results = parallel_search.invoke({})

# 汇总结果
summary_prompt = f"""请根据以下多源搜索结果，生成一份简洁的摘要：

{results['zhihu']}

{results['twitter']}

{results['news']}
"""

summary = llm.invoke(summary_prompt)
print(summary.content)
