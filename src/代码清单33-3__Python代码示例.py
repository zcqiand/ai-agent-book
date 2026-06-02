from langchain_openai import ChatOpenAI

class EvaluationSetBuilder:
    """评估集构建器"""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)

    def build_from_documents(self, documents: list, questions_per_doc: int = 5) -> list:
        """从文档生成评估问题"""
        eval_set = []

        for doc in documents:
            # 生成问题
            prompt = f"""基于以下文档内容，生成 {questions_per_doc} 个测试问题。
            包括：事实性问题、推理问题、总结性问题。

            文档内容:
            {doc.page_content[:1000]}

            生成的问题（每行一个问题）:"""

            response = self.llm.invoke(prompt)
            questions = [
                q.strip() for q in response.content.split("\n")
                if q.strip() and q.strip()[0].isdigit()
            ]

            # 为每个问题生成期望答案
            for question in questions:
                answer_prompt = f"""基于以下文档回答问题。

                文档: {doc.page_content}
                问题: {question}

                回答:"""

                answer_response = self.llm.invoke(answer_prompt)

                eval_set.append({
                    "question": question,
                    "expected_answer": answer_response.content,
                    "context": doc.page_content,
                    "doc_id": doc.metadata.get("id", "")
                })

        return eval_set

    def add_ground_truth(self, eval_set: list, query: str, answer: str):
        """添加人工标注的问答对"""
        eval_set.append({
            "question": query,
            "expected_answer": answer,
            "source": "human_annotation"
        })
        return eval_set

# 使用
builder = EvaluationSetBuilder()
eval_set = builder.build_from_documents(documents, questions_per_doc=3)

# 添加人工标注
eval_set = builder.add_ground_truth(
    eval_set,
    query="公司年假政策的具体规定是什么？",
    answer="根据员工手册，年假按工龄计算：1-3年5天，3-5年10天，5年以上15天。"
)

print(f"构建了 {len(eval_set)} 个评估用例")