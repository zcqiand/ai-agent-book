from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 步骤1：分析问题
analyze_prompt = ChatPromptTemplate.from_template(
    """你是一个问题分析专家。请分析以下问题，识别关键概念和潜在的回答方向。
    问题：{question}
    
    分析要点：
    1. 问题涉及哪些核心概念？
    2. 回答需要涵盖哪些方面？
    3. 有哪些需要注意的细节或限制条件？"""
)

# 步骤2：生成回答
answer_prompt = ChatPromptTemplate.from_template(
    """基于以下分析，生成一个全面且准确的回答。
    
    【分析】
    {analysis}
    
    【原问题】
    {question}
    
    请生成一个结构清晰、详略得当的回答。"""
)

# 使用 LCEL 组合两个步骤
analyze_chain = analyze_prompt | llm
full_chain = (
    {"question": lambda x: x["question"], "analysis": analyze_chain}
    | answer_prompt
    | llm
)

# 调用 Chain
response = full_chain.invoke({
    "question": "大语言模型是如何工作的？它们为什么能生成看似智能的文本？"
})
print(response.content)