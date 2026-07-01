import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool

os.environ["LANGCHAIN_API_KEY"] = "your-key"
os.environ["LANGCHAIN_TRACING_V2"] = "true"

class AgentEvaluator:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.agent = self._create_agent()

    def _create_agent(self):
        """创建被评估的 Agent"""
        tools = [
            Tool(name="搜索", func=lambda q: f"关于{q}的信息...", description="搜索信息")
        ]
        return initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=False
        )

    def evaluate_single(self, question: str, criteria: dict) -> dict:
        """评估单个问题"""
        # 1. 获取 Agent 回答
        answer = self.agent.run(question)

        # 2. LLM 评估
        evaluation_prompt = f"""
        问题：{question}
        回答：{answer}

        评估标准：{criteria}

        给出评分（1-5）和简短评价。
        """

        evaluation = self.llm.invoke(evaluation_prompt)

        return {
            "question": question,
            "answer": answer,
            "evaluation": evaluation.content
        }

    def evaluate_dataset(self, test_cases: list) -> dict:
        """评估整个数据集"""
        results = []
        for case in test_cases:
            result = self.evaluate_single(
                question=case["question"],
                criteria=case.get("criteria", "回答质量")
            )
            results.append(result)

        # 汇总
        total = len(results)
        return {
            "total_cases": total,
            "results": results
        }

# 使用示例
evaluator = AgentEvaluator()

test_cases = [
    {"question": "什么是机器学习？"},
    {"question": "AI的未来发展趋势是什么？"},
    {"question": "如何入门深度学习？"},
]

report = evaluator.evaluate_dataset(test_cases)
print(f"评估完成，共 {report['total_cases']} 个测试用例")

for r in report["results"]:
    print(f"\n问题: {r['question']}")
    print(f"回答: {r['answer'][:100]}...")
    print(f"评估: {r['evaluation']}")
