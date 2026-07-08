import os
import sys
import shutil
import tempfile
import subprocess


# 白名单只保留子进程真正需要的几个变量——刻意不带 API_KEY / SECRET_TOKEN 这类
# 业务侧常用来注入密钥的环境变量，避免子进程把主进程的密钥『顺手读走』。
_ENV_WHITELIST = ("PATH", "PYTHONPATH", "LANG", "LC_ALL", "HOME", "SYSTEMROOT", "TEMP")


def _clean_env():
    """从 os.environ 抽出白名单变量的子集，作为子进程的环境变量。"""
    # 直接传 os.environ 会让子进程继承主进程全部变量（含 API_KEY 等），
    # 这里做最小化白名单，是『最小权限原则』在环境变量维度的体现。
    return {k: os.environ[k] for k in _ENV_WHITELIST if k in os.environ}


def run_isolated(code, timeout=10, workdir=None):
    """在独立子进程里执行一段 Python 代码，返回 dict（含 stdout/stderr/exit_code）。

    设计思路：把『执行不受信代码』当作一次有界的子进程调用——子进程崩溃、超时、
    OOM 都不会波及主进程。这是用 Python 标准库能做到的最便宜的进程级隔离。
    """
    # 没有显式 workdir 就开一个临时目录；子进程的 cwd 被钉在这里，
    # 它的相对路径读写都被限制在这个目录下（文件系统维度的『划片』）。
    own_tmpdir = workdir is None
    if own_tmpdir:
        workdir = tempfile.mkdtemp(prefix="sandbox_")

    snippet_path = os.path.join(workdir, "snippet.py")
    try:
        # 用 utf-8 显式编码，避免 Windows 默认 GBK 导致中文源码乱码。
        with open(snippet_path, "w", encoding="utf-8") as f:
            f.write(code)

        try:
            # sys.executable 是当前解释器的绝对路径——不用字符串 'python'，
            # 避免子进程被 PATH 上的同名恶意可执行文件『狸猫换太子』。
            result = subprocess.run(
                [sys.executable, snippet_path],
                timeout=timeout,
                capture_output=True,
                cwd=workdir,
                env=_clean_env(),
                encoding="utf-8",
                text=True,
            )
            return {
                "code_result": result.stdout or "",
                "code_error": result.stderr or "",
                "exit_code": result.returncode,
            }
        except subprocess.TimeoutExpired as e:
            # subprocess.run 在 timeout 触发时会自动 kill 子进程，
            # 这里捕获异常转成结构化返回，让上层节点拿到的是『状态字典』而非抛错。
            return {
                "code_result": "",
                "code_error": f"执行超时（上限 {timeout} 秒）：{e}",
                "exit_code": -1,
            }
    finally:
        # own_tmpdir 为真说明这个目录是我们开的，函数退出时无论成败都清掉。
        if own_tmpdir:
            shutil.rmtree(workdir, ignore_errors=True)