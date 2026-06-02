from agents import Agent, handoff

# 定义带有上下文收集的 Agent
collector = Agent(
    name="info_collector",
    instructions="收集用户的基本信息：姓名、联系方式、问题类型。收集完成后转交给专家处理。",
)

def create_specialist_handoff(specialist_type: str):
    """创建一个携带上下文信息的 Handoff"""
    specialist = Agent(
        name=f"{specialist_type}_specialist",
        instructions=f"你是{specialist_type}专家，处理用户的问题。",
    )
    return handoff(
        specialist,
        context={
            "transferred_from": "info_collector",
            "specialist_type": specialist_type,
        }
    )

# 运行
response = collector.run("我叫张三，电话138xxxx，技术问题")
# 自动转交给技术专家，并携带用户信息上下文