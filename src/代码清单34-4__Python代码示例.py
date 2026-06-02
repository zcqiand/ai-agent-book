from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from slowapi import Limiter
from slowapi.util import get_remote_address
import hashlib
import time

app = FastAPI()

# 限流器
limiter = Limiter(key_func=get_remote_address)

# API Key 认证
api_key_header = APIKeyHeader(name="X-API-Key")

# 简单的 API Key 验证
VALID_API_KEYS = {
    "key_client_001": "user_001",
    "key_client_002": "user_002"
}

async def verify_api_key(api_key: str = Depends(api_key_header)):
    """验证 API Key"""
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=403, detail="无效的 API Key")
    return VALID_API_KEYS[api_key]

@app.post("/api/query")
@limiter.limit("10/minute")  # 每分钟10次请求
async def query(request: QueryRequest, user_id: str = Depends(verify_api_key)):
    """问答接口（需认证，限流）"""
    # 实现...
    pass

# 请求日志中间件
@app.middleware("http")
async def log_requests(request, call_next):
    """记录请求日志"""
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    print(f"{request.method} {request.url.path} - {response.status_code} ({duration:.2f}s)")

    return response