# @Version  : 1.0
# @Author   : 但成豪
# @File     : favorite_news.py
# @ Time    : 2026/2/5 15:45
from fastapi import APIRouter, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud.favorite import is_favorite, add_news_favorite, delete_news_favorite, get_user_favorites, remove_all_favorites
from config.db_config import get_db
from models.users import User
from schemas.favorite import FavoriteResponse, FavoriteAddRequest, FavoriteListResponse
from utils.response import success_response
from crud.jwt import  get_current_user
from fastapi import Depends

router = APIRouter(prefix="/api/favorite", tags=["favorite_news"])
@router.get("/check")
async def check_favorite(news_id:int = Query(...,alias = "newsId"),
                         current_user: User = Depends(get_current_user) ,
                         db: AsyncSession = Depends(get_db)
):
    """检查用户是否收藏了该新闻"""
    favorite = await is_favorite(current_user.id,news_id,db)
    return success_response(message="检查收藏状态成功",data=FavoriteResponse(isFavorite= favorite))

@router.post("/add")
async def add_favorite(data:FavoriteAddRequest,
                       current_user: User = Depends(get_current_user) ,
                       db: AsyncSession = Depends(get_db)
):
    """添加收藏"""
    favor =await add_news_favorite(current_user.id,data.news_id,db)
    return success_response(message="收藏成功",data=favor)
@router.delete("/remove")
async def remove_favorite(news_id:int = Query(...,alias = "newsId"),
                          current_user: User = Depends(get_current_user) ,
                          db: AsyncSession = Depends(get_db)
):
    result = await delete_news_favorite(current_user.id,news_id,db)
    if not result:
        raise HTTPException(status_code=404, detail="收藏不存在")
    return success_response(message="取消收藏成功")
@router.get("/list")
async def get_favorite_list(page : int = Query(1,ge=1),
                            page_size :int = Query(10,ge=1,le=100,alias="pageSize"),
                            current_user: User = Depends(get_current_user) ,
                            db: AsyncSession = Depends(get_db)
):
    """获取用户收藏列表"""
    favorite,total = await get_user_favorites(current_user.id,db,page,page_size)
    news_list = [{
        **news.__dict__,
        "favorite_time": favorite_time,
        "favorite_id": favorite_id
    }for news,favorite_time,favorite_id in favorite]
    has_more= total > page * page_size
    data = FavoriteListResponse(list=news_list,total=total,hasMore=has_more)
    return success_response(message="获取收藏列表成功", data=data)

@router.delete("/clear")
async def clear_favorite(current_user: User = Depends(get_current_user) ,
                         db: AsyncSession = Depends(get_db)
):
    """清空收藏"""
    all_count = await remove_all_favorites(current_user.id,db)
    return success_response(message=f"清空{all_count}条收藏成功")