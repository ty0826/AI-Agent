from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Integer, String, Enum, Index, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    pass


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        Index('user_name_id', 'username'),
        Index('user_name_password', 'password'),
    )
    # unique不能重复 nullable必须要有值
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment='用户姓名')
    password: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, comment='用户密码')
    nickname: Mapped[Optional[str]] = mapped_column(String(50), comment='用户昵称')
    avatar: Mapped[Optional[str]] = mapped_column(String(255), comment='用户头像')
    gender: Mapped[Optional[str]] = mapped_column(Enum('male', 'female', 'unknown'), comment='用户性别',
                                                  default='unknown')
    bio: Mapped[Optional[str]] = mapped_column(String(500), comment='个人简介', default='用户很懒，什么都没留下 ')
    phone: Mapped[Optional[str]] = mapped_column(String(20), unique=True, comment='手机号')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment='创建时间')
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now,
                                                 comment='更新时间')

    def __repr__(self):
        return f'<User(id={self.id},username={self.username})>'


class UserToken(Base):
    __tablename__ = 'user_token'
    __table_args__ = (
        Index('user_token_id', 'id'),
        Index('user_user_id', 'user_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='tokenID')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment='用户ID')
    token: Mapped[str] = mapped_column(String(255), nullable=False, comment='令牌')
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment='过期时间')
    created_at: Mapped[datetime] = mapped_column(DateTime, comment='创建时间')
