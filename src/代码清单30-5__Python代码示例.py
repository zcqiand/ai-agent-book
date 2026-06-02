from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

class EnterpriseKnowledgeBase:
    """企业多格式知识库"""

    def __init__(self):
        self.kb = MultiFormatKnowledgeBase()
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.qa_chain = None

    def ingest(self, files: dict):
        """批量导入文件"""
        results = {}

        for file_type, file_paths in files.items():
            for path in file_paths:
                if file_type == "pdf":
                    result = self.kb.add_pdf(path)
                elif file_type == "word":
                    result = self.kb.add_word(path)
                elif file_type == "markdown":
                    result = self.kb.add_markdown(path)

                results[path] = result

        # 构建 QA 链
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.kb.vectorstore.as_retriever(search_kwargs={"k": 5})
        )

        return results

    def query(self, question: str) -> str:
        """知识问答"""
        if not self.qa_chain:
            return "请先导入文档"

        return self.qa_chain.run(question)

# 使用
kb = EnterpriseKnowledgeBase()

results = kb.ingest({
    "pdf": ["./docs/report.pdf", "./docs/handbook.pdf"],
    "word": ["./docs/policy.docx"],
    "markdown": ["./docs/guide.md"]
})

for path, result in results.items():
    print(f"{path}: {result}")

# 问答
answer = kb.query("公司年假政策是什么？")
print(f"回答: {answer}")