"""安全四件之：身份验证（API Key）+ 授权（RBAC）。

把旧 ch27 的 Authenticator（API Key + hashlib.sha256）+ Authorizer
（Role/Permission RBAC）思想改写成 FastAPI Depends 形态：
  - verify_api_key：从请求头取 X-API-Key、sha256 比对、返回 user_id 或抛 401；
  - require_permission(...)：依赖工厂，检查当前 user 是否有所需 Permission，
    无则抛 403。

两层 Depends 叠加在一个端点上，就实现了「先认证、再授权」的纵深姿态。
秘钥管理（环境变量 + secrets，不入代码库）见文末说明。
"""
from __future__ import annotations
import hashlib
from enum import Enum

from fastapi import Depends, FastAPI, Header, HTTPException


# --- 1. Role / Permission / 角色权限映射 ----------------------------

class Role(Enum):
    """角色枚举：三类典型身份。"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class Permission(Enum):
    """权限枚举：四类典型操作。"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"


# 角色权限映射：set 表达「无序、不重复」，判重用 O(1) 集合查找
ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.ADMIN: {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.EXECUTE},
    Role.USER: {Permission.READ, Permission.WRITE, Permission.EXECUTE},
    Role.GUEST: {Permission.READ},
}


# --- 2. 用户表：user_id → (key_hash, role) --------------------------

def _sha256(text: str) -> str:
    """对明文做 sha256，返回十六进制摘要。

    为什么存哈希而非明文：即便用户表泄漏，攻击者也无法直接拿到原始
    API Key——sha256 是单向函数。比对时把请求里的 Key 同样哈希一遍、
    再跟存的哈希比即可。
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# 演示用用户表：生产环境这个表应在数据库里，这里写死只为可独立运行。
USERS: dict[str, dict] = {
    "u_admin": {"key_hash": _sha256("admin-secret-key"), "role": Role.ADMIN},
    "u_user": {"key_hash": _sha256("user-secret-key"), "role": Role.USER},
    "u_guest": {"key_hash": _sha256("guest-secret-key"), "role": Role.GUEST},
}
# 反向索引：key_hash → user_id，把校验从 O(n) 遍历降到 O(1) 查找
_KEY_HASH_TO_USER: dict[str, str] = {
    info["key_hash"]: uid for uid, info in USERS.items()
}


# --- 3. 身份验证依赖：verify_api_key --------------------------------

def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> str:
    """从请求头取 X-API-Key，sha256 比对，返回 user_id 或抛 401。

    Header(...) 让 FastAPI 自动从请求头取值、缺失时返回 422（参数缺失），
    校验通过则返回 user_id 供下游依赖（require_permission）复用——
    这就是 Depends 的串联：一个依赖的返回值会被下一个依赖通过参数名接住。
    """
    user_id = _KEY_HASH_TO_USER.get(_sha256(x_api_key))
    if user_id is None:
        raise HTTPException(status_code=401, detail="无效的 API Key")
    return user_id


# --- 4. 授权依赖工厂：require_permission ----------------------------

def require_permission(permission: Permission):
    """依赖工厂：返回一个检查 ``permission`` 的依赖函数。

    为什么是工厂而非直接一个函数：端点需要的权限不同（有的要 DELETE、
    有的要 EXECUTE），用工厂按需生产依赖函数，避免每个端点手写一遍
    权限检查。FastAPI 把内层函数当 Depends 处理——它的参数 user_id
    会自动接住上游 verify_api_key 的返回值。
    """
    def _checker(user_id: str = Depends(verify_api_key)) -> str:
        role = USERS[user_id]["role"]
        if permission not in ROLE_PERMISSIONS[role]:
            raise HTTPException(
                status_code=403,
                detail=f"角色 {role.value} 无 {permission.value} 权限",
            )
        return user_id
    return _checker


# --- 5. 演示端点：两层 Depends 叠加 --------------------------------

app = FastAPI(title="Ch21 Security Demo")


@app.delete("/data/{item_id}")
def delete_data(
    item_id: str,
    user_id: str = Depends(require_permission(Permission.DELETE)),
):
    """删除数据：必须通过身份验证（API Key）且角色有 DELETE 权限。

    两层 Depends 叠加的执行顺序由 FastAPI 自动编排：
    verify_api_key（内层，先跑）→ require_permission 产出的 _checker（外层，后跑）。
    任意一层抛异常都会短路返回对应状态码（401 / 403）。
    """
    return {"deleted": item_id, "by": user_id}


@app.get("/data/{item_id}")
def read_data(
    item_id: str,
    user_id: str = Depends(require_permission(Permission.READ)),
):
    """读取数据：身份验证 + READ 权限。GUEST 也能调通。"""
    return {"item": item_id, "by": user_id}


# --- 6. 秘钥管理说明 ------------------------------------------------
# 上面的明文 Key（"admin-secret-key" 等）写死在代码里只为演示。
# 生产环境务必：
#   1) 明文 Key 通过环境变量或 secrets 管理系统注入，不入代码库；
#   2) USERS 表存数据库，启动时加载；
#   3) 真实系统的 Key 应有足够熵（用 secrets.token_urlsafe(32) 生成）。
# 生产姿势示意（本章不启用）：
#   _DEMO_KEY = os.environ.get("AGENT_API_KEY")  # 从环境变量取
#   _SAFE_KEY = secrets.token_urlsafe(32)        # 生成高熵 Key 的正确方式