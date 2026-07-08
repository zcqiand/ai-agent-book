import tempfile

from langgraph.checkpoint.sqlite import SqliteSaver

# 复用代码清单19-1 的 DemoState / echo_node
# from listing_19_1 import DemoState, echo_node


def build_graph():
    """与代码清单19-1 同构，留出 compile 时挂 checkpointer 的位置。"""
    graph_builder = StateGraph(DemoState)
    graph_builder.add_node("echo", echo_node)
    graph_builder.add_edge(START, "echo")
    graph_builder.add_edge("echo", END)
    return graph_builder


def main():
    tmp_dir = tempfile.mkdtemp(prefix="ch19_")
    db_path = f"{tmp_dir}/checkpoints.db"

    # 用 with 进 from_conn_string 的上下文，saver 在整个 with 块内有效
    with SqliteSaver.from_conn_string(db_path) as saver:
        graph = build_graph().compile(checkpointer=saver)

        # 同一个 thread_id 贯穿两次 invoke——这是「跨 invoke 续跑」的关键
        config = {"configurable": {"thread_id": "demo-001"}}

        # === 第一次 invoke：喂初始 state，落盘 ===
        print("=== 第一次 invoke ===")
        first_state = {
            "messages": [HumanMessage(content="你好")],
            "user_input": "你好",
            "turn_count": 0,
        }
        result1 = graph.invoke(first_state, config)
        print("turn_count:", result1["turn_count"])
        print("messages 长度:", len(result1["messages"]))

        # get_state 读回 checkpointer 落盘的最新快照——验证「状态真的存下来了」
        # snapshot.values 是当前状态值，snapshot.next 表示下一步要执行的节点（空元组=已到 END）
        snapshot = graph.get_state(config)
        print("checkpoint 里的 turn_count:", snapshot.values.get("turn_count"))

        # === 第二次 invoke：同 thread_id + 新消息，自动读回上次状态续跑 ===
        print("\n=== 第二次 invoke（同 thread_id）===")
        second_input = {
            "messages": [HumanMessage(content="再问一句")],
            "user_input": "再问一句",
            # 注意：这里没传 turn_count——checkpointer 会从上次快照读回 turn_count=1
        }
        result2 = graph.invoke(second_input, config)

        # 续跑效果：messages 在第一次的 2 条基础上累加到 4，turn_count 从 1 累加到 2
        # 如果 checkpointer 没生效，第二次 invoke 会从空 state 起步、turn_count 重置成 1
        print("turn_count:", result2["turn_count"])
        print("messages 长度:", len(result2["messages"]))
        print("第3条:", result2["messages"][2].content)
        print("第4条:", result2["messages"][3].content)


if __name__ == "__main__":
    main()