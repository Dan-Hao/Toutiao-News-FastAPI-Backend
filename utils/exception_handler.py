# @Version  : 1.0
# @Author   : 但成豪
# @File     : exception_handler.py
# @ Time    : 2026/2/3 17:33
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from utils.exceptiom import http_exception_handler, integrity_error_handler, sqlalchemy_error_handler, \
    general_exception_handler


def register_exception_handler(app):
    """
    注册全局异常处理
    """
    app.add_exception_handler(HTTPException,http_exception_handler)#捕获HTTPException异常
    app.add_exception_handler(IntegrityError,integrity_error_handler)#数据完整性异常
    app.add_exception_handler(SQLAlchemyError,sqlalchemy_error_handler)#数据库异常
    app.add_exception_handler(Exception,general_exception_handler )