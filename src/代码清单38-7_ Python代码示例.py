class ComparativeEvaluator:
    """对比评估器"""

    def __init__(self, llm):
        self.llm = llm

    def compare(
        self,
        original: str,
        improved: str,
        criteria: list
    ) -> dict:
        """对比两个版本的优劣"""
        prompt = f"""对比以下两个版本的内容，按照给定标准判断改进效果。

原始版本：
{original}

改进版本：
{improved}

评估标准：{', '.join(criteria)}

请逐项分析：
1. 每个标准下哪个版本更好？
2. 改进幅度如何？
3. 改进是否引入了新问题？

输出JSON格式。"""

        response = self.llm.invoke(prompt)
        return self._parse(response)
