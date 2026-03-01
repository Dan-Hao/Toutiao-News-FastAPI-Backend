# @Version  : 1.0
# @Author   : 但成豪
# @File     : users.py
# @ Time    : 2026/2/2 14:42
from sqlalchemy import String, Integer, Enum as SQLEnum, DateTime, Index, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from typing import Optional
import enum


class Base(DeclarativeBase):
    """数据库模型基类"""
    pass


class GenderEnum(str, enum.Enum):
    """性别枚举"""
    male = "male"
    female = "female"
    unknown = "unknown"


class User(Base):
    """用户信息表"""
    __tablename__ = "user"
    __table_args__ = (Index('idx_username', 'username'), Index('idx_phone', 'phone'),
                      {'comment': '用户信息表', 'mysql_charset': 'utf8mb4'})

    # 必填字段
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="用户名")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码(加密存储)")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp(),
                                                 comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp(),
                                                 onupdate=func.current_timestamp(), comment="更新时间")

    # 可选字段
    nickname: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="昵称")
    avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True,
                                                  default="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
                                                  server_default="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
                                                  comment="头像URL")
    gender: Mapped[Optional[GenderEnum]] = mapped_column(SQLEnum(GenderEnum, native_enum=False), nullable=True,
                                                         default=GenderEnum.unknown, server_default="unknown",
                                                         comment="性别")
    bio: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="个人简介")
    phone: Mapped[Optional[str]] = mapped_column(String(20), unique=True, nullable=True, comment="手机号")


class UserToken(Base):
    """用户令牌表"""
    __tablename__ = "user_token"
    __table_args__ = (Index('fk_user_token_user_idx', 'user_id'),
                      Index('token_UNIQUE',"token"))

    # 必填字段
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="令牌ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'),
                                         nullable=False, comment="用户ID")
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, comment="令牌值")
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="过期时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp(),
                                                 comment="创建时间")
