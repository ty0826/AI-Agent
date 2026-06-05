from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 密码加密
def get_hash_password(password: str):
    return pwd_context.hash(password)

#密码验证
def verify_password(plain_password, hashed_password):
    #plain_password明文密码 hashed_password加密密码
    return pwd_context.verify(plain_password, hashed_password)