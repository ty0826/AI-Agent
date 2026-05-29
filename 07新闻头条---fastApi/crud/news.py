from fastapi import HTTPException
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, NewsList


# 获取新闻分类
async def get_category(db: AsyncSession, page: int, page_size: int):
    stmt = select(Category).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    return result.scalars().all()


# 获取新闻列表
async def get_book_list(db: AsyncSession, page: int, page_size: int, category_id: int):
    if category_id is None:
        raise ValueError("category_id is required")
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
    if new_id is None:
        raise ValueError("new_id is required")
    stmt = select(NewsList).where(NewsList.id == new_id)
    result = await db.execute(stmt)
    return result.scalars().all()


# 更新新闻
async def update_news_detail(db: AsyncSession, news_id: int):
    if news_id is None:
        raise ValueError("category_id is required")
    # news = await db.get(NewsList, news_id)
    # if news is None:
    #     raise HTTPException(code='500',detail='news not found')
    # news.views += 1
    await db.execute(
        update(NewsList)
        .where(NewsList.id == news_id)
        .values(views=NewsList.views + 1)
    )
    await  db.commit()
    return


async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    if category_id is None or news_id is None:
        raise ValueError("category_id or news_id is required")
    stmt = (
        select(NewsList)
        .where(NewsList.category_id == category_id, NewsList.id != news_id)
        .limit(limit)
        .order_by(NewsList.views.desc(), NewsList.publish_time.desc())
    )
    return (await db.execute(stmt)).scalars().all()
