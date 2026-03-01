# @Version  : 1.0
# @Author   : 但成豪
# @File     : history.py
# @ Time    : 2026/2/6 15:27
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from config.db_config import get_db
from crud.history import add_news_history, get_history_list, clear_history, delete_history
from crud.jwt import get_current_user
from models.users import User
from schemas.history import HistoryAddRequest, HistoryListResponse, HistoryResponse
from utils.response import success_response

router = APIRouter(prefix="/api/history", tags=["history"])

@router.post("/add")
async def add_history(data:HistoryAddRequest,
                      current_user: User = Depends(get_current_user) ,
                      db: AsyncSession = Depends(get_db)
):
    """添加历史记录"""
    history = await add_news_history(data.news_id,current_user.id,db)
    return success_response(message="添加历史记录成功",data=history)

@router.get("/list")
async def get_history_news_list(page: int = Query(1, ge=1),
                           page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
                           user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    """
    获取历史记录列表
    """
    rows, total = await get_history_list(db, user.id, page, page_size)
    has_more = total> page * page_size
    history_list = [HistoryResponse.model_validate({
        **news.__dict__,
        "view_time": view_time,
        "history_id": history_id
    }) for news, view_time, history_id in rows]
    return success_response(message="获取历史记录成功", data=HistoryListResponse(list=history_list, total=total, hasMore=has_more))

@router.delete("/delete/{history_id}")
async def delete_news_history(history_id: int,
                         user: User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)):
    """
    删除历史记录
    """
    result = await delete_history(db, user.id, history_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="历史记录不存在")
    return success_response(message="删除成功")


@router.delete("/clear")
async def clear_history_all(user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    """
    清空历史记录
    """
    result = await clear_history(db, user.id)
    return success_response(message="清空成功")