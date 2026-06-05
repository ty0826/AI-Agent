import json
import redis.asyncio as redis
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0

# 创建redis的连接对象
redis_client = redis.Redis(
    host=REDIS_HOST,  # redis服务器的主机地址
    port=REDIS_PORT,  # redis端口号
    db=REDIS_DB,  # redis数据库编号 0-15
    decode_responses=True  # 是否将字节数据编码成字符串
)


# 设置和读取（字符串、列表、字典）

# 读取字符串
async def get_cache(key: str):
    try:
        return await redis_client.get(key)
    except  Exception as e:
        print(f'获取失败{e}')
        return None


# 读取列表或者字典
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            # 转列表、字典
            return json.loads(data)
    except Exception as e:
        print(f'获取失败{e}')
        return None


# 设置缓存
async def set_cache(key: str, value, expire: int = 3600):
    try:
        # 如果是字典或者列表
        if isinstance(value, (dict, list)):
            # 先转字符串
            data = json.dumps(value, ensure_ascii=False)  # 中文乱码也存入
        else:
            data = value
        await redis_client.setex(key, expire, data)
        return True
    except Exception as e:
        print(f'缓存失败{e}')
        return None
