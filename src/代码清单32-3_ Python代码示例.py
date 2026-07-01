from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

class ConversationalRAG:
    """对话式 RAG"""

    def __init__(self, vectorstore, embeddings):
        self.vectorstore = vectorstore
        self.embeddings = embeddings
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.history_manager = ConversationHistoryManager()
        self.chain = None
        self._build_chain()

    def _build_chain(self):
        """构建对话链"""
        prompt = PromptTemplate.from_template("""基于以下对话历史和检索到的文档回答问题。
        如果发现对话历史中的问题和当前问题相关，请结合历史上下文回答。

        对话历史:
        {chat_history}

        检索到的文档:
        {context}

        问题: {question}

        回答:""")

        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
            combine_docs_chain_kwargs={"prompt": prompt}
        )

    def query(self, session_id: str, question: str) -> str:
        """查询"""
        # 获取对话历史
        history = self.history_manager.get_history(session_id)
        chat_history = self._format_history(history)

        # 执行查询
        response = self.chain.invoke({
            "question": question,
            "chat_history": chat_history
        })

        # 保存历史
        self.history_manager.add_message(session_id, "user", question)
        self.history_manager.add_message(session_id, "assistant", response["answer"])

        return response["answer"]

    def _format_history(self, history: List[Dict]) -> str:
        """格式化历史"""
        return "\n".join([
            f"{'用户' if m['role'] == 'user' else '助手'}: {m['content']}"
            for m in history
        ])

# 使用
rag = ConversationalRAG(vectorstore, OpenAIEmbeddings())

print(rag.query("session_1", "公司的年假政策是什么？"))
print(rag.query("session_1", "那加班调休呢？"))
