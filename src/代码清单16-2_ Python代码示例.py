from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 加载文档
loader = DirectoryLoader('./docs', glob="**/*.txt")
documents = loader.load()

# 分块策略
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # 每块500字符
    chunk_overlap=50,    # 块之间50字符重叠
    separators=["\n\n", "\n", "。", "！", "？"]  # 按优先级分割
)

chunks = text_splitter.split_documents(documents)
print(f"生成了 {len(chunks)} 个文档块")
