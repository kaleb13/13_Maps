from typing import List, Callable

from fastapi import Depends, HTTPException, status

from app.core.security import get_current_user
from app.models.user import User

class RoleChecker:
    """
    Dependency class to enforce Role-Based Access Control (RBAC).
    """
    def __init__(self, allowed_roles: List[str], require_superuser: bool = False):
        self.allowed_roles = allowed_roles
        self.require_superuser = require_superuser

    def __call__(self, user: User = Depends(get_current_user)) -> User:
        if self.require_superuser and not user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Superuser privileges required"
            )
            
        if user.is_superuser:
            return user  # Superusers bypass regular role checks

        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Required roles: {', '.join(self.allowed_roles)}"
            )

        return user

def require_roles(roles: List[str]) -> Callable:
    """Helper to return a RoleChecker instance"""
    return RoleChecker(allowed_roles=roles)

def require_superuser() -> Callable:
    """Helper to return a RoleChecker instance requiring superuser"""
    return RoleChecker(allowed_roles=[], require_superuser=True)
