# @Version  : 1.0
# @Author   : 但成豪
# @File     : news.py
# @ Time    : 2026/1/16 13:49
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news_cache import get_categories_cache, set_categories_cache, get_news_list_cache, set_news_list_cache, \
        get_news_detail_cache, set_related_news_cache, set_news_detail_cache, get_related_news_cache
from models.news import News ,Category
from schemas.base import NewsItemBase
from schemas.news import NewsDetailResponse, RelatedNewsResponse


async def get_categoreis(db: AsyncSession,skip: int = 0, limit: int = 100):
        #先从缓存中找新闻列表
        data = await get_categories_cache()
        if data:
                return data
        # 如果缓存中没有，则从数据库中获取
        stmt = select(Category).offset(skip).limit(limit)
        result = await db.execute(stmt)
        categories = result.scalars().all()
        #找到后，在缓存里写入
        if categories:
                categories =jsonable_encoder(categories)
                await set_categories_cache(categories)
        #返回
        return categories

async def get_news_list(db: AsyncSession,category_id: int,skip: int=0 , limit: int = 10):
        #先从缓存中找新闻列表
        #skip = (page -1)*page_size 则页码page = skip/limit + 1
        page = skip//limit + 1
        cache_list = await get_news_list_cache(category_id, page, limit)
        if cache_list:
                return [News(**item)for item in cache_list]#转换成模型类orm对象
        #如果缓存没有，在数据库里查
        stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
        result = await db.execute(stmt)
        news_list=  result.scalars().all()
        #设置缓存
        #先将模型类orm对象转换成pydantic , 再转换成字典
        if news_list:
                news_list = [NewsItemBase.model_validate(item).
                             model_dump(mode = "json",by_alias = False)
                             for item in news_list]
                news_list = jsonable_encoder(news_list)
                await set_news_list_cache(category_id, page, limit, news_list)
        return news_list

async def get_news_count(db: AsyncSession,category_id: int):
        stmt = select(func.count(News.id)).where(News.category_id == category_id)
        result = await db.execute(stmt)
        return result.scalar_one()
async def get_news_detail(db: AsyncSession,news_id: int):
        #缓存查找
        news_detail = await get_news_detail_cache(news_id)
        if news_detail:
                return news_detail
        #如果没有，则从数据库中查
        stmt = select(News).where(News.id == news_id)
        result = await db.execute(stmt)
        news_detail_cache = result.scalar_one_or_none()
        #重新设置缓存
        #orm对象转换为pydantic后转为json
        # 构造新闻详情数据用于缓存（包含 content 字段）
        # news_dict = {k: v for k, v in news.__dict__.items() if not k.startswith('_')}
        if news_detail_cache:
                news_dict = NewsDetailResponse.model_validate(news_detail_cache).model_dump(
                        by_alias=False, mode="json", exclude={'related_news'} )
                await set_news_detail_cache(news_id,news_dict)
        return news_detail_cache
async def crease_news_views(db: AsyncSession,news_id: int):
        stmt = update(News).where(News.id == news_id).values(views=News.views+1)
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount >0
async def get_related_news(db: AsyncSession,news_id: int,category_id,limit: int = 5):
        cached_related = await get_related_news_cache(news_id, category_id)
        if cached_related:
                return cached_related
        stmt = (select(News).where(
        News.id != news_id,News.category_id == category_id).order_by(
                News.views.desc()
        ).limit(limit))
        result = await db.execute(stmt)
        related_news =  result.scalars().all()
        if related_news:
                related_data = [
                        RelatedNewsResponse.model_validate(news).model_dump(by_alias=False, mode="json")
                        for news in related_news
                ]
                await set_related_news_cache(news_id, category_id, related_data)
                return related_data

                # 没有相关新闻，返回空列表
        return []