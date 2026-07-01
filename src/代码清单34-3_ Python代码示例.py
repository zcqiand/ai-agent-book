from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from your_rag_module import RAGSystem

app = FastAPI(title="企业知识库 API", version="1.0.0")

# 初始化
rag = RAGSystem()

# 请求模型
class QueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    top_k: Optional[int] = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]
    session_id: str

# 端点
@app.post("/api/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """问答接口"""
    try:
        result = rag.query(
            request.question,
            session_id=request.session_id,
            top_k=request.top_k
        )

        return QueryResponse(
            answer=result["answer"],
            sources=[{"content": doc.page_content, "metadata": doc.metadata}
                     for doc in result.get("source_documents", [])],
            session_id=request.session_id or "default"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health():
    """健康检查"""
    return {"status": "healthy"}

@app.get("/api/sessions/{session_id}/history")
async def get_history(session_id: str):
    """获取会话历史"""
    history = rag.get_history(session_id)
    return {"session_id": session_id, "history": history}

# 启动命令
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
