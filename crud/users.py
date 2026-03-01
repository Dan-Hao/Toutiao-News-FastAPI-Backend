# @Version  : 1.0
# @Author   : 但成豪
# @File     : users.py
# @ Time    : 2026/2/2 15:10
from fastapi import Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.jwt import get_current_user
from models.users import User
from schemas.users import UserRequest, UserUpdate, UserChangePassword
from utils import  security

#根据用户名查询用户
async def get_user_by_username(username: str, db: AsyncSession):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

#创建用户，已有用户则创建失败,创建时用passlib加密
async def create_user(userdata: UserRequest, db: AsyncSession):
    hash_pwd = security.get_password_hash(userdata.password)
    user = User(username=userdata.username, password= hash_pwd)
    db.add(user)
    await db.commit()
    await db.refresh(user) #获取当前写入最新的user
    return user
#更新用户信息，通过依赖注入验证token，userdata是一个pydantic，需要**来解包
async def update_user(userdata: UserUpdate, db: AsyncSession,username: str):
    stmt = update(User).where(User.username == username).values(**userdata.model_dump(
        exclude_unset=True,
        exclude_none= True
    ))
    result = await db.execute(stmt)
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    updated_user = await get_user_by_username(username, db)
    return updated_user

async def change_password(db: AsyncSession,user:User, old_password: str, new_password: str ):
        # 验证旧密码
        if not security.verify_password(old_password, user.password):
            return  False

        # 更新密码
        new_hash_pwd = security.get_password_hash(new_password)
        user.password = new_hash_pwd
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return True