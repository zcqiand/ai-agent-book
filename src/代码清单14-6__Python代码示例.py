from langchain.memory import ConversationBufferMemory, VectorStoreRetrieverMemory
from langchain_openai import ChatOpenAI

class MultiLayerMemory:
    """多层记忆系统"""
    def __init__(self):
        self.short_term = ConversationBufferMemory(memory_key="short")
        self.long_term = VectorStoreRetrieverMemory(memory_key="long")

    def save(self, input_data, output_data):
        self.short_term.save_context(input_data, output_data)
        # 同时保存到长期记忆
        self.long_term.save_context(input_data, output_data)

    def load(self, query):
        short = self.short_term.load_memory_variables({})
        long = self.long_term.load_memory_variables({"query": query})
        return {
            "short_term": short.get("short", []),
            "long_term": long.get("long", [])
        }

# 使用多层记忆
memory = MultiLayerMemory()
memory.save({"input": "我喜欢川菜"}, {"output": "好的，已记住"})
memory.save({"input": "我工作很忙"}, {"output": "了解，您比较忙"})

context = memory.load("用户的饮食偏好")
print(context["long_term"])  # 可能找回"喜欢川菜"