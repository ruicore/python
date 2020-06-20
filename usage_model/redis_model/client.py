from typing import Optional

import aioredis

REDIS_URL = "redis://localhost:6379"


class Redis:
    def __init__(self, address: str = REDIS_URL):
        self.address = address
        self.is_connected: bool = False
        self.redis: Optional[aioredis.Redis] = None

    async def connect(self):
        assert not self.is_connected, "Redis is already connected."

        self.redis = await aioredis.create_redis_pool(self.address, minsize=5, maxsize=20)
        self.is_connected = True

    async def dis_connected(self):
        assert self.is_connected, "Redis is already disconnected."

        self.redis.close()
        await self.redis.wait_closed()
        self.is_connected = False
        self.redis = None

    async def execute(self, command, *args, **kwargs):
        return await self.redis.execute(command, *args, **kwargs, encoding='utf8')


async def test():
    from uuid import uuid4
    from datetime import datetime
    from bson.json_util import loads, dumps

    redis = Redis()
    await redis.connect()

    key = uuid4().hex
    random_dict = {uuid4().hex: {"name": "test", "time": datetime.utcnow()}}
    status = await redis.execute("SET", key, dumps(random_dict))
    value = await redis.execute("GET", key)

    assert status == "OK", f"set key {key} failed"
    print(loads(value))

    await redis.dis_connected()


if __name__ == "__main__":
    import asyncio

    asyncio.run(test())
