from langchain.text_splitter import RecursiveCharacterTextSplitter

class TextChunker:
    """文本分块器"""

    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", "！", "？", " ", ""]
        )

    def chunk(self, documents: list) -> list:
        """分块"""
        return self.splitter.split_documents(documents)

    def chunk_text(self, text: str) -> list:
        """分块单个文本"""
        return self.splitter.split_text(text)

chunker = TextChunker(chunk_size=500, chunk_overlap=50)
chunks = chunker.chunk(docs)

print(f"生成了 {len(chunks)} 个文本块")