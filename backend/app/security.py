import secrets

from fastapi import Header, HTTPException, status

from .settings import settings


def require_admin(x_admin_token: str | None = Header(default=None)) -> None:
    expected = settings.admin_api_token
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Administrative API access is not configured",
        )
    if not x_admin_token or not secrets.compare_digest(x_admin_token, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid administrative credentials",
        )
