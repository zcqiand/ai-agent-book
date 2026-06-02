# 问题1：Handoff 后上下文丢失
# 分析：根据原理，Handoffs 应该自动传递上下文
# 如果丢失，可能是：

# 原因1：没有正确配置 handoffs 列表
router.handoffs = [tech_expert]  # 正确

# 原因2：context 传递方式不对
# 应该使用 handoff() 函数而不是直接赋值
router.handoffs = handoff(tech_expert, context={"key": "value"})

# 问题2：Guardrails 检查不生效
# 分析：Guardrails 在输出前执行，检查失败会拦截

# 原因1：检查函数返回值格式不对
def check(output):
    return {"is_safe": True}  # 错误！应该返回布尔值或特定格式

# 正确格式
def check(output):
    return True  # 或返回特定错误信息

# 原因2：Guardrails 配置位置不对
# 应该在创建 Agent 时配置，不是在 run() 时
agent = Agent(instructions=..., guardrails=[...])

# 问题3：Agent 陷入无限循环
# 分析：Agent 的循环由 stop conditions 控制

# 原因：没有设置合理的 stop conditions
# 解决方案：设置 max_turns 或其他停止条件
result = agent.run("...", max_turns=5)  # 最多5轮