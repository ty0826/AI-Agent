from datetime import datetime

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, NewsList
from cache.new_cache import get_category_cache, set_category_cache


# 获取新闻分类
async def get_category(db: AsyncSession, page: int, page_size: int):
    ###先从redis中获取，没有再查询
    data = await  get_category_cache('new:category')
    if data:
        return data
    stmt = select(Category).offset((page - 1) * page_size).limit(page_size)
    result = (await db.execute(stmt)).scalars().all()
    print('=======')
    if result:
        # jsonable_encoder:“Python对象”转换成“JSON 可序列化对象”
        await set_category_cache('new:category', jsonable_encoder(result), 3600)
    return result


# 获取新闻列表
async def get_book_list(db: AsyncSession, page: int, page_size: int, category_id: int):
    stmt = (
        select(NewsList, Category.name.label('category_name'))
        .join(Category, NewsList.category_id == Category.id)
        .where(NewsList.category_id == category_id)
        .offset((page - 1) * page_size)
        .limit(page_size).
        order_by(NewsList.publish_time.asc())
    )
    result = await db.execute(stmt)
    rows = result.all()  # result.scalars().all()只取第一列取决于select()有几项
    data = []
    # row=[(Newlist,category_name),(Newlist,category_name),(Newlist,category_name)....]
    for news, category_name in rows:
        item = news.__dict__.copy()
        item.pop("_sa_instance_state", None)
        item["category_name"] = category_name
        data.append(item)
    return data


# 获取新闻总数
async def get_news_count(db: AsyncSession, category_id: int):
    if category_id is None:
        raise ValueError("category_id is required")
    stmt = select(func.count(NewsList.id)).where(NewsList.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar()


##新闻详情
async def get_news_detail(db: AsyncSession, new_id: int):
    stmt = select(NewsList).where(NewsList.id == new_id)
    result = await db.execute(stmt)
    return result.scalars().all()


# 更新新闻
async def update_news_detail(db: AsyncSession, news_id: int):
    # news = await db.get(NewsList, news_id)
    # if news is None:
    #     raise HTTPException(code='500',detail='news not found')
    # news.views += 1
    result = await db.execute(
        update(NewsList)
        .where(NewsList.id == news_id)
        .values(views=NewsList.views + 1)
    )
    await  db.commit()
    return result.rowcount > 0


class NeesOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    author: str | None = None
    views: int
    title: str
    description: str | None = None
    image: str | None = None
    category_id: int

    created_at: datetime
    publish_time: datetime
    updated_at: datetime


async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    stmt = (
        select(NewsList)
        .where(NewsList.category_id == category_id, NewsList.id != news_id)
        .limit(limit)
        .order_by(NewsList.views.desc(), NewsList.publish_time.desc())
    )
    data = (await db.execute(stmt)).scalars().all()
    return [
        {
            "content": item.content,
            "id": item.id,
            "author": item.author,
            "views": item.views,
            "created_at": datetime.strftime(item.created_at, '%Y-%m-%d %H:%M:%S'),
            "title": item.title,
            "description": item.description,
            "image": item.image,
            "category_id": item.category_id,
            "publish_time": datetime.strftime(item.publish_time, '%Y-%m-%d %H:%M:%S'),
            "updated_at": datetime.strftime(item.updated_at, '%Y-%m-%d %H:%M:%S'),
        }
        for item in data
    ]
