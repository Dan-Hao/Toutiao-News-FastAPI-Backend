# @Version  : 1.0
# @Author   : 但成豪
# @File     : history.py
# @ Time    : 2026/2/6 15:31

from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


class HistoryAddRequest(BaseModel):

    news_id: int = Field(...,alias="newsId")

class HistoryResponse(NewsItemBase):
    """历史记录时间和id模型,继承新闻表类"""
    history_id: int = Field(alias="historyId")
    view_time: datetime = Field(alias="viewTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True)

class HistoryListResponse(BaseModel):
    """历史记录新闻响应模型"""
    list: list[HistoryResponse]
    total: int
    has_more: bool = Field(alias="hasMore")
    model_config = ConfigDict(populate_by_name=True,from_attributes= True)