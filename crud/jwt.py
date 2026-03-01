# @Version  : 1.0
# @Author   : 但成豪
# @File     : jwt.py
# @ Time    : 2026/2/2 17:36
from datetime import datetime, timedelta
from typing import  Dict, Any

from fastapi import HTTPException, Depends
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from config.jwt_config import settings

from models.users import UserToken, User


async def create_access_token(
    data: Dict[str, Any],
    db: AsyncSession,
    user_id: int
) -> str:
    to_encode = data.copy()
    # 1. 生成JWT标准的过期时间（UTC时间，必须！避免时区/库校验偏差）
    expire = datetime.utcnow()+ timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # 2. 写入JWT payload，保证和数据库expires_at完全一致
    to_encode.update({"exp": expire, "user_id": user_id})  # 额外写入user_id，方便后续解析JWT直接获取
    # 3. 生成JWT Token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    # 4. 检索用户的现有Token记录
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        # 有记录：更新Token和过期时间，**必须提交/刷新**，否则更新不生效
        user_token.token = encoded_jwt
        user_token.expires_at = expire
        await db.flush()  # 轻量刷入数据库，不新建事务（推荐），也可用await db.commit()
    else:
        # 无记录：新增Token记录，提交事务
        new_token = UserToken(
            user_id=user_id,
            token=encoded_jwt,
            expires_at=expire
        )
        db.add(new_token)
        await db.commit()  # 新增必须commit，保证数据持久化
        await db.refresh(new_token)  # 可选，刷新对象获取数据库自增字段（如id）

    return encoded_jwt




from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
security = HTTPBearer(auto_error= False)
from fastapi import Request

async def decode_access_token(
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    兼容两种 Authorization：
    1. Authorization: Bearer <token>
    2. Authorization: <token>
    """

    token: str | None = None

    # 情况 1：标准 Bearer（HTTPBearer 解析成功）
    if credentials:
        token = credentials.credentials

    # 情况 2：前端直接传 token（无 Bearer）
    if not token:
        auth_header = request.headers.get("authorization")
        if auth_header:
            token = auth_header

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # 1. 解码 JWT
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: int = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证凭证",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. 数据库校验 token 是否存在
    query = select(UserToken).where(
        UserToken.user_id == user_id,
        UserToken.token == token
    )
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if not user_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 不存在或已失效",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. 校验过期时间
    if user_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


#依赖注入函数
async def get_current_user(
        payload: Dict[str, Any] = Depends(decode_access_token),
        db: AsyncSession = Depends(get_db)
) -> User:
    """
    获取当前登录用户
    """
    user_id = payload.get("user_id")

    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user