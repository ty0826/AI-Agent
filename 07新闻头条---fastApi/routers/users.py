from fastapi import APIRouter, Depends, HTTPException, status
from config.db_conf import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from utils.auth import get_current_user
from utils.response import success_response
from utils.jwt import create_access_token
from crud.user import check_user, add_user, login_user, save_user_token_jti, update_password_service, update_userInfo
from schemas.users import UserRequest, UserAuthResponse, PasswordClass, UserInfoResponse

router_user = APIRouter(prefix="/api/users", tags=["用户相关"])


@router_user.post("/register")
async def register(data: UserRequest, db: AsyncSession = Depends(get_db)):
    existing = await check_user(db, data.username)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在!")
    await add_user(db, data.username, data.password)
    return success_response(message="注册成功！")


"""
model_vaildate():将数据类型转成Pydantic模型对象
model_dump():将模型对象转成dict
"""


@router_user.post("/login")
async def login(data: UserRequest, db: AsyncSession = Depends(get_db)):
    user = await login_user(db, data.username, data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户密码错误!")
    # 生成 token 并落库（同一用户重复登录会覆盖旧 token，保证单点登录）
    token_info = create_access_token(user.id, user.username)
    await save_user_token_jti(db, user.id, token_info["jti"], token_info["expires_at"])
    auth = UserAuthResponse(
        token=token_info["access_token"],
        user_info=UserInfoResponse.model_validate(user),
    )
    return success_response(message="登录成功！", data=auth.model_dump(by_alias=True))


@router_user.post("/user_info")
async def user_info(user: User = Depends(get_current_user)):
    return success_response(messages='获取用户信息成功！', data=UserInfoResponse.model_validate(user))


@router_user.post('/update_user_info')
async def update_user_info(data: UserInfoResponse,
                           db: AsyncSession = Depends(get_db)):
    await update_userInfo(db, data)
    return success_response(messages='用户更新成功！')


@router_user.post('/update_password')
async def update_password(data: PasswordClass, db: AsyncSession = Depends(get_db)):
    await update_password_service(db, data)
    return success_response(messages='密码更新成功！')
