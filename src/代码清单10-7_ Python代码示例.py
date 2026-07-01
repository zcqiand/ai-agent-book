# 查看中间输出
chain = prompt | llm
# 单独测试 prompt
prompt_output = prompt.invoke({"input": "测试"})
print(prompt_output)
