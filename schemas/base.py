# @Version  : 1.0
# @Author   : 但成豪
# @File     : base.py
# @ Time    : 2026/2/5 19:36
from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel, ConfigDict


class NewsItemBase(BaseModel):
    id: int
    title: str
    description: Optional [str] = None
    image: Optional [str] = None
    author: Optional [str] = None
    category_id : int = Field (alias="categorId")
    views: int
    publish_time: Optional [datetime] = Field (None, alias= "publishedTime" )
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)