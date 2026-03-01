# @Version  : 1.0
# @Author   : 但成豪
# @File     : response.py
# @ Time    : 2026/2/3 13:20

from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(message: str ,data= None):
    content ={
        'code': 200,
        'message': message,
        'data': data
    }
    return JSONResponse(content = jsonable_encoder(content))
