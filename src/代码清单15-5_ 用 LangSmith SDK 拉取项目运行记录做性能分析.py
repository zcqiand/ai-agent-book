from langsmith import Client  # langsmith 是独立包，1.x 不变

client = Client()

# 拉取项目最近的运行记录（list_runs，不是 list_examples——后者是数据集示例）
# 注意只有最外层 run 是 root run；想看每次 invoke 的顶层轨迹，加 is_root=True
project_runs = client.list_runs(
    project_name="my-agent-project",
    limit=10,
    is_root=True,
)

for run in project_runs:
    print(f"Run ID: {run.id}")
    # Run 对象上 latency / token 都是直接属性，没有 .stats 子对象
    print(f"执行时间: {run.total_latency_ms:.0f}ms" if run.total_latency_ms else "执行时间: N/A")
    total_tokens = (run.prompt_tokens or 0) + (run.completion_tokens or 0)
    print(f"Token消耗: {total_tokens}")
    if run.error:
        print(f"错误: {run.error}")
    print("-" * 50)