
# 注意：本示例使用 OpenAI Agents SDK 1.x 版本
from agents import Agent, Runner, handoff
from openai import OpenAI

# 初始化OpenAI客户端（实际项目中应注入）
# 假设 tools 已在前面章节（第17章）定义
# order_query_tool 和 logistics_tool 是模拟的工具名称

# 定义订单Agent
order_agent = Agent(
    name="订单查询员",
    instructions="""你是一名订单查询专家。
当用户询问订单状态、订单详情等问题时，使用订单查询工具回答。
如果用户的问题不属于订单范畴，请调用handoff转交给相关Agent。""",
    tools=["order_query_tool"]  # 工具名，实际项目需完整定义
)

# 定义物流Agent
logistics_agent = Agent(
    name="物流分析师",
    instructions="""你是一名物流分析专家。
根据订单信息，分析最优物流方案。
考虑送达时间、运费、仓库位置等因素。""",
    tools=["logistics_tool"]  # 工具名，实际项目需完整定义
)

# 定义总控Agent，带handoffs
triage_agent = Agent(
    name="总控",
    instructions="""你是一个客服总控Agent。
分析用户意图，将请求转交给最合适的专员Agent。
使用handoff函数进行转交。""",
    handoffs=[
        handoff(order_agent, name="订单专员"),
        handoff(logistics_agent, name="物流专员")
    ]
)

# 运行示例
def demo_handoffs():
    """演示Handoffs机制"""
    result = Runner.run_sync(
        starting_agent=triage_agent,
        input="我想查一下订单A12345的物流情况"
    )
    print(result.final_output)

## 36.4　实战练习：角色定义文档

本节练习要求你为一个多智能体客服系统编写完整的角色定义文档。

**练习目标：** 掌握多智能体系统的角色设计方法：
1. 定义系统边界和职责分工
2. 编写每个角色的规范文档
3. 设计智能体间的通信协议

**参考模板：**