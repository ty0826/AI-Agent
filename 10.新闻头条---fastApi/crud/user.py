from datetime import datetime
from sqlalchemy import select, delete, update
from models.user import User, UserToken
from schemas.users import UserInfoResponse, PasswordClass
from utils.security import get_hash_password, verify_password
from sqlalchemy.ext.asyncio import AsyncSession


# 查询用户唯一性
async def check_user(db: AsyncSession, username):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    return user


# 添加用户
async def add_user(db: AsyncSession, username, password):
    hashed_password = get_hash_password(password)
    add_user = User(username=username, password=hashed_password)
    db.add(add_user)
    await db.commit()
    return add_user


# 用户登陆
async def login_user(db: AsyncSession, username, password):
    login_user = await check_user(db, username)
    if not login_user:
        return None
    if not verify_password(password, login_user.password):
        return None
    return login_user


# 保存token
async def save_user_token_jti(db: AsyncSession, user_id: int, jti: str, expires_at: datetime):
    await db.execute(delete(UserToken).where(UserToken.user_id == user_id))
    token_record = UserToken(
        user_id=user_id,
        token=jti,
        expires_at=expires_at,
        created_at=datetime.now(),
    )
    db.add(token_record)
    await db.commit()
    return token_record


# 查询token
async def get_user_token_jti(db: AsyncSession, user_id: int, jti: str):
    stmt = select(UserToken).where(UserToken.user_id == user_id, UserToken.token == jti)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 根据token查询用户
async def get_token_user_info(db: AsyncSession, token):
    query = select(UserToken).where(UserToken.token == token)
    db_token = (await db.execute(query)).scalar_one_or_none()
    if not db_token or db_token.expires_at < datetime.now():
        return None
    return (await db.execute(select(User).where(User.id == db_token.user_id))).scalar_one_or_none()


# 用户更新
async def update_userInfo(db: AsyncSession, data: UserInfoResponse):
    # user_record = await db.get(User, data.id)
    # if user_record is None:
    #     return None
    # user_record.username = data.username
    # user_record.nickname = data.nickname
    # user_record.avatar = data.avatar
    # user_record.gender = data.gender
    # user_record.bio = data.bio
    # user_record.phone = data.phone
    # await db.commit()
    # await db.refresh(user_record)
    query = update(User).where(User.id == data.id).values(
        **data.model_dump(
            exclude={'id'},  # 不更新的字段
            exclude_unset=True,  # 只更新前端传的字段
            exclude_none=True,  # 值为None的字段不更新
        )
    )
    await db.execute(query)
    await db.commit()
    return


async def update_password_service(db: AsyncSession, data: PasswordClass):
    query = await db.get(User, data.id)
    if query is None:
        raise ValueError('用户不存在！')
    if not verify_password(data.old_password, query.password):
        raise ValueError('账号密码不一致！')
    if verify_password(data.new_password, query.password):
        raise ValueError('新密码不能与旧密码一致！')
    stmt = update(User).where(User.id == data.id).values(
        password=get_hash_password(data.new_password),
    )
    await db.execute(stmt)
    await db.commit()
    return
