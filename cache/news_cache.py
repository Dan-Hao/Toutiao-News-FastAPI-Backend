# @Version  : 1.0
# @Author   : 但成豪
# @File     : news_cache.py
# @ Time    : 2026/3/20 16:38
from typing import List, Dict, Any, Optional

from config.cache_config import get_json_cache, set_cache


#获取新闻分类缓存
CATEGORIES_KEY= "news:categories"
NEWS_LIST_PREFIX = "news:list:"
NEWS_DETAIL_PREFIX = "news:detail:"
RELATED_NEWS_PREFIX = "news:related:"
async def get_categories_cache():
    return await get_json_cache(CATEGORIES_KEY)

#设置新闻缓存，变量有数据，过期时间
#分类，配置 缓存时间7200，列表 600 ，详情 1800 验证码 120
async def set_categories_cache(data:List[Dict[str,Any]],expire:int = 7200):
    return await set_cache(CATEGORIES_KEY,data,expire)

#封装新闻列表的设置缓存函数 新闻列表的key = news_list:category_id:页码：pase_size
# 参数还包括新闻列表和过期时间
async def set_news_list_cache(category_id:[Optional[int]],
                              page:int,page_size:int,
                              news_list:List[Dict[str,Any]],
                              expire:int = 1800):
    category_part = category_id if category_id else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{page_size}"
    return await set_cache(key,news_list,expire)
#获取新闻列表缓存
async def get_news_list_cache(category_id:[Optional[int]],page:int,page_size:int):
    category_part = category_id if category_id else "all"
    key = f"{NEWS_LIST_PREFIX}:{category_part}:{page}:{page_size}"
    return await get_json_cache(key)
#获取新闻详情缓存
async def get_news_detail_cache(news_id:int):
    key = f"{NEWS_DETAIL_PREFIX}{news_id}"
    return await get_json_cache(key)

#设置新闻详情缓存
async def set_news_detail_cache(news_id:int,news_detail:Dict[str,Any],expire:int = 1800):
    """
       缓存新闻详情
       Args:
           news_id: 新闻ID
           news_data: 新闻数据字典
           expire: 过期时间（秒），默认5分钟

       Returns:
           bool: 缓存成功返回True
    """
    news_detail_id = news_id if news_id else "all"
    key = f"{NEWS_DETAIL_PREFIX}{news_detail_id}"
    return await set_cache(key,news_detail,expire)
#获取新闻详情缓存
async def get_related_news_cache(news_id:int,category_id: int):
    key = f"{RELATED_NEWS_PREFIX}{news_id}:{category_id}"
    return await get_json_cache(key)
#设置新闻详情缓存
async def set_related_news_cache(news_id:int, category_id: int,related_news:List[Dict[str,Any]],
                                 expire:int = 1800):
    key = f"{RELATED_NEWS_PREFIX}{news_id}:{category_id}"
    return await set_cache(key,related_news,expire)