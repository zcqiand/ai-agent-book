from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

class EnterpriseRAG:
    def __init__(self, docs_path):
        self.docs_path = docs_path
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.vectorstore = None
        self.retriever = None
        self.prompt = ChatPromptTemplate.from_template(
            "你是一名严谨的企业知识库助手。请只依据下面的资料回答问题，"
            "资料中没有的内容请直接说「资料中未提及」。\n\n"
            "【资料】\n{context}\n\n【问题】{question}"
        )

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

        # 检索器（LCEL 链的检索端）
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

        return f"索引完成，共 {len(chunks)} 个文档块"

    def ask(self, question):
        """问答：LCEL 手搓链——检索→拼 context→生成"""
        if not self.retriever:
            return "请先调用 load_and_index() 建立索引"

        docs = self.retriever.invoke(question)
        context = "\n".join(d.page_content for d in docs)
        messages = self.prompt.format_messages(context=context, question=question)
        answer = self.llm.invoke(messages).content

        return {
            "answer": answer,
            "sources": [doc.page_content[:100] for doc in docs]
        }

# 使用示例
rag = EnterpriseRAG("./company_docs")
rag.load_and_index()
answer = rag.ask("公司对远程办公有什么政策？")
print(answer)