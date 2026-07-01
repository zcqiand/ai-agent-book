from typing import TypedDict, List

class AgentState(TypedDict):
    """Agent 执行过程中的状态"""
    messages: List[str]  # 对话历史
    current_step: str   # 当前步骤
    context: dict        # 上下文信息
    result: str          # 最终结果
