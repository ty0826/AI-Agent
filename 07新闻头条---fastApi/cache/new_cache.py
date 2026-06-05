"""
新闻相关的redis缓存
"""
from typing import Dict, Any
from config.cache_conf import get_json_cache, set_cache


# 读取缓存
async def get_category_cache(key:str):
    return await  get_json_cache(key)


# 设置缓存
async def set_category_cache(key:str,data: list[Dict[str, Any]], expire: int):
    return await set_cache(key, data, expire)
