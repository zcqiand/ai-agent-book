from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 工具
@tool
def search_homework(topic: str) -> str:
    """查询学生作业情况。"""
    return f"作业: 关于{topic}的数学作业已完成批改"

# 短期记忆由 create_agent 的 messages 状态承载
agent = create_agent(
    model=llm,
    tools=[search_homework],
    system_prompt=(
        "你是班级助手，能记住学生的姓名、班级和历史交互。"
        "对话历史会自动累积在你的 messages 状态中。"
    ),
    debug=True,
)

# 运行示例：手动累积 messages 演示多轮记忆
messages = []

def chat(user_input: str) -> str:
    messages.append({"role": "user", "content": user_input})
    result = agent.invoke({"messages": messages})
    reply = result["messages"][-1].content
    messages.append({"role": "assistant", "content": reply})
    return reply

print(chat("我是李明，班级初一(2)班"))
print(chat("我的数学作业完成情况如何？"))
print(chat("我是谁？记住我叫什么名字？"))  # 能从 messages 历史里答出"李明"