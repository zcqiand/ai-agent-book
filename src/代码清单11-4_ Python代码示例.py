app = workflow.compile()

# 运行
result = app.invoke({
    "messages": ["用户的问题"],
    "current_step": "start",
    "context": {},
    "result": ""
})

print(result["result"])
