import agents.tracing as tracing

# 获取最近的追踪记录
traces = tracing.list_traces(
    project_name="my-agent-project",
    limit=10
)

for trace in traces:
    print(f"Trace ID: {trace.id}")
    print(f"开始时间: {trace.start_time}")
    print(f"耗时: {trace.duration}")
    print(f"步骤数: {len(trace.spans)}")
    print("-" * 50)

# 查看单个追踪的详细信息
detail = tracing.get_trace(trace_id="your-trace-id")
for span in detail.spans:
    print(f"步骤: {span.name}")
    print(f"  输入: {span.input[:100]}...")
    print(f"  输出: {span.output[:100]}...")
    print(f"  耗时: {span.duration_ms}ms")