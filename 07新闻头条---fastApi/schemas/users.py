from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class UserRequest(BaseModel):
    username: str
    password: str


class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description='昵称')
    avatar: Optional[str] = Field(None, max_length=255, description='头像')
    gender: Optional[str] = Field(None, max_length=10, description='性别')
    bio: Optional[str] = Field(None, max_length=500, description='个人简介')
    phone: Optional[str] = Field(None, max_length=11, description='手机号')


class UserInfoResponse(UserInfoBase):
    id: int
    username: str
    model_config = ConfigDict(
        from_attributes=True
    )


class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias='user_info')
    model_config = ConfigDict(
        populate_by_name=True,  # alias/字段名兼容
        from_attributes=True  # 允许orm对象属性中取值
    )


class PasswordClass(BaseModel):
    id: int = Field(..., description='用户id')
    old_password: str = Field(..., description='旧密码')
    new_password: str = Field(..., description='新密码')
