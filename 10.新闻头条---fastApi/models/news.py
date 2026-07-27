from datetime import datetime
from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, DateTime, String, Text, Index


class Base(DeclarativeBase):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment='创建时间')
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now,
                                                 comment='更新时间')


class Category(Base):
    __tablename__ = "news_category"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='分类id')
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment='分类名称')
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment='排序')


class NewsList(Base):
    __tablename__ = "news"
    #构建表索引
    __table_args__ = (
        Index('fx_new_category_idx', 'category_id'),
        Index('idx_publish_time', 'publish_time'),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='新闻Id')
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment='新闻标题')
    description: Mapped[Optional[str]] = mapped_column(String(500), comment='新闻描述')
    content: Mapped[str] = mapped_column(Text, comment='新闻内容')
    image: Mapped[Optional[str]] = mapped_column(String(255), comment='新闻封面')
    author: Mapped[Optional[str]] = mapped_column(String(50), comment='新闻作者')
    category_id: Mapped[int] = mapped_column(Integer, comment='新闻分类ID')
    views: Mapped[int] = mapped_column(Integer, comment='新闻评论数量')
    publish_time: Mapped[datetime] = mapped_column(DateTime, comment='新闻发表时间')

    def __repr__(self):
        return (f'<NewsList(id={self.id},'
                f' title={self.title},description={self.description},content={self.content},image={self.image},'
                f' author={self.author},category_id={self.category_id}, views={self.views},publish_time={self.publish_time})>')
