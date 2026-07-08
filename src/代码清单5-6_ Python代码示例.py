# 启用详细输出
chain = prompt | llm
chain.verbose = True  # 或者在 invoke 时传 verbose=True