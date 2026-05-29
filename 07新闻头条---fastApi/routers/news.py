from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud.news import get_book_list, get_category, get_news_count, get_news_detail, update_news_detail, get_related_news
from utils.response import success_response
from pydantic import BaseModel, Field

router_news = APIRouter(prefix="/api/news", tags=["news"])
"""
Query:参数跟在地址后面
Body:参数放在请求体里
"""


##新闻类型分类
@router_news.post("/category")
async def get_news_category(
        db: AsyncSession = Depends(get_db),
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
):
    res = await get_category(db, page, limit)
    return success_response(data=res)


class NewsQuery(BaseModel):
    page: int = Field(1, alias='pageCurrent', description='当前页数')
    limit: int = Field(10, alias='pageSize', description='一页条数')
    category_id: int = Field(..., alias='categoryId', description='分类ID')


# 获取新闻列表
@router_news.post("/news_list")
async def get_news_list(
        data: NewsQuery,
        db: AsyncSession = Depends(get_db),

):
    res = await get_book_list(db, data.page, data.limit, data.category_id)
    count = await get_news_count(db, data.category_id)
    return success_response(data={
        "data": res,
        "total": count,
    })


class detailClass(BaseModel):
    new_id: int = Field(..., alias='newId')
    category_id: int = Field(..., alias='categoryId')


# 获取新闻详情
@router_news.post("/news_details")
async def get_news_details(data: detailClass, db: AsyncSession = Depends(get_db)):
    res = await get_news_detail(db, data.new_id)
    if not res:
        raise HTTPException(status_code=500, detail="news is null")
    await  update_news_detail(db, data.new_id)
    relateList = await  get_related_news(db, data.new_id, data.category_id)
    return success_response(data={
        'data': res,
        'relateList': relateList
    })
