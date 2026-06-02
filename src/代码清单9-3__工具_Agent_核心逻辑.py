from langchain.agents import Tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

def query_leave_balance(employee_id):
    """查询请假余额"""
    # 实际会调用内部HR系统API
    return f"员工{employee_id}年假余额：10天，病假余额：5天"

leave_tool = Tool(
    name="查询请假余额",
    func=query_leave_balance,
    description="查询员工的请假余额，输入员工ID"
)

tools = [leave_tool]