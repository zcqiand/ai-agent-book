# 在 code/saas-cs-agent 目录下执行；PYTHONPATH=src 保证可导入包内模块
# PowerShell: $env:PYTHONPATH="src"  bash: export PYTHONPATH=src
#
# 脚本自包含（内联 FakeLLM，不依赖 API Key），一次跑通：invoke 客服请求 →
# list_history 看 checkpoint 链（验证 >=2 快照、最新在前）→ 挑最早 checkpoint_id →
# fork_from 用新输入分叉 → 验证原 thread 不变、fork thread 走新输入（承接 ch27 隔离）。
from saas_cs_agent.checkpoint import make_checkpointer, close_all
from saas_cs_agent.graph import build_graph
from saas_cs_agent.time_travel import list_history, fork_from


class FakeLLM:
    """最小 LLM 替身：llm.generate(prompt) 返回固定字符串。

    内联而非引入包内 FakeLLM，是为了让脚本复制即跑、不耦合测试构造。返回值
    'password_reset' 恰好命中 nodes.py 迷你知识库的键，让 retrieve_kb 真正追加一条
    片段，使整条 checkpoint 链留下多个节点痕迹（满足 list_history >=2）。
    """

    def generate(self, prompt: str) -> str:
        return "password_reset"


# 1) 建 checkpointer（默认 SqliteSaver，ch26 讲过保活连接，此处不展开）。
checkpointer = make_checkpointer()

# 2) 装配图：compile 绑 checkpointer + interrupt_before=['human_review']。
#    图在 compose_reply 后、human_review 之前真暂停，每个节点执行后落一次盘，
#    形成一条 checkpoint 链（一个 thread_id 对应一条链）。
graph = build_graph(checkpointer, FakeLLM())

# thread_id 是持久化主键，不同 thread_id 互相隔离（ch27）。
config = {"configurable": {"thread_id": "demo-001"}}

# 最简 CSState 五字段（state.py）。
initial_state = {
    "messages": [{"role": "user", "content": "我的账号登不进去，密码好像忘了"}],
    "thread_id": "demo-001",
    "tenant_id": "tenant-acme",
    "intent": "",
    "awaiting_human": False,
}

# 3) 第一次 invoke：三节点各落一次盘，到 human_review 之前真暂停。每个节点执行后
#    那份完整状态串成一条历史链，就是本章要利用的「资产」。
graph.invoke(initial_state, config)

# 4) list_history 看 chain：1.2.x 倒序 yield，list[0] 最新、list[-1] 最早
#    （踩坑点：别按「从早到晚」直觉取 list[0] 当最早）。
history = list_history(graph, "demo-001")
print("历史快照数 =", len(history), "（预期 >=2：每个节点执行后各落一次盘）")
print("从最新(history[0])到最早(history[-1]) 的 checkpoint 链：")
for i, snap in enumerate(history):
    cid = snap.config["configurable"]["checkpoint_id"]  # fork_from 的回溯定位键
    print(f"  [{i}] next={snap.next}  checkpoint_id={cid}")

# 5) 挑 history[-1]（最早快照）作 fork 起点——相当于「从对话起点重新分叉」。
early_checkpoint_id = history[-1].config["configurable"]["checkpoint_id"]
print("挑 fork 起点（history[-1]，最早）checkpoint_id =", early_checkpoint_id)

# 6) fork_from 用新输入分叉：config 同时带 checkpoint_id（从哪起）和 fork_thread_id
#    （在独立 thread 上跑）。靠 ch27 立的隔离边界，新轨迹与原 thread 互不可见。
new_input = {
    "messages": [{"role": "user", "content": "我的账单在哪里查？"}],
    "thread_id": "demo-001-fork1",
    "tenant_id": "tenant-acme",
    "intent": "",
    "awaiting_human": False,
}
fork_from(graph, early_checkpoint_id, new_input, "demo-001-fork1")

# 7) 验证非破坏性（承接 ch27）：原 thread 状态没被 fork 改、fork thread 走了新轨迹。
orig_state = graph.get_state(config)  # 原 thread：config.thread_id='demo-001'
fork_state = graph.get_state(
    {"configurable": {"thread_id": "demo-001-fork1"}}
)

print("\n--- 对照：原 thread vs fork thread ---")
print("原 thread messages[0] =", orig_state.values["messages"][0])
print("fork thread messages[0] =", fork_state.values["messages"][0])

# 原 thread 的初始消息没变（fork 没污染它）；fork thread 走了新输入。
assert orig_state.values["messages"][0]["content"] == "我的账号登不进去，密码好像忘了", \
    "原 thread 被污染：fork 后 messages[0] 不该变"
assert fork_state.values["messages"][0]["content"] == "我的账单在哪里查？", \
    "fork thread 未走新输入：messages[0] 应是 new_input 的内容"
print("\n非破坏性 OK：原 thread 状态不变，fork thread 走了新轨迹（隔离承接 ch27）")

# 测试进程短，可省略 close_all；长驻进程优雅停机时应调用以释放底层连接。
close_all()