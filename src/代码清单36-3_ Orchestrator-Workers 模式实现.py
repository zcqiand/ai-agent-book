from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import JsonOutputParser

class Orchestrator:
    """任务编排器"""

    def __init__(self, workers: dict):
        self.workers = workers  # {"角色名": agent实例}
        self.llm = ChatOpenAI(model="gpt-4")

    def decompose_task(self, user_query: str) -> list:
        """将用户任务分解为子任务"""
        prompt = ChatPromptTemplate.from_template(
            """分析用户查询，将其分解为可并行执行的子任务。

用户查询：{query}

请输出JSON格式的子任务列表，每个子任务包含：
- task_id: 任务ID
- task_type: 任务类型（order_query/logistics/decision/notification）
- description: 任务描述
- assigned_to: 分配的worker角色

只输出JSON，不要有其他文字。"""
        )
        parser = JsonOutputParser()
        chain = prompt | self.llm | parser
        subtasks = chain.invoke({"query": user_query})
        return subtasks

    def execute_subtask(self, subtask: dict, context: dict) -> dict:
        """执行单个子任务"""
        worker_name = subtask["assigned_to"]
        worker = self.workers.get(worker_name)

        if not worker:
            return {"status": "error", "message": f"Unknown worker: {worker_name}"}

        # 调用worker执行
        result = worker.run(
            task_description=subtask["description"],
            context=context
        )
        return {"task_id": subtask["task_id"], "status": "success", "result": result}

    def aggregate_results(self, subtask_results: list, original_query: str) -> str:
        """聚合子任务结果"""
        results_text = "\n".join([
            f"任务{i+1}结果：{r.get('result', r.get('message', 'N/A'))}"
            for i, r in enumerate(subtask_results)
        ])

        prompt = ChatPromptTemplate.from_template(
            """根据以下子任务结果，回答用户的原始问题。

原始问题：{query}

子任务结果：
{results}

请综合分析这些结果，给出完整的回答。如果某个子任务失败，请在回答中说明。"""
        )
        chain = prompt | self.llm
        final_response = chain.invoke({
            "query": original_query,
            "results": results_text
        })
        return final_response.content

# 使用示例
def demo_orchestrator():
    """演示Orchestrator-Workers模式"""
    # 创建Workers
    workers = {
        "order_query": OrderQueryWorker(),
        "logistics": LogisticsWorker(),
        "decision": DecisionWorker()
    }

    # 创建Orchestrator
    orchestrator = Orchestrator(workers)

    # 处理用户请求
    user_query = "我上个月有个订单，订单号A12345，帮我选择最优物流方案"

    # 1. 任务分解
    subtasks = orchestrator.decompose_task(user_query)
    print(f"分解为 {len(subtasks)} 个子任务")

    # 2. 并行执行子任务
    context = {"order_id": "A12345"}
    results = [orchestrator.execute_subtask(task, context) for task in subtasks]

    # 3. 结果聚合
    final_response = orchestrator.aggregate_results(results, user_query)
    print(final_response)

print("Orchestrator-Workers模式实现完成")
