import sys


def apply_resource_limits(cpu_seconds=5, memory_mb=256, file_size_mb=10):
    """在当前进程上设置 CPU 时间 / 内存 / 输出文件大小三项硬上限。

    用法：此函数必须在『子进程内部』调用——即把它写到 snippet.py 的开头，
    让设上限的对象是子进程，不是主进程。
    """
    try:
        import resource  # POSIX 专属模块，Windows 上 import 直接失败
    except ImportError:
        # Windows 没有 resource 模块。这种平台上进程级资源限制要靠 Job Object
        # 这套 Win32 API（Python 标准库没有封装），落地成本高且与 POSIX 写法不可对齐。
        # 本章的诚实折中是：Windows 仅靠 subprocess 的 timeout 兜底，
        # 内存/文件大小上限在 Windows 上不强制——这是『跨平台诚实边界』。
        return {"status": "skipped", "reason": "resource 模块在当前平台不可用（Windows 兜底）"}

    # RLIMIT_CPU：进程消耗的 CPU 时间（秒）。超限内核会发 SIGXCPU，默认终止进程。
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds))

    # RLIMIT_AS：进程虚拟地址空间上限（字节）。超限后 malloc 返回 NULL，Python 抛 MemoryError。
    mem_bytes = memory_mb * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))

    # RLIMIT_FSIZE：进程能写出的单个文件大小上限（字节）。防御『把磁盘塞满』的 DoS。
    fsize_bytes = file_size_mb * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_FSIZE, (fsize_bytes, fsize_bytes))

    return {
        "status": "applied",
        "limits": {"cpu_seconds": cpu_seconds, "memory_mb": memory_mb, "file_size_mb": file_size_mb},
    }


if __name__ == "__main__":
    info = apply_resource_limits(cpu_seconds=2, memory_mb=128, file_size_mb=5)
    print(info)
    print("limits ready, platform =", sys.platform)