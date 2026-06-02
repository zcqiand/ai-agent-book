from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

class EnterpriseKnowledgeBase:
    """企业知识库"""

    def __init__(self, persist_dir="./kb_vectorstore"):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
        self.persist_dir = persist_dir
        self.qa_chain = None

    def build(self, docs_path: str):
        """构建知识库"""
        # 1. 解析文档
        parser = DocumentParser()
        docs = parser.parse_directory(docs_path)

        # 2. 分块
        chunker = TextChunker()
        chunks = chunker.chunk(docs)

        # 3. 向量化
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )

        # 4. 创建检索链
        llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5})
        )

        return f"知识库构建完成，共 {len(chunks)} 个知识块"

    def query(self, question: str) -> str:
        """知识问答"""
        if not self.qa_chain:
            return "知识库未构建"

        return self.qa_chain.run(question)

# 使用
kb = EnterpriseKnowledgeBase()
kb.build("./documents")
result = kb.query("如何申请年假？")
print(result)