from functools import partial, wraps

from usage_model import Redis


def init_redis(func=None, *, redis: Redis = None):
    if func is None:
        return partial(init_redis, redis=redis)

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not redis.is_connected:
            await redis.connect()
        try:
            result = func(*args, **kwargs)
        finally:
            if redis.is_connected:
                await redis.dis_connected()
        return result

    return wrapper
