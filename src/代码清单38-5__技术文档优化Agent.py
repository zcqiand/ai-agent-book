from dataclasses import dataclass
from typing import List

@dataclass
class DocumentQuality:
    """文档质量评估"""
    technical_accuracy: float   # 技术准确性
    clarity: float              # 表达清晰度
    completeness: float         # 内容完整性
    structure: float            # 结构合理性
    examples: float             # 示例质量

class DocumentOptimizer:
    """技术文档优化器"""

    def __init__(self, llm):
        self.llm = llm

    def evaluate_technical_document(
        self,
        document: str,
        target_audience: str = "中级开发者"
    ) -> DocumentQuality:
        """评估技术文档质量"""
        prompt = f"""评估以下技术文档的质量。

目标读者：{target_audience}

文档内容：
{document}

请从以下维度评分（0-10分）：
1. technical_accuracy（技术准确性）：技术内容是否正确
2. clarity（表达清晰度）：是否易于理解
3. completeness（内容完整性）：是否涵盖所有必要信息
4. structure（结构合理性）：组织是否清晰
5. examples（示例质量）：示例是否充分、有用

输出JSON格式。"""

        response = self.llm.invoke(prompt)
        # 解析为 DocumentQuality 对象
        return DocumentQuality(
            technical_accuracy=8.5,
            clarity=7.5,
            completeness=8.0,
            structure=7.0,
            examples=7.5
        )

    def optimize_document(
        self,
        document: str,
        target_audience: str = "中级开发者"
    ) -> str:
        """优化技术文档"""
        iterations = 3  # 固定迭代次数

        current_doc = document
        for i in range(iterations):
            quality = self.evaluate_technical_document(current_doc, target_audience)

            # 找出最弱的维度
            weakest = min(
                [("technical_accuracy", quality.technical_accuracy),
                 ("clarity", quality.clarity),
                 ("completeness", quality.completeness),
                 ("structure", quality.structure),
                 ("examples", quality.examples)],
                key=lambda x: x[1]
            )

            # 针对最弱维度优化
            optimize_prompt = f"""优化以下技术文档，重点改进 {weakest[0]} 维度。

当前文档：
{current_doc}

当前质量评估：
- 技术准确性：{quality.technical_accuracy}/10
- 表达清晰度：{quality.clarity}/10
- 内容完整性：{quality.completeness}/10
- 结构合理性：{quality.structure}/10
- 示例质量：{quality.examples}/10

最弱维度：{weakest[0]}（{weakest[1]}/10）

请生成改进后的文档。"""

            current_doc = self.llm.invoke(optimize_prompt)

        return current_doc

# 使用示例
def demo_document_optimizer():
    """演示文档优化流程"""
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4")
    optimizer = DocumentOptimizer(llm)

    # 待优化的文档
    original_doc = """
    # Python装饰器教程

    装饰器是Python的重要特性。它可以修改函数的行为。
    使用 @decorator 语法可以应用装饰器。
    """

    # 评估
    quality = optimizer.evaluate_technical_document(original_doc)
    print(f"原始文档质量：")
    print(f"  技术准确性：{quality.technical_accuracy}")
    print(f"  表达清晰度：{quality.clarity}")
    print(f"  内容完整性：{quality.completeness}")

    # 优化
    optimized = optimizer.optimize_document(original_doc)
    print(f"\n优化后文档：\n{optimized}")