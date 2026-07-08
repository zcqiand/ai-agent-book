from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

@tool
def search(query: str) -> str:
    """搜索信息。"""
    return f"搜索结果: {query}"

tools = [search]

# ReAct Prompt 模板
react_prompt = ChatPromptTemplate.from_template(
    """你是一个助手。使用以下工具回答问题。

    可用工具：
    {tools}

    问题：{input}

    思考你的下一步行动，执行后继续...
    """
)

# 手动 ReAct 循环
def run_react_loop(input_text, max_iterations=5):
    """手动运行 ReAct 循环"""
    current_input = input_text
    iteration = 0

    while iteration < max_iterations:
        # 1. Think - 让 LLM 决定行动
        response = llm.invoke(react_prompt.format(
            tools=[t.name for t in tools],
            input=current_input
        ))

        # 2. Act - 解析并执行工具调用
        # 这里简化了，实际需要解析 tool_call
        if "search" in response.content.lower():
            result = search.invoke({"query": "AI最新进展"})
            current_input = f"工具返回: {result}\n请继续回答原问题"
        else:
            return response.content

        iteration += 1

    return "达到最大迭代次数"

# 运行
result = run_react_loop("AI的最新发展动态是什么？")
print(result)