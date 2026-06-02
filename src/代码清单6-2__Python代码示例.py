from agents import Agent
from openai_tools import function

@function
def search_product(query: str) -> str:
    """搜索产品信息"""
    # 实际应用中这里会调用产品数据库或搜索API
    products = {
        "ai助手": "AI助手是一款智能对话产品，支持多模态交互",
        "代码助手": "代码助手专注于编程辅助，支持多种语言",
    }
    return products.get(query, "未找到相关产品")

# 创建带工具的 Agent
product_assistant = Agent(
    name="product_assistant",
    instructions="你是一个专业的产品顾问。当用户询问产品信息时，使用搜索工具查找相关产品信息并给出准确回答。如果搜索不到相关信息，诚实地告诉用户你无法找到该产品。",
    tools=[search_product],
)

# 运行
response = product_assistant.run("你们有AI助手吗？")
print(response)