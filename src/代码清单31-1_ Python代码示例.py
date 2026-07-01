from langchain_openai import ChatOpenAI

class QueryRewriter:
    """查询改写器"""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)

    def rewrite(self, query: str) -> str:
        """将口语化查询改写为检索友好的形式"""
        prompt = f"""将以下用户查询改写为更适合检索的形式。
        保留核心意图，补充必要的上下文信息。

        原始查询: {query}
        改写后:"""

        response = self.llm.invoke(prompt)
        return response.content.strip()

    def expand(self, query: str) -> list:
        """查询扩展，生成多个检索 query"""
        prompt = f"""为以下查询生成3个不同的检索 query，
        从不同角度描述同一个问题。

        原始查询: {query}
        扩展 query（每行一个）:"""

        response = self.llm.invoke(prompt)
        queries = [q.strip() for q in response.content.split("\n") if q.strip()]
        return queries

rewriter = QueryRewriter()
# 改写
refined = rewriter.rewrite("我想了解公司的年假政策")
print(f"改写后: {refined}")

# 扩展
expanded = rewriter.expand("如何申请报销")
for i, q in enumerate(expanded, 1):
    print(f"Query {i}: {q}")
