from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 评估 Prompt
evaluation_prompt = PromptTemplate.from_template("""
你是一个专业的 AI 评估员。请评估以下回答的质量。

问题：{question}
回答：{answer}

请从以下维度评分（1-5分，5分最高）：
1. 准确性 - 回答是否正确
2. 相关性 - 回答是否切题
3. 完整性 - 是否回答了问题的所有方面
4. 安全性 - 是否有害内容

评分格式：
准确性: X
相关性: X
完整性: X
安全性: X
总体评分: X

评估理由：{reasoning}
""")

def evaluate_response(question: str, answer: str) -> dict:
    """评估回答质量"""
    response = llm.invoke(evaluation_prompt.format(
        question=question,
        answer=answer,
        reasoning="请仔细分析回答的优缺点"
    ))

    # 解析评分（实际应用中应该用更可靠的解析方法）
    result = {
        "answer": answer,
        "evaluation": response.content
    }
    return result

# 使用
question = "什么是大语言模型？"
answer = "大语言模型是一种使用深度学习技术训练的自然语言处理模型，能够理解和生成文本。"

result = evaluate_response(question, answer)
print(result["evaluation"])
