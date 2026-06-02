from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 新闻摘要 Prompt
summarize_prompt = ChatPromptTemplate.from_template(
    "请将以下新闻内容摘要为100字以内：\n\n{content}"
)

# 综合报告 Prompt
synthesize_prompt = ChatPromptTemplate.from_template(
    "请将以下多条新闻摘要综合成一篇简洁的报告：\n\n{summaries}"
)

# 定义多个新闻源的处理
def create_news_chain(source_name, search_func):
    """为每个新闻源创建处理链"""
    return (
        ChatPromptTemplate.from_template(
            f"从{source_name}获取关于{{topic}}的新闻，并摘要关键信息"
        )
        | llm
        | (lambda x: f"【{source_name}】{x.content}")
    )

# 并行获取多个来源的新闻
news_parallel = RunnableParallel(
    zhihu=create_news_chain("知乎", None),
    twitter=create_news_chain("Twitter", None),
    news=create_news_chain("新闻", None),
)

# 最终综合链
synthesis_chain = synthesize_prompt | llm

# 完整 Chain
full_chain = (
    {"topic": RunnablePassthrough()}
    | {
        "summaries": news_parallel
    }
    | synthesis_chain
)

# 运行
result = full_chain.invoke("AI大模型最新进展")
print(result.content)