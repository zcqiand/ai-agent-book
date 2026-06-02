from agents import Agent, handoff
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.agents import Tool
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

# 1. 初始化
llm = ChatOpenAI(model="gpt-4", temperature=0)
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(persist_directory="./vector_db", embedding=embeddings)

# 2. 定义工具
def query_leave(employee_id: str) -> str:
    """查询请假余额"""
    return f"员工{employee_id}剩余年假10天"

leave_tool = Tool(name="查询请假", func=query_leave, description="查询员工请假余额")

# 3. 定义各个 Agent
rag_agent = Agent(
    name="rag_agent",
    instructions="从知识库检索相关信息并回答问题。",
    tools=[],
)

tool_agent = Agent(
    name="tool_agent",
    instructions="调用内部工具获取实时数据。",
    tools=[leave_tool],
)

general_agent = Agent(
    name="general_agent",
    instructions="用友好专业的语气回答一般性问题。",
)

# 4. 路由 Agent
router = Agent(
    name="router",
    instructions="""分析用户问题类型并转交：
    - 知识性问题 → rag_agent
    - 需要查数据 → tool_agent
    - 闲聊/一般问题 → general_agent""",
    handoffs=[rag_agent, tool_agent, general_agent],
)

# 5. 主循环
def run_assistant(user_input: str):
    """运行助手"""
    messages = []

    # 路由
    response = router.run(user_input)

    # 如果需要 RAG，先检索再生成
    if response.requires_rag:
        docs = vectorstore.similarity_search(user_input, k=5)
        context = "\n".join([doc.page_content for doc in docs])
        prompt = f"根据以下内容回答问题：\n{context}\n\n问题：{user_input}"
        result = llm.invoke(prompt)
    else:
        result = response.content

    return result

# 示例运行
if __name__ == "__main__":
    result = run_assistant("我想查一下我的年假还剩多少天")
    print(result)