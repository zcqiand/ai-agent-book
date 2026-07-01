from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

class EnterpriseRAG:
    def __init__(self, docs_path):
        self.docs_path = docs_path
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.vectorstore = None
        self.qa_chain = None

    def load_and_index(self):
        """加载文档并建立索引"""
        # 加载
        loader = DirectoryLoader(self.docs_path, glob="**/*.*")
        docs = loader.load()

        # 分块
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(docs)

        # 向量化
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory="./enterprise_vector_db"
        )

        # 创建检索链
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 5}
            ),
            return_source_documents=True
        )

        return f"索引完成，共 {len(chunks)} 个文档块"

    def ask(self, question):
        """问答"""
        if not self.qa_chain:
            return "请先调用 load_and_index() 建立索引"

        result = self.qa_chain({"query": question})
        return {
            "answer": result["result"],
            "sources": [doc.page_content[:100] for doc in result["source_documents"]]
        }

# 使用示例
rag = EnterpriseRAG("./company_docs")
rag.load_and_index()
answer = rag.ask("公司对远程办公有什么政策？")
print(answer)
