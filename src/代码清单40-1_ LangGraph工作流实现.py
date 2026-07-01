from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, List, Optional
from datetime import datetime
from pydantic import BaseModel

class WorkflowState(TypedDict):
    """工作流状态"""
    workflow_id: str
    current_step: str
    payload: dict              # 工作流输入数据
    context: dict              # 执行过程中的数据
    results: dict              # 各步骤的执行结果
    errors: List[str]          # 错误记录
    started_at: str            # 开始时间
    updated_at: str            # 更新时间

class WorkflowDefinition:
    """工作流定义"""

    def __init__(self, workflow_id: str, name: str):
        self.workflow_id = workflow_id
        self.name = name
        self.steps: List[dict] = []
        self.graph = None

    def add_step(
        self,
        step_id: str,
        handler: callable,
        next_step: Optional[str] = None,
        error_handler: Optional[str] = None
    ):
        """添加工作流步骤"""
        self.steps.append({
            "step_id": step_id,
            "handler": handler,
            "next_step": next_step,
            "error_handler": error_handler
        })

    def build(self):
        """构建工作流图"""
        workflow = StateGraph(WorkflowState)

        # 添加节点
        for step in self.steps:
            workflow.add_node(step["step_id"], step["handler"])

        # 添加边
        for i, step in enumerate(self.steps[:-1]):
            next_step = self.steps[i + 1]["step_id"]
            workflow.add_edge(step["step_id"], next_step)

        workflow.set_entry_point(self.steps[0]["step_id"])
        workflow.set_finish_point(self.steps[-1]["step_id"])

        self.graph = workflow.compile()
        return self.graph
