from datetime import datetime
from fastapi import Header, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from config.db_conf import AsyncSession, get_db
from crud.user import get_user_token_jti, get_token_user_info
from utils.jwt import JWTError, JWTExpiredError, decode_access_token

WHITE_LIST_PATHS = {
    "/api/users/login",
    "/api/users/register",
    "/docs",
    "/redoc",
    "/openapi.json",
}


def _unauthorized(message: str):
    return JSONResponse(
        status_code=401,
        content={"code": 401, "message": message, "data": None},
    )


def _is_public_path(path: str):
    return path in WHITE_LIST_PATHS or path.startswith("/docs/")


# 请求拦截
def register_auth_middleware(app):
    @app.middleware("http")
    async def auth_middleware(request, call_next):
        if request.method == "OPTIONS" or _is_public_path(request.url.path):
            return await call_next(request)

        if not request.url.path.startswith("/api"):
            return await call_next(request)
        authorization = request.headers.get("Authorization", "")
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not token:
            return _unauthorized("请先登录")

        try:
            payload = decode_access_token(token)
        except JWTExpiredError:
            return _unauthorized("token已过期")
        except JWTError:
            return _unauthorized("token无效")

        user_id = int(payload["sub"])
        jti = payload["jti"]
        async with AsyncSession() as db:
            token_record = await get_user_token_jti(db, user_id, jti)

        if not token_record:
            return _unauthorized("账号已在其他地方登录")
        if token_record.expires_at <= datetime.now():
            return _unauthorized("token已过期")

        request.state.user_id = user_id
        request.state.username = payload.get("username")
        return await call_next(request)


# 解析token获取用户信息
async def get_current_user(
        authorization: str = Header(..., alias="authorization"),
        db: AsyncSession = Depends(get_db)
):
    token = authorization.replace("Bearer ", "")
    user = await get_token_user_info(db, token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='无效令牌')
    return user
