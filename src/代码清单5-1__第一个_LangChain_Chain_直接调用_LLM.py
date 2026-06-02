from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# 初始化 LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# 直接调用
response = llm.invoke("用一句话解释什么是AI智能体")
print(response.content)