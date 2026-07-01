from langchain.memory import ConversationWindowBufferMemory

memory = ConversationWindowBufferMemory(
    memory_key="window",
    k=5,  # 只保留最近5轮
    return_messages=True
)

# 超过5轮后，最早的对话会被自动清除
for i in range(10):
    memory.save_context(
        {"input": f"用户消息{i}"},
        {"output": f"助手回复{i}"}
    )

# 只保留最后5轮
window = memory.load_memory_variables({})
print(len(window["window"]))  # 5
