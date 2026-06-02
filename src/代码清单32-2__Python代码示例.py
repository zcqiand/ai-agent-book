from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from typing import List, Dict, Set

class MultiDocumentContextManager:
    """多文档上下文管理器"""

    def __init__(self):
        self.vectorstores: Dict[str, Chroma] = {}
        self.document_metadata: Dict[str, Dict] = {}
        self.embeddings = OpenAIEmbeddings()

    def add_document(self, doc_id: str, documents: list, metadata: dict = None):
        """添加文档到独立向量存储"""
        vs = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=f"./vs_{doc_id}"
        )
        vs.persist()

        self.vectorstores[doc_id] = vs
        self.document_metadata[doc_id] = metadata or {}

    def retrieve(self, query: str, doc_ids: List[str] = None, k: int = 3) -> List[dict]:
        """从指定文档或全部文档检索"""
        results = []
        target_vs = doc_ids if doc_ids else list(self.vectorstores.keys())

        for doc_id in target_vs:
            if doc_id not in self.vectorstores:
                continue

            docs = self.vectorstores[doc_id].similarity_search(query, k=k)

            for doc in docs:
                results.append({
                    "content": doc.page_content,
                    "doc_id": doc_id,
                    "metadata": {**doc.metadata, **self.document_metadata[doc_id]}
                })

        # 按相关性排序
        results.sort(key=lambda x: x["metadata"].get("score", 0), reverse=True)
        return results[:k]

    def build_context(self, query: str, retrieved: List[dict]) -> str:
        """构建多文档上下文"""
        context_parts = []

        for i, item in enumerate(retrieved, 1):
            doc_name = item["metadata"].get("name", item["doc_id"])
            context_parts.append(f"【文档{i}: {doc_name}】\n{item['content']}")

        return "\n\n".join(context_parts)

# 使用
mdcm = MultiDocumentContextManager()

# 添加多个文档
mdcm.add_document("policy", policy_docs, {"name": "员工政策手册"})
mdcm.add_document("handbook", handbook_docs, {"name": "员工守则"})

# 检索
results = mdcm.retrieve("年假和调休", k=5)
context = mdcm.build_context("年假和调休", results)