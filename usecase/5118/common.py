import logging
import os
import re
from functools import wraps
from pathlib import Path
from time import time
from typing import Iterable, List, Set

import jieba
import pandas as pd
from logger import logger

jieba.setLogLevel(logging.INFO)


def cache(func):
    """ 对函数运行的结果进行缓存 """
    values = {}

    @wraps(func)
    def wrapper(*args):
        key = ''.join(str(x) for x in args)
        if key not in values:
            values[key] = func(*args)
        return values[key]

    return wrapper


def time_logger(func):
    """ 记录函数执行所花费的时间 """

    @wraps(func)
    def wrapper(*arg, **kwargs):
        start = time()
        logger.info(f'开始执行 {func.__name__} 函数')
        res = func(*arg, **kwargs)
        end = time()
        logger.info(
            f'执行函数 {func.__name__} 结束, 用时 {(end - start):.2f} 秒,{(end - start) / 60 / 60} 小时 '
        )
        return res

    return wrapper


def get_files(directory: str, pattern='*.zip') -> List[Path]:
    """
    读取指定目录下指定类型的文件，这里用来读取 directory 目录下的所有 zip 文件
    """
    directory = os.path.join(Path(__file__).parent.absolute(), directory)
    logger.info(f'读取目录下的 zip {directory} 文件')
    path = Path(directory)
    return [x for x in path.glob(pattern) if x.is_file()]


def write_csv(texts: Iterable[str], file_name: str) -> bool:
    """ 将结果写回 csv 文件 """
    file_name = os.path.join(Path(__file__).parent.absolute(), file_name)
    df = pd.DataFrame(texts)
    df.to_csv(file_name, index=False, header=False, encoding='UTF_8_SIG')
    logger.info(f'写 csv 文件  {file_name}')
    return True


def write_excel(groups, file_name: str):
    """ 将结果写回 excel 文件 """
    file_name = os.path.join(Path(__file__).parent.absolute(), file_name)
    df = pd.DataFrame(dict([(k, pd.Series(list(v))) for k, v in groups.items()]))
    df.to_excel(file_name, index=False, header=False, encoding='UTF_8_SIG')
    logger.info(f'写 excel 文件  {file_name}')
    return True


@time_logger
def _aggregate(files: List[Path], skip_rows=None) -> Set[str]:
    """ 读取多个文件，将这些文件中的内容汇集一起 """
    texts = set()
    for file in files:
        df = pd.read_csv(file, encoding='GB18030', skiprows=skip_rows)
        logging.info(f'读取 csv {file.as_posix()}')
        first_column = df.iloc[:, 0]
        first_column = first_column.apply(
            lambda x: re.sub(r'[^\u4e00-\u9fa5]', '', str(x))
        )
        texts.update(set(first_column))

    return texts


@time_logger
def aggregate_files(directory: str, file_name: str):
    """
    获取目录下的所有文件
    将所有文件的内容汇集到一起
    将结果重新写回到 csv 文件
    """
    files = get_files(directory)
    texts = _aggregate(files, skip_rows=[0])
    write_csv(texts, file_name)
    return True


def ignore_visited(x: str, visited: Set[str]):
    """ 判断一个短语是否已经被分到了一个组中 """
    return x in visited


@cache
def cut_word(content) -> Iterable[str]:
    """ 结巴分词 """
    return jieba.lcut(content)


def get_path(file_name):
    file_name = os.path.join(Path(__file__).parent.absolute(), file_name)
    return file_name


def get_stop_words() -> Set[str]:
    file_path = get_path('stop_words.csv')
    df = pd.read_csv(file_path)
    return set(df.iloc[:, 0])
