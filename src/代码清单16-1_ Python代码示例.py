
# Chroma - 轻量级，适合本地开发
from langchain_community.vectorstores import Chroma
# FAISS - Facebook开源，适合大规模数据
from langchain_community.vectorstores import FAISS
# Pinecone - 云服务，适合生产环境
from langchain_community.vectorstores import Pinecone

### 文档加载与分块

文档需要先分块（Chunking）才能向量化。分块策略直接影响检索质量。
