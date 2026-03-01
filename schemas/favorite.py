# @Version  : 1.0
# @Author   : 但成豪
# @File     : favorite.py
# @ Time    : 2026/2/5 16:37
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


class FavoriteResponse(BaseModel):
    """是否收藏响应模型"""
    is_favorite: bool = Field(..., description="是否收藏",alias="isFavorite")

class FavoriteAddRequest(BaseModel):
    """收藏请求模型"""
    news_id: int = Field(..., description="新闻ID",alias="newsId")

class FavoriteNewsItemResponse(NewsItemBase):
    """收藏新闻项响应模型"""
    favorite_id:int = Field(alias="favoriteId")
    favorite_time: datetime = Field(alias="favoriteTime")
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class FavoriteListResponse(BaseModel):
    """收藏列表响应模型"""
    list: list[FavoriteNewsItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")
    model_config = ConfigDict(populate_by_name=True,from_attributes= True)