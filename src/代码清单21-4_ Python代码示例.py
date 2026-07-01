from agents import Agent, handoff

# 分析 Agent
analyzer = Agent(
    name="analyzer",
    instructions="分析用户需求，准备广播给多个专家。"
)

# 专家 Agents
tech_expert = Agent(name="tech", instructions="提供技术建议")
market_expert = Agent(name="market", instructions="提供市场建议")
legal_expert = Agent(name="legal", instructions="提供法律建议")

# 主 Agent 协调
coordinator = Agent(
    name="coordinator",
    instructions="""收集多个专家的建议并汇总。

    流程：
    1. 先用 handoff 转交给 analyzer 分析需求
    2. 然后并行咨询 tech、market、legal 专家
    3. 汇总所有建议生成最终报告""",
    handoffs=[analyzer, tech_expert, market_expert, legal_expert]
)
