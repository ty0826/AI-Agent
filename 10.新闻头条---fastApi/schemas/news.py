from pydantic import BaseModel, Field


class NewsQuery(BaseModel):
    page: int = Field(1, alias='pageCurrent', description='当前页数')
    limit: int = Field(10, alias='pageSize', description='一页条数')
    category_id: int = Field(..., alias='categoryId', description='分类ID')


class detailClass(BaseModel):
    new_id: int = Field(..., alias='newId')
    category_id: int = Field(..., alias='categoryId')
