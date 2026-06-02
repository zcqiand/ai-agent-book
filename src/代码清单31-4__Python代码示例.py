from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class OptimizedRAG:
    """优化后的 RAG 系统"""

    def __init__(self, vectorstore, embeddings):
        self.vectorstore = vectorstore
        self.embeddings = embeddings
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.rewriter = QueryRewriter()
        self.reranker = Reranker(embeddings)

    def build_chain(self):
        """构建 RAG 链"""
        prompt = PromptTemplate.from_template("""基于以下上下文回答问题。
        如果上下文中没有相关信息，诚实地说明不知道。

        上下文:
        {context}

        问题: {question}

        回答:""")

        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 10}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )

    def query(self, question: str) -> dict:
        """查询"""
        # 1. 查询改写
        refined_query = self.rewriter.rewrite(question)

        # 2. 检索
        docs = self.vectorstore.similarity_search(refined_query, k=20)

        # 3. 重排
        reranked_docs = self.reranker.rerank(refined_query, docs, top_k=5)

        # 4. 构建上下文
        context = "\n\n".join([doc.page_content for doc in reranked_docs])

        # 5. 生成回答
        response = self.llm.invoke(f"上下文:\n{context}\n\n问题: {question}")

        return {
            "question": question,
            "refined_query": refined_query,
            "answer": response.content,
            "source_documents": reranked_docs
        }

# 使用
rag = OptimizedRAG(vectorstore, OpenAIEmbeddings())
result = rag.query("公司年假是怎么计算的？")
print(f"回答: {result['answer']}")