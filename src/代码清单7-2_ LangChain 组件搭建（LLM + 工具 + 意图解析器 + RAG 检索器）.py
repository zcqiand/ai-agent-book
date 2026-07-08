from typing import Literal
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


# 1) LLM：用 LangChain 的 ChatOpenAI 包装，而非裸调 openai SDK
#    temperature=0 让意图分类与工具调用结果稳定可复现
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# 2) 查询请假余额工具：@tool 装饰器把普通函数登记为 LangChain 工具
#    教学版返回 mock 数据；生产环境接 HR 系统
@tool
def query_leave_balance(employee_id: str) -> str:
    """查询某员工的年假余额。入参 employee_id 为员工工号。"""
    # 真实场景调 HR 接口；这里返回写死数据让示例无外部依赖也能跑
    return f"员工{employee_id}年假余额：10天"


# 3) 意图结构化：PydanticOutputParser 用 pydantic schema 约束 LLM 输出
#    把意图塞进固定字段，比让 LLM 自由吐字符串更稳——下游路由靠它分流
class IntentClassification(BaseModel):
    intent: Literal["rag", "tool", "chat"] = Field(
        ..., description="用户意图：查资料=rag，查订单/查余额=tool，闲聊=chat"
    )
    reason: str = Field(..., description="一句话说明为何这么分类")


intent_parser = PydanticOutputParser(pydantic_object=IntentClassification)


# 4) RAG 检索器：教学版用内存 retriever，再用 LCEL 把「检索→拼接→生成」串起来
#    生产环境把 InMemoryRetriever 换成 FAISS / Chroma 等真实向量库，下游拼接不变
class InMemoryRetriever(BaseRetriever):
    """最小内存检索器：按关键词命中返回预设文档。

    真实 RAG 用向量相似度召回；这里按子串匹配足够讲清组件拼装方式，
    且不依赖 embedding 模型，复制即可跑。
    """

    docs: list = [
        Document(page_content="公司年假政策：入职满1年享有5天年假，满3年10天，满10年15天。"),
        Document(page_content="请假流程：在OA系统提交申请，直属经理审批后生效。"),
    ]

    def _get_relevant_documents(self, query, *, run_manager=None):
        # 关键词命中即返回，教学用；真实场景换 similarity_search
        return [d for d in self.docs if any(w in d.page_content for w in ("年假", "请假", "政策", "流程"))]


# retriever：负责「取文档」这一步
retriever = InMemoryRetriever()


# qa_chain：用 LCEL 把「检索→拼 context→生成」串成一条可调用的链
# 这等价于旧版 RetrievalQA.from_chain_type(chain_type="stuff") 的效果——
# LangChain 1.x 已移除 RetrievalQA，改用 LCEL 手搓更显式也更可控
def qa_chain_invoke(query: str) -> dict:
    docs = retriever.invoke(query)
    context = "\n".join(d.page_content for d in docs)
    answer = llm.invoke(f"根据以下资料回答问题：\n{context}\n问题：{query}")
    return {"query": query, "result": answer.content}


qa_chain = type("QAChain", (), {"invoke": staticmethod(qa_chain_invoke)})()