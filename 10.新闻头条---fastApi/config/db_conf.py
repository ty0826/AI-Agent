from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

ASYNC_DATABASE_URl = 'mysql+aiomysql://root:123456@127.0.0.1:3306/news_app?charset=utf8'

async_engine = create_async_engine(
    ASYNC_DATABASE_URl,
    echo=True,
    pool_size=10,
    max_overflow=20,
)

AsyncSession = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSession() as session:
        try:
            yield session
            await session.commit()
        finally:
            await session.close()
