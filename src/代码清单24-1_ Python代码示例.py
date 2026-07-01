# 独立调用的问题
response1 = llm.invoke("我叫张三")
print(response1)  # 不会记住"张三"

response2 = llm.invoke("我叫什么？")
print(response2)  # 不知道
