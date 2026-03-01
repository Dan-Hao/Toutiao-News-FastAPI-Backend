# @Version  : 1.0
# @Author   : 但成豪
# @File     : security.py
# @ Time    : 2026/2/2 15:27
import hashlib
from passlib.context import CryptContext

# 强制使用 bcrypt 库的特定版本
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b"  # 强制使用 2b 版本
)

def get_password_hash(password: str) -> str:
    """加密密码（解决bcrypt 72字节限制）"""
    sha256_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pwd_context.hash(sha256_hash)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    sha256_hash = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    return pwd_context.verify(sha256_hash, hashed_password)