from agents import Agent
from agents.hitl import pause, approve, reject

# 创建 Agent
transaction_agent = Agent(
    name="transaction_agent",
    instructions="""你是一个交易助手。处理用户的转账请求。

    流程：
    1. 分析转账请求
    2. 调用 pause() 暂停，等待批准
    3. 根据用户反馈执行或取消

    转账金额超过10000时必须暂停等待批准。""",
)

# 处理转账
def handle_transfer(from_account: str, to_account: str, amount: float):
    """处理转账请求"""
    if amount > 10000:
        # 大额转账需要批准
        result = transaction_agent.run(
            f"从 {from_account} 转账 {amount} 元到 {to_account}"
        )
        # 等待用户批准...
        return result
    else:
        # 小额直接执行
        return execute_transfer(from_account, to_account, amount)
