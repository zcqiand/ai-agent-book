from langsmith import Client

client = Client()

# 获取项目的运行统计
project_runs = client.list_examples(
    project_name="my-agent-project",
    limit=10
)

for run in project_runs:
    print(f"Run ID: {run.id}")
    print(f"执行时间: {run.stats.latency_ms}ms")
    print(f"Token消耗: {run.stats.total_tokens}")
    if run.error:
        print(f"错误: {run.error}")
    print("-" * 50)
