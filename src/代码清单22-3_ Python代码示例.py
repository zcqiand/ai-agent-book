# 1. 减少不必要的 Handoffs
# 如果只有简单问题，不需要经过多级 Agent

# 2. 合理设置 max_turns
result = agent.run(input, max_turns=5)  # 防止无限循环

# 3. 使用流式输出提升感知性能
# 对于长回答，使用 stream=True 让用户看到思考过程

# 4. 缓存常用 Agent
# 如果某个 Agent 被频繁使用，可以预加载

# 5. 异步处理非关键步骤
# 满意度调查等非关键步骤可以异步执行
