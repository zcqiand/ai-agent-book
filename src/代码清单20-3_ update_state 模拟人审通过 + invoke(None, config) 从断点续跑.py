# 复用代码清单20-1 的 build_graph
# from listing_20_1 import build_graph
# from langgraph.checkpoint.memory import MemorySaver


def main():
    saver = MemorySaver()
    graph = build_graph(saver)
    config = {"configurable": {"thread_id": "demo-001"}}

    # 第一步：跟代码清单20-2 一样，先 invoke 到 human_review 之前暂停
    init_state = {"user_input": "帮我把退款链接发给张三", "generated_content": "", "approved": False}
    graph.invoke(init_state, config)
    print("=== 暂停时 ===")
    print("snapshot.next:", graph.get_state(config).next)
    print("approved:", graph.get_state(config).values.get("approved"))

    # 第二步：模拟人审通过——用 update_state 把 approved 写回 True。
    # update_state 是 LangGraph 提供的「外部写回 state」的 API：
    # 不经过节点、直接把 partial state 合并进 checkpointer 落盘的最新快照。
    # 真实生产场景里，人审这一步是由外部人审系统（Web 审批台 / IM 审批机器人）调用 update_state 完成——
    # 节点函数 human_review 在生产里通常不需要再写一遍 approved=True，因为它代表的是「人工动作」而非「图内逻辑」。
    graph.update_state(config, {"approved": True})
    print("\n=== update_state 写回人审结果后 ===")
    print("approved:", graph.get_state(config).values.get("approved"))

    # 第三步：从断点续跑——invoke(None, config)。
    # 第一参 None 是 LangGraph 的「续跑协议」：表示「不喂新输入，从 checkpointer 落盘的断点继续跑后半段」。
    # 此刻断点在 human_review 之前，所以这一句会把 human_review → execute → END 这后半段跑完。
    # 如果第一参传一个完整 state，会被当成新输入重新跑一遍图，那就不是「续跑」了——这是读者最易踩的坑。
    result = graph.invoke(None, config)
    print("\n=== invoke(None, config) 续跑后 ===")
    print("generated_content:", result.get("generated_content"))
    print("approved:", result.get("approved"))

    # 续跑完毕的判据：snapshot.next 变成空元组 ()——已到 END，没有待执行的节点了
    snapshot = graph.get_state(config)
    print("snapshot.next:", snapshot.next)


if __name__ == "__main__":
    main()