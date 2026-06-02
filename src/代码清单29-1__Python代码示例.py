from langchain_community.document_loaders import DirectoryLoader, PDFLoader

class DocumentParser:
    """文档解析器"""

    def __init__(self):
        self.loaders = {
            ".pdf": PDFLoader,
            ".txt": DirectoryLoader,
            ".md": DirectoryLoader,
        }

    def parse(self, file_path: str) -> list:
        """解析文档"""
        ext = file_path.split(".")[-1]

        if ext == "pdf":
            loader = PDFLoader(file_path)
        else:
            loader = DirectoryLoader(file_path)

        docs = loader.load()
        return docs

    def parse_directory(self, dir_path: str, glob_pattern="**/*.*") -> list:
        """解析目录"""
        loader = DirectoryLoader(dir_path, glob=glob_pattern)
        return loader.load()

parser = DocumentParser()
docs = parser.parse_directory("./knowledge_base")
print(f"解析了 {len(docs)} 个文档")