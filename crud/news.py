# @Version  : 1.0
# @Author   : 但成豪
# @File     : news.py
# @ Time    : 2026/1/16 13:49
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession


from models.news import News ,Category


async def get_categoreis(db: AsyncSession,skip: int = 0, limit: int = 100):
        stmt = select(Category).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()
async def get_news_list(db: AsyncSession,category_id: int,skip: int=0 , limit: int = 10):
        stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()
async def get_news_count(db: AsyncSession,category_id: int):
        stmt = select(func.count(News.id)).where(News.category_id == category_id)
        result = await db.execute(stmt)
        return result.scalar_one()
async def get_news_detail(db: AsyncSession,news_id: int):
        stmt = select(News).where(News.id == news_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
async def crease_news_views(db: AsyncSession,news_id: int):
        stmt = update(News).where(News.id == news_id).values(views=News.views+1)
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount >0
async def get_related_news(db: AsyncSession,news_id: int,category_id,limit: int = 5):
        stmt = (select(News).where(
        News.id != news_id,News.category_id == category_id).order_by(
                News.views.desc()
        ).limit(limit))
        result = await db.execute(stmt)
        relate_news =  result.scalars().all()
        return [{
                'id': related_news.id,
                'title': related_news.title,
                'image': related_news.image,
                'author': related_news.author,
                'publishTime': related_news.publish_time,
                'categoryId': related_news.category_id,
                'views': related_news.views,
                'relatedNews': []
        }for related_news in relate_news]