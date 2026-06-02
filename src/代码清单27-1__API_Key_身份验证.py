from functools import wraps
import hashlib

class Authenticator:
    """简单的 API Key 验证"""

    def __init__(self):
        self.valid_keys = {
            "user1": "hash_of_key1",
            "user2": "hash_of_key2"
        }

    def verify(self, api_key: str) -> str:
        """验证 API Key，返回用户ID"""
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        for user_id, stored_hash in self.valid_keys.items():
            if key_hash == stored_hash:
                return user_id

        return None  # 验证失败

auth = Authenticator()

def require_auth(func):
    """认证装饰器"""
    @wraps(func)
    def wrapper(api_key, *args, **kwargs):
        user_id = auth.verify(api_key)
        if not user_id:
            return {"error": "Unauthorized"}

        return func(user_id, *args, **kwargs)

    return wrapper

@require_auth
def agent_endpoint(user_id: str, query: str):
    """需要认证的 Agent 端点"""
    return f"User {user_id} query: {query}"