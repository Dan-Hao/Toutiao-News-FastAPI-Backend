# @Version  : 1.0
# @Author   : 但成豪
# @File     : news.py
# @ Time    : 2026/1/16 12:32
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud import news

from config.db_config import get_db

router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100,db:AsyncSession = Depends(get_db)):
   categories = await news.get_categoreis( db,skip, limit)
   return {
        'code' :200,
        "message": "获取分类成功",
        'data':categories
         }
@router.get("/list")
async def get_news_list(
        category_id: int = Query(...,alias="categoryId"),
        page: int = 1,
        page_size: int = Query(...,alias="pageSize",le=100),
        db:AsyncSession = Depends(get_db)
):
    offset = (page -1)*page_size #跳过的数量
    news_lists= await news.get_news_list(db,category_id,offset,page_size)
    total = await news.get_news_count(db,category_id)
    has_more = (offset + len(news_lists))<total
    return {
        'code' :200,
        "message": "获取新闻列表成功",
        'data':{
            "list": news_lists,
            "total":total,
            "hasMore":has_more
        }
    }
@router.get("/detail")
async def get_news_detail(
        news_id: int = Query(...,alias="id"),
        db:AsyncSession = Depends(get_db)
):
    news_detail = await news.get_news_detail(db,news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")
    views_res =await news.crease_news_views(db,news_detail.id)
    if not views_res:
        raise HTTPException(status_code=404, detail="新闻不存在")
    related_news = await news.get_related_news(db,news_detail.id,news_detail.category_id)
    return {
        'code' :200,
        "message": "获取新闻详情成功",
        'data': {
        'id': news_detail.id,
        'title': news_detail.title,
        'content':news_detail.content,
        'image':news_detail.image,
        'author':news_detail.author,
        'publishTime':news_detail.publish_time,
        'categoryId': news_detail.category_id,
        'views':news_detail.views,
        'relatedNews': related_news,
        }
    }