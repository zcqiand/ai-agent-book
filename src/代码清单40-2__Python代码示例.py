from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.memory import MemorySaver
import json
from pathlib import Path

class WorkflowStateManager:
    """工作流状态管理器"""

    def __init__(self, storage_path: str = "./workflow_state"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # 使用 SQLite 进行持久化存储
        self.checkpointer = SqliteSaver.from_conn_string(
            str(self.storage_path / "workflows.db")
        )

    def save_state(self, workflow_id: str, state: dict):
        """保存工作流状态"""
        state_file = self.storage_path / f"{workflow_id}.json"
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def load_state(self, workflow_id: str) -> Optional[dict]:
        """加载工作流状态"""
        state_file = self.storage_path / f"{workflow_id}.json"
        if not state_file.exists():
            return None

        with open(state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_workflows(self, status: str = None) -> List[dict]:
        """列出所有工作流"""
        workflows = []
        for state_file in self.storage_path.glob("*.json"):
            with open(state_file, "r", encoding="utf-8") as f:
                wf = json.load(f)
                if status is None or wf.get("status") == status:
                    workflows.append(wf)
        return workflows

    def delete_workflow(self, workflow_id: str):
        """删除工作流状态"""
        state_file = self.storage_path / f"{workflow_id}.json"
        if state_file.exists():
            state_file.unlink()