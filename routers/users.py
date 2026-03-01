# @Version  : 1.0
# @Author   : 但成豪
# @File     : users.py
# @ Time    : 2026/2/2 13:19
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from datetime import  timedelta
from config.db_config import get_db
from models.users import User
from schemas.users import UserRequest, UserAuthResponse, UserResponse, UserUpdate, UserChangePassword
from crud.users import get_user_by_username, create_user, update_user, change_password
from crud.jwt import create_access_token, get_current_user
from utils.response import success_response
from utils.security import verify_password

router = APIRouter(prefix="/api/user", tags=["users"])


@router.post("/register")
async def register(userdata: UserRequest, db: AsyncSession = Depends(get_db)):
    """用户注册"""
    # 1. 检查用户是否存在
    await get_user_by_username(userdata.username, db)
    # 2. 创建用户（密码加密）
    user = await create_user(userdata, db)
    await db.refresh(user)
    # 3. 生成JWT token
    token_data = {
        "user_id": user.id,
        "username": user.username
    }
    access_token = await create_access_token(data=token_data,db=  db, user_id=user.id)

    # 4. 返回用户信息和token
    # 修改第42行代码如下：
    response_data = UserAuthResponse(token=access_token, userInfo=user)
    return success_response(message="注册成功",data =response_data)

@router.post("/login")
async def login(userdata: UserRequest, db: AsyncSession = Depends(get_db)):
    """用户登录"""
    # 1. 查询用户
    user = await get_user_by_username(userdata.username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 2. 验证密码
    if not verify_password(userdata.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 3. 生成JWT token
    token_data = {
        "user_id": user.id,
        "username": user.username
    }
    access_token = await create_access_token(data=token_data,db=  db, user_id = user.id)

    # 4. 返回用户信息和token
    return success_response(message="登录成功",data =UserAuthResponse(token=access_token, userInfo=user))

@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    """获取用户信息"""
    return success_response(message="获取用户信息成功",data =UserResponse.model_validate(user))

@router.put("/update")
async def update_user_info( userdata: UserUpdate,current_user: User = Depends(get_current_user),
                            db: AsyncSession = Depends(get_db)
):
    """更新用户信息"""
    # 1. 更新用户信息
    user= await update_user(userdata, db, current_user.username)
    return success_response(message="更新用户信息成功",data =UserResponse.model_validate(user))

@router.put("/password")
async def update_user_password( userdata: UserChangePassword ,db: AsyncSession = Depends(get_db),
                                current_user: User = Depends(get_current_user)
):
    """更新用户密码"""
    # 1. 验证旧密码
    res_change_password = await change_password(db,current_user, userdata.old_password, userdata.new_password)
    if not res_change_password:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="旧密码错误，修改失败"
        )
    return success_response(message="修改密码成功")