# 复用代码清单20-1 的 HitlState、generate、human_review、execute、build_graph
# from listing_20_1 import build_graph
# from langgraph.checkpoint.memory import MemorySaver


def main():
    saver = MemorySaver()
    graph = build_graph(saver)

    # thread_id 是持久化主键——同一 thread_id 多次 invoke 共享同一份 checkpoint
    # HITL 场景下它扮演第三层角色：人审结果写回 + 续跑都要靠它定位到「这条暂停了的对话」
    config = {"configurable": {"thread_id": "demo-001"}}

    # 初始 state：approved=False 是初值，generate 会填 generated_content
    init_state = {"user_input": "帮我把退款链接发给张三", "generated_content": "", "approved": False}

    # 第一次 invoke：从 START 跑到 human_review 之前真暂停
    # 关键：暂停发生在 human_review 节点之前（节点尚未执行），不是「跑到 END 后返回」——
    # 这正是 interrupt_before 的语义。invoke 此时返回的是「暂停时的中间状态」，不是最终状态。
    result = graph.invoke(init_state, config)
    print("=== invoke 后立刻看 invoke 的返回值（中间状态）===")
    print("generated_content:", result.get("generated_content"))
    print("approved:", result.get("approved"))

    # 判暂停的权威信号：graph.get_state(config).next
    # snapshot.next 是「下一步要执行的节点」元组——
    #   ('human_review',)  = 停在 human_review 之前，待放行
    #   ()                 = 已到 END，图跑完了
    snapshot = graph.get_state(config)
    print("\n=== get_state 读回 checkpointer 落盘的最新快照 ===")
    print("snapshot.next:", snapshot.next)
    print("snapshot.values.generated_content:", snapshot.values.get("generated_content"))
    print("snapshot.values.approved:", snapshot.values.get("approved"))

    # 为什么不能拿 approved 判暂停：
    # 暂停这一刻 approved 还是初值 False——因为它要等 human_review 节点跑过才会变 True，
    # 而我们恰恰是暂停在 human_review 之前、human_review 还没跑。
    # 所以 approved=False 既可能是「暂停中」也可能是「图根本没建好」——歧义。
    # snapshot.next 没有歧义：它直接告诉你是停在哪个节点之前。这是 HITL 判暂停的唯一定义。


if __name__ == "__main__":
    main()