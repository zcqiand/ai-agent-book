from typing import TypedDict

from langgraph.graph import StateGraph, START, END

# from code_listing_18_3 import execute_code  # 节点函数来自代码清单18-3


class SandboxState(TypedDict):
    """沙箱执行节点的状态契约。

    四个字段的分工：
    - code：待执行代码（输入，由上游节点或 invoke 提供）
    - code_result：标准输出（输出，节点写入）
    - code_error：错误输出（输出，节点写入）
    - exit_code：退出码（输出；0=正常，-1=超时，>0=子进程异常退出）
    """
    code: str
    code_result: str
    code_error: str
    exit_code: int


def build_sandbox_graph(timeout=10):
    """组装一个『START → execute_code → END』的最小 StateGraph。"""
    graph = StateGraph(SandboxState)
    graph.add_node("execute_code", lambda state: execute_code(state, timeout=timeout))
    graph.add_edge(START, "execute_code")
    graph.add_edge("execute_code", END)
    return graph.compile()


if __name__ == "__main__":
    app = build_sandbox_graph(timeout=10)

    # 演示一：正常执行 print(1+1)
    print("正常路径：", app.invoke({"code": "print(1 + 1)"}))
    # 输出: {'code': 'print(1 + 1)', 'code_result': '2\n', 'code_error': '', 'exit_code': 0}

    # 演示二：执行报错的代码——主进程不会崩，错误被封进 code_error 回流
    print("异常路径：", app.invoke({"code": "raise ValueError('demo')"}))
    # 输出: {'code': "raise ValueError('demo')", 'code_result': '', 'code_error': 'Traceback ...', 'exit_code': 1}