# 在 code/saas-cs-agent 目录下执行；PYTHONPATH=src 保证可导入包内模块
# PowerShell 写法：$env:PYTHONPATH="src"；bash 写法：export PYTHONPATH=src
#
# 脚本复制即跑：不依赖真实 API Key、不调任何 LLM SDK，只验证 tenant.py 的
# 两件事——thread_id_for 的双重隔离（同租户不同会话 / 不同租户同会话都得不同
# thread_id），以及 TenantRouter 的 register 幂等 / get_thread 已登记返回+未登记即时构建。
from saas_cs_agent.tenant import thread_id_for, TenantRouter

# 1) thread_id_for 双重隔离验证。
#    格式 `{tenant_id}:{session_id}` 两段输入只要有一段不同，输出就不同——
#    这是「双重隔离」的物理基础，无需任何特判。
tid_acme_s1 = thread_id_for("acme", "s1")   # 同租户、会话 s1
tid_acme_s2 = thread_id_for("acme", "s2")   # 同租户、会话 s2 → 会话隔离
tid_globex_s1 = thread_id_for("globex", "s1")  # 不同租户、同会话 s1 → 租户隔离

print("thread_id_for('acme', 's1')   =", tid_acme_s1)
print("thread_id_for('acme', 's2')   =", tid_acme_s2)
print("thread_id_for('globex', 's1') =", tid_globex_s1)

# 会话隔离：同租户不同会话 → 不同 thread_id（acme:s1 != acme:s2）
assert tid_acme_s1 != tid_acme_s2, "会话隔离失败：同租户不同会话撞了 thread_id"
# 租户隔离：不同租户同会话 → 不同 thread_id（acme:s1 != globex:s1）
assert tid_acme_s1 != tid_globex_s1, "租户隔离失败：不同租户同会话撞了 thread_id"
# 双重叠加：acme:s2 与 globex:s1 两段都不同，必然不同
assert tid_acme_s2 != tid_globex_s1, "双重隔离失败：两段都不同却撞了 thread_id"
print("双重隔离 OK：会话隔离 + 租户隔离 + 双重叠加，两两不同")

# 2) TenantRouter.register 幂等验证。
#    幂等性来自 thread_id_for 的确定性（同输入恒同输出），不是 register 内部去重——
#    register 每次都 self._threads[(t,s)] = thread_id_for(t,s)，只是写同一个值。
router = TenantRouter()
t1 = router.register("acme", "s1")
t2 = router.register("acme", "s1")  # 重复登记同一组合
print("register('acme', 's1') 第1次 =", t1)
print("register('acme', 's1') 第2次 =", t2)
assert t1 == t2 == "acme:s1", "幂等失败：重复登记返回了不同值"
print("register 幂等 OK：重复登记同一组合始终返回 'acme:s1'")

# 3) TenantRouter.get_thread 验证。
#    已登记则返回存储值；未登记则即时构建（不写入注册表，保持 register 的显式语义）。
g1 = router.get_thread("acme", "s1")     # 已登记 → 返回存储值 'acme:s1'
g2 = router.get_thread("globex", "s9")   # 未登记 → 即时构建 'globex:s9'，但不写入注册表
print("get_thread('acme', 's1')   =", g1, "（已登记，返回存储值）")
print("get_thread('globex', 's9') =", g2, "（未登记，即时构建）")
assert g1 == "acme:s1", "get_thread 已登记返回值不符"
assert g2 == "globex:s9", "get_thread 未登记即时构建值不符"
# 验证 get_thread 未登记不写入注册表：再 register('globex','s9') 应拿到同一个值，
# 且注册表里此前并不存在该键（若 get_thread 已偷偷写入，register 仍写同值，行为不变——
# 真正的区分在「显式登记 vs 即时构建」的语义，而非注册表是否有副作用）。
assert router.register("globex", "s9") == "globex:s9"
print("get_thread OK：已登记返回存储值，未登记即时构建 'globex:s9'")