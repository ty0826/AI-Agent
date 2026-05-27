from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import DateTime, func, String, Float, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, result
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()

# 创建异步引擎
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@127.0.0.1:3306/fastapi_test?charset=utf8"
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,  # 输出SQL日志
    pool_size=10,  # 设置连接池中保持的持久连接数
    max_overflow=20,  # 设置连接池允许创建的额外连接数
)

##定义模型类：基类+表对应的模型类
##基类：创建时间、更新时间；书籍表：id，书名、作者、价格、出版社
"""
1、基类：相当于就是复用，可以被其他模型类继承，容易维护
2、Mapped:python标注类型
3、mapped_column:数据库字段配置
4、dafault:默认值
5、insert_default:插入sql时的默认值
6、onupdate：更新时自动执行
"""


class Base(DeclarativeBase):
    __abstract__ = True  ##表示抽象基类，不生成表
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now(),
                                                  comment='创建时间')
    update_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now(),
                                                  onupdate=func.now(), comment='更新时间')


class Book(Base):
    __tablename__ = 'book'
    id: Mapped[int] = mapped_column(primary_key=True, comment='书籍ID')
    book_name: Mapped[str] = mapped_column(String(255), comment='书名')
    author: Mapped[str] = mapped_column(String(255), comment='作者')
    price: Mapped[float] = mapped_column(Float, comment='书本价格')
    publisher: Mapped[str] = mapped_column(String(255), comment='出版社')
    mark: Mapped[str] = mapped_column(String(255), comment='备注')


async def create_tables():
    # 创建一个异步数据库链接
    async with async_engine.begin() as conn:
        ##Base.metadata.create_all扫描所有继承Base的模型
        await  conn.run_sync(Base.metadata.create_all)


##程序启动命令，一启动就创建数据库
@app.on_event('startup')
async def startup():
    await create_tables()


# 获取数据库会话
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 绑定数据库引擎
    class_=AsyncSession,  # 指定会话类
    expire_on_commit=False,  # 提交后会话不过期，不会重新查询数据库
)


# 创建依赖项
async def get_database():
    async with AsyncSessionLocal() as session:
        try:
            yield session  # 返回数据库会话给处理函数
            await session.commit()  # 提交事务
        # except Exception as e:
        #     await  session.rollback()  # 异常就回滚
        finally:
            await session.close()  # 会话关闭


@app.post("/book/query")
async def book_query(id: int, db: AsyncSession = Depends(get_database)):
    # result = await db.execute(select(Book))
    # book = result.scalars().all()##查询所有数据
    # book= result.scalars().first()#获取第一条数据
    # book = await db.get(Book, id)#获取某条数据

    """
    比较判断：==、>、<、>=、<=
    模糊查询：like()
    与非查询：&、|、~
    包含查询：in_()
    """
    result = await db.execute(select(Book).where(id == Book.id))
    book = result.scalar_one_or_none()  # 返回一条，运行None
    return book


##条件价格大于等于price
@app.post("/book/query_price")
async def book_query_price(price: float, database: AsyncSession = Depends(get_database)):
    result = await database.execute(select(Book).where(Book.price <= price))
    book = result.scalars().all()  # 返回多条
    return book


##模糊查询
class BookQuery(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = 0
    id_list: Optional[list[int]] = []


@app.post("/book/query_author")
async def book_query_anthor(data: BookQuery, db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book).where(Book.author.like(data.name + '_')))  # name后面一个字符，以此类推
    result = await db.execute(select(Book).where(Book.author.like(data.name + '%')))  # 以name开头
    result = await db.execute(select(Book).where(Book.author.like('%' + data.name)))  # 以name结尾的
    result = await db.execute(select(Book).where(Book.author.like(data.name + '%') | (Book.price >= data.price)))
    result = await db.execute(select(Book).where(Book.id.in_(data.id_list)))
    book = result.scalars().all()
    return book


@app.post('/book/count')
async def book_count(db: AsyncSession = Depends(get_database)):
    """
    func的方法例子
    """
    result = await  db.execute(select(func.count(Book.id)))  # 总数
    result = await  db.execute(select(func.max(Book.price)))  # 最大
    result = await db.execute(select(func.min(Book.price)))  # 最小
    result = await  db.execute(select(func.avg(Book.price)))  # 平均
    result = await db.execute(select(func.sum(Book.price)))  # 总数
    book = result.scalar()  # 用来提取一个数值
    return book


# 分页查询
@app.post('/book/page_query')
async def book_page_book(page: Optional[int] = 0, page_size: Optional[int] = 3,
                         db: AsyncSession = Depends(get_database)):
    skip = (page - 1) * page_size
    result = await  db.execute(select(Book).offset(skip).limit(page_size))
    book = result.scalars().all()
    return book


# 新增操作add
class BookBase(BaseModel):
    id: Optional[int] = None
    name: str
    author: str
    price: float
    publisher: str
    mark: str


@app.post('/book/book_add')
async def book_add(data: BookBase, db: AsyncSession = Depends(get_database)):
    db.add(Book(
        book_name=data.name,
        author=data.author,
        price=data.price,
        publisher=data.publisher,
    ))
    await  db.commit()
    return data


# 更新----先查询----在赋值修改
@app.post('/book/book_update')
async def book_update(update_data: BookBase, db: AsyncSession = Depends(get_database)):
    book = await  db.get(Book, update_data.id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    book.book_name = update_data.name
    book.author = update_data.author
    book.price = update_data.price
    book.publisher = update_data.publisher
    book.mark = update_data.mark
    await db.commit()
    return book


# 删除
@app.post('/book/book_delete')
async def book_delete(book_id: int, db: AsyncSession = Depends(get_database)):
    book = await  db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    await db.delete(book)
    await db.commit()
    return {"message": f"{book.book_name} 删除成功！"}
