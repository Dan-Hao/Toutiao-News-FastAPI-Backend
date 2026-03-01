# @Version  : 1.0
# @Author   : 但成豪
# @File     : jwt_config.py
# @ Time    : 2026/2/2 17:38
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # JWT配置
    SECRET_KEY: str ="9V6FhZ2aNqE8M0LrYkX4cWmP3JtIuB_oGd7S5eR1HKA"  # 生产环境必须改成随机密钥
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天

    class Config:
        env_file = ".env"

settings = Settings()