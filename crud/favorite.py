# @Version  : 1.0
# @Author   : 但成豪
# @File     : favorite.py
# @ Time    : 2026/2/5 16:27
from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.favorite import Favorite
from models.news import News


# 判断用户是否收藏了这一条新闻
async  def is_favorite(user_id:int,news_id:int,db:AsyncSession):
    query = select(Favorite).where(Favorite.user_id==user_id,Favorite.news_id==news_id)
    result = await db.execute(query)
    favorite = result.scalar_one_or_none()
    #是否收藏
    return favorite is not None
# 添加收藏
async def add_news_favorite(user_id :int,news_id:int,db: AsyncSession):

    favorite = Favorite(user_id= user_id,news_id=news_id)
    db.add( favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite
# 取消收藏
async def delete_news_favorite(user_id :int,news_id:int,db: AsyncSession):
    query = delete(Favorite).where(Favorite.user_id==user_id,Favorite.news_id==news_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0
# 查询用户收藏的列表
async def get_user_favorites(user_id:int,db: AsyncSession,page:int = 1,page_size:int = 10):
    #收藏总量
    count_query = select(func.count ()).where(Favorite.user_id==user_id)
    result = await db.execute(count_query)
    total =  result.scalar_one()
    # 联合查询获取收藏列表
    #联表查询样式：select(查询主体,别名).join(联合的表,Favorite.联合查询条件).where(查询条件)。order_by(排序条件)
    #别名样式  Favorite.created_at.label("favorite_time")
    offest = (page-1)*page_size
    query = (select(News,Favorite.created_at.label("favorite_time"),Favorite.id.label("favorite_id"))
             .join(Favorite,Favorite.news_id==News.id)
             .where(Favorite.user_id==user_id)
             .order_by(Favorite.created_at.desc())
             .offset(offest).limit(page_size))
    result = await db.execute(query)
    favorites = result.all()
    return favorites,total

async def remove_all_favorites(user_id:int,db: AsyncSession):
    query = delete(Favorite).where(Favorite.user_id==user_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount or 0