from langchain_community.document_loaders import PDFLoader, UnstructuredPDFLoader

class PDFParser:
    """PDF 解析器"""

    def __init__(self):
        self.loader_mode = "fast"  # fast 或 detailed

    def parse(self, file_path: str, mode="fast") -> list:
        """解析 PDF"""
        if mode == "fast":
            loader = PDFLoader(file_path)
        else:
            loader = UnstructuredPDFLoader(file_path)

        docs = loader.load()
        return docs

    def parse_with_metadata(self, file_path: str) -> list:
        """带元数据的解析"""
        loader = PDFLoader(file_path, add_page_numbers=True)

        docs = loader.load()

        # 添加文档级元数据
        for i, doc in enumerate(docs):
            doc.metadata["page"] = i + 1
            doc.metadata["source"] = file_path

        return docs

pdf_parser = PDFParser()
docs = pdf_parser.parse_with_metadata("document.pdf")
print(f"解析了 {len(docs)} 页")
