import tempfile

from langgraph.checkpoint.sqlite import SqliteSaver

# 复用代码清单19-1 的 DemoState 和 echo_node
# from listing_19_1 import DemoState, echo_node


def build_graph_with_checkpointer(db_path: str):
    """编译一张挂了 SqliteSaver 的图，返回 (graph, saver_ctx)。

    关键坑点：SqliteSaver.from_conn_string 是「上下文管理器工厂」，
    返回的是 Iterator[SqliteSaver]（生成器），不是 saver 实例。
    必须用 with 进上下文取出 yield 出来的 saver，直接 return 工厂产物会拿到生成器对象、
    后面一编译就报错。这是读者最易踩的坑，本清单用显式进上下文的写法做正解示范。
    """
    # 进上下文：__enter__ 里打开 sqlite3 连接、yield saver；__exit__ 里关连接。
    saver_ctx = SqliteSaver.from_conn_string(db_path)
    saver = saver_ctx.__enter__()
    try:
        # 编译时挂 checkpointer——这是「两步启用持久化」的第一步
        # （第二步是 invoke 时传 thread_id，见代码清单19-3）
        graph_builder = StateGraph(DemoState)
        graph_builder.add_node("echo", echo_node)
        graph_builder.add_edge(START, "echo")
        graph_builder.add_edge("echo", END)
        graph = graph_builder.compile(checkpointer=saver)
        return graph, saver_ctx
    except Exception:
        # 编译失败要主动退出上下文，否则 sqlite3 连接泄漏
        saver_ctx.__exit__(None, None, None)
        raise


if __name__ == "__main__":
    # 用 tempfile 拿一个临时目录放 db 文件，避免污染仓库工作区
    tmp_dir = tempfile.mkdtemp(prefix="ch19_")
    db_path = f"{tmp_dir}/checkpoints.db"

    graph, saver_ctx = build_graph_with_checkpointer(db_path)

    # thread_id 是持久化主键：同一个 thread_id 的多次 invoke 共享同一份 checkpoint
    # 不同 thread_id 的状态彼此隔离（本章只把 thread_id 当主键，不展开多租户——那是第27章）
    config = {"configurable": {"thread_id": "demo-001"}}

    try:
        init_state = {
            "messages": [HumanMessage(content="第一句")],
            "user_input": "第一句",
            "turn_count": 0,
        }
        # invoke 时传 config（带 thread_id）——「两步启用持久化」的第二步
        result = graph.invoke(init_state, config)
        print("turn_count:", result["turn_count"])
        print("messages 长度:", len(result["messages"]))
    finally:
        # 演示脚本结束前主动关连接，避免 Windows 上文件句柄残留
        saver_ctx.__exit__(None, None, None)