# @Version  : 1.0
# @Author   : 但成豪
# @File     : users.py
# @ Time    : 2026/2/2 14:10
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class UserRequest(BaseModel):
    username: str
    password: str

class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None,max_length=50,description="昵称")
    avatar: Optional[str] = Field(None,max_length=255,description="头像")
    gender: Optional[str] = Field(None,max_length=10,description="性别")
    bio: Optional[str] = Field(None,max_length=500,description="个人简介")

class UserResponse(UserInfoBase):
    """用户信息返回数据模型"""
    id: int
    username: str

    model_config = ConfigDict(
        from_attributes=True,
    )

class UserAuthResponse(BaseModel):
    """用户认证返回数据模型"""
    token: str
    user_info:UserResponse = Field( ...,alias="userInfo" )

    model_config = ConfigDict(
        from_attributes=True,   #取值
        populate_by_name=True   #字段名兼容
    )

class UserUpdate(BaseModel):
    """用户更新数据模型"""
    nickname: str = None
    avatar: str = None
    gender: str =None
    bio: str = None
    phone: str = None

class UserChangePassword(BaseModel):
    """用户修改密码数据模型"""
    old_password: str = Field(...,alias="oldPassword",description="旧密码")
    new_password: str = Field(...,min_length= 6,alias="newPassword",description="新密码")
