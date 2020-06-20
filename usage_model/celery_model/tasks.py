import sys

from celery.utils.log import get_logger

from usage_model.celery_model import app

sys.path.append("/Users/herui/Desktop/python/")  # this is for ipython shell
logger = get_logger(__name__)


@app.task(bind=True)
def add(self, a, b):
    logger.info(f"add {a} and {b}")
    return a + b


@app.task
def mul(a=1, b=1):
    logger.info(f"mul {a} and {b}")
    return a * b


if __name__ == "__main__":
    app.start()
