class HallucinationDetector:
    """幻觉检测器"""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)

    def detect(self, answer: str, context: str) -> Dict:
        """检测回答中的幻觉"""
        prompt = f"""检测以下回答中是否存在幻觉（上下文中没有的信息）。

        上下文: {context}

        回答: {answer}

        请识别：
        1. 回答中哪些陈述在上下文中没有依据
        2. 对每个幻觉陈述给出严重程度（轻微/中等/严重）

        格式：
        {{
            "has_hallucination": true/false,
            "claims": [
                {{"text": "幻觉内容", "severity": "程度"}}
            ]
        }}"""

        response = self.llm.invoke(prompt)

        try:
            result = json.loads(response.content)
            return result
        except:
            return {"has_hallucination": False, "claims": []}

    def batch_detect(self, answers: List[Tuple[str, str]]) -> List[Dict]:
        """批量检测"""
        results = []
        for answer, context in answers:
            result = self.detect(answer, context)
            results.append(result)

        hallucination_rate = sum(
            1 for r in results if r.get("has_hallucination")
        ) / len(results)

        return {
            "results": results,
            "hallucination_rate": hallucination_rate
        }

detector = HallucinationDetector()

# 检测
result = detector.detect(
    answer="根据文档，公司年假最长为15天",
    context="文档中提到年假按工龄计算，1-3年5天，3-5年10天，5年以上15天"
)
print(f"幻觉检测结果: {result}")