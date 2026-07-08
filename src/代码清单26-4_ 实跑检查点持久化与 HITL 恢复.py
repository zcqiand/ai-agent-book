# 在 code/saas-cs-agent 目录下执行；PYTHONPATH=src 保证可导入包内模块
# PowerShell 写法：$env:PYTHONPATH="src"；bash 写法：export PYTHONPATH=src
#
# 脚本自包含：内联一个最小 FakeLLM（llm.generate 接口），让脚本不依赖真实 API Key 即可跑通
# 「invoke → 在 human_review 前暂停 → invoke(None, config) 从断点续跑到 END」全流程。
from saas_cs_agent.checkpoint import make_checkpointer, close_all
from saas_cs_agent.graph import build_graph


class FakeLLM:
    """最小 LLM 替身：llm.generate(prompt) 返回固定字符串。

    为什么内联而不引入包内 FakeLLM：让脚本复制即跑，不耦合包内测试构造。
    客服图的 classify_intent / compose_reply 只要求 llm.generate(string) -> string。
    """

    def generate(self, prompt: str) -> str:
        return "已查到您的订单状态：在途，预计 2 天内送达。"


# 1) 建 checkpointer——默认走 SqliteSaver（langgraph-checkpoint-sqlite），
#    底层 SQLite 文件默认 checkpoints.db；make_checkpointer 已用进程级 ExitStack 保活连接。
checkpointer = make_checkpointer()

# 2) 装配图：build_graph 把 checkpointer 与 interrupt_before=['human_review'] 绑进 compile，
#    图执行到 human_review 之前会真暂停、把状态落盘到 checkpointer（按 thread_id 存取）。
graph = build_graph(checkpointer, FakeLLM())

# thread_id 是 checkpointer 的持久化主键 / 对话线程唯一键——
# 同 thread_id 的多次 invoke 共享一份 checkpoint 历史，不同 thread_id 互相隔离。
config = {"configurable": {"thread_id": "demo-001"}}

# 最简 CSState 五字段（state.py）——多轮对话特有字段 thread_id / awaiting_human 都给初值。
initial_state = {
    "messages": [{"role": "user", "content": "我的订单还没到，帮我查一下"}],
    "thread_id": "demo-001",
    "tenant_id": "tenant-acme",
    "intent": "",
    "awaiting_human": False,
}

# 3) 第一次 invoke：跑到 human_review 之前因 interrupt_before 真暂停，不出 END。
#    compose_reply 已生成回复并落盘，但 human_review 尚未执行——等人放行。
result = graph.invoke(initial_state, config)
print("第一次 invoke 后 awaiting_human =", result["awaiting_human"])

# 用 graph.get_state(config) 看下一步是哪个节点——预期停在 human_review 之前。
# snapshot.next 才是判断暂停的权威信号：指向 human_review 即表示在等人放行。
# 注意 awaiting_human 在本仓未被任何节点置 True，暂停时仍为初值 False，不可用它判暂停。
snapshot = graph.get_state(config)
print("当前中断点 next =", snapshot.next)  # 预期 ('human_review',)

# 4) 第二次 invoke(None, config)：第一参 None=不喂新输入、从断点继续——
#    human_review 执行 → END，整张图走完。这是 interrupt_before 的恢复语义（resume）。
final = graph.invoke(None, config)
print("第二次 invoke 后 next =", graph.get_state(config).next)  # 预期 ()，已到 END

# 测试进程短，可省略 close_all；长驻进程优雅停机时应调用以释放底层连接。
close_all()