from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from typing import List

class MultiFormatKnowledgeBase:
    """多格式知识库"""

    def __init__(self, persist_dir="./multi_kb"):
        self.persist_dir = persist_dir
        self.embeddings = OpenAIEmbeddings()
        self.pdf_parser = PDFParser()
        self.word_parser = WordParser()
        self.md_parser = MarkdownParser()

    def add_pdf(self, file_path: str):
        """添加 PDF"""
        docs = self.pdf_parser.parse_with_metadata(file_path)
        return self._add_documents(docs)

    def add_word(self, file_path: str):
        """添加 Word"""
        docs = self.word_parser.parse(file_path)
        return self._add_documents(docs)

    def add_markdown(self, file_path: str):
        """添加 Markdown"""
        docs = self.md_parser.parse(file_path)
        return self._add_documents(docs)

    def _add_documents(self, docs: list):
        """添加到向量存储"""
        if not hasattr(self, "vectorstore"):
            self.vectorstore = Chroma.from_documents(
                documents=docs,
                embedding=self.embeddings,
                persist_directory=self.persist_dir
            )
        else:
            self.vectorstore.add_documents(docs)

        return f"添加了 {len(docs)} 个文档"

    def search(self, query: str, k=5) -> List:
        """检索"""
        if not hasattr(self, "vectorstore"):
            return []

        return self.vectorstore.similarity_search(query, k=k)

# 使用
kb = MultiFormatKnowledgeBase()

kb.add_pdf("./docs/report.pdf")
kb.add_word("./docs/proposal.docx")
kb.add_markdown("./docs/guide.md")

results = kb.search("如何申请")
for doc in results:
    print(f"文档: {doc.page_content[:100]}...")
