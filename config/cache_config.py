# @Version  : 1.0
# @Author   : 但成豪
# @File     : news_cache.py
# @ Time    : 2026/3/19 21:08
from typing import Any

import redis.asyncio as redis
from pydantic import json

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
redis_client = redis.Redis(
    host = REDIS_HOST, # Redis服务器的IP地址
    port = REDIS_PORT, # Redis服务端口
    db = REDIS_DB,  # Redis数据库编号 0-15
    decode_responses = True #是否将字节数据解码
)

#取字符串
async def get_cache(key:str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取字符串失败，{e}")
        return None
#获取字典和列表
async def get_json_cache(key:str):
    try:
        data =  await redis_client.get(key)
        if data:
            return json.loads(data)#序列化数据，将带引号的字典或列表的引号去掉
    except Exception as e:
        print(f"获取JSON失败，{e}")
        return None
#设置缓存
# async def set_cache(key:str,value:Any,expire:int=3600):
#     try:
#         if isinstance(value,(dict,list)):
#             value = json.dumps(value,ensure_ascii=False)#转换成JSON
#         await redis_client.setex(key,expire,value)
#         return True
#     except Exception as e:
#         print(f"设置缓存失败，{e}")
#         return False
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        # 关键修改：判断value是否已是字符串，是则直接用；否则仅对非字符串类型序列化
        if isinstance(value, str):
            final_value = value  # 已是字符串，直接用
        elif isinstance(value, (dict, list)):
            # 若传入的是字典/列表（如jsonable_encoder后的结果），直接转字符串（非JSON序列化）
            final_value = str(value)
        else:
            # 其他类型（如int/对象），转字符串兜底
            final_value = str(value)

        await redis_client.setex(key, expire, final_value)
        return True
    except Exception as e:
        print(f"设置缓存失败，{e}")
        return False
