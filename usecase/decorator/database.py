from functools import partial, wraps

from databases import Database


def init_db(func=None, *, db: Database = None):
    if func is None:
        if db is None:
            raise ValueError('init db must not be None')
        return partial(init_db, db=db)

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not db.is_connected:
            await db.connect()
        try:
            result = await func(*args, **kwargs)
        except Exception as e:
            return str(e)
        finally:
            if db.is_connected:
                await db.disconnect()
        return result

    return wrapper
