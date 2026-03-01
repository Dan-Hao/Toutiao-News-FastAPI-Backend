# @Version  : 1.0
# @Author   : 但成豪
# @File     : db_config.py
# @ Time    : 2026/1/16 12:48
from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker,create_async_engine

ASYNC_DATABASE_URL = "mysql+aiomysql://root:Dch123456789@localhost:3306/news_app?charset=utf8"
#创建数据库引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo = True,
    pool_size= 5,
    max_overflow=20,
)
AsyncsSessionLocal = async_sessionmaker (
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
async def get_db():
    async with AsyncsSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
