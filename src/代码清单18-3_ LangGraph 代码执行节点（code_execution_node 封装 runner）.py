import os
import functools

# 复用代码清单18-1的 runner 和代码清单18-2的资源限制器
# from sandbox_runner import run_isolated
# from resource_limiter import apply_resource_limits


def _wrap_with_limits(code, timeout):
    """把 resource 限制注入到子进程内部：在 snippet.py 头部插入设限调用。

    resource.setrlimit 只对调用它的进程生效，所以把 apply_resource_limits
    拼接到 snippet.py 开头，让它在子进程里执行（Windows 上自动兜底跳过）。
    """
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    return (
        "import sys; sys.path.insert(0, {pkg_dir!r})\n"
        "from resource_limiter import apply_resource_limits\n"
        "apply_resource_limits(cpu_seconds={timeout}, memory_mb=256, file_size_mb=10)\n"
        "\n"
        "{code}\n"
    ).format(pkg_dir=pkg_dir, timeout=timeout, code=code)


def execute_code(state, timeout=10, enforce_resource_limits=False):
    """LangGraph 节点：在隔离沙箱里执行 state['code']，回流执行结果。

    返回的是 partial state（部分状态字典）——只含本节点负责的字段。
    LangGraph 框架会把它浅合并回全局 state，这是『节点返回 partial state』契约。
    """
    code = state["code"]
    if enforce_resource_limits:
        snippet = _wrap_with_limits(code, timeout=timeout)
    else:
        snippet = code

    # 核心调用：subprocess 进程隔离 + 超时强制 + 干净 env（详见代码清单18-1）
    result = run_isolated(snippet, timeout=timeout)

    # 只回流本节点产出的字段——partial state 契约。
    return {
        "code_result": result["code_result"],
        "code_error": result["code_error"],
        "exit_code": result["exit_code"],
    }


# 用 functools.partial 绑定配置，得到一个『带默认超时的节点函数』——
# 节点本身是无状态的纯函数，配置通过 partial 注入（承接第5章纯函数节点设计）。
execute_code_strict = functools.partial(
    execute_code, timeout=5, enforce_resource_limits=True
)