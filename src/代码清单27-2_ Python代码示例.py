from enum import Enum
from typing import Set

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"

# 角色权限映射
ROLE_PERMISSIONS = {
    Role.ADMIN: {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.EXECUTE},
    Role.USER: {Permission.READ, Permission.WRITE, Permission.EXECUTE},
    Role.GUEST: {Permission.READ},
}

class Authorizer:
    """授权控制"""

    def __init__(self):
        self.user_roles = {}

    def set_role(self, user_id: str, role: Role):
        self.user_roles[user_id] = role

    def check_permission(self, user_id: str, permission: Permission) -> bool:
        role = self.user_roles.get(user_id)
        if not role:
            return False

        return permission in ROLE_PERMISSIONS[role]

authorizer = Authorizer()
authorizer.set_role("user_123", Role.USER)

# 使用
if authorizer.check_permission("user_123", Permission.DELETE):
    print("允许删除")
else:
    print("权限不足")
