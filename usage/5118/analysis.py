import logging
import re
from collections import Counter, defaultdict
from functools import wraps, lru_cache
from pathlib import Path
from time import time
from typing import List, Set, Iterable

from itertools import combinations
import jieba
import pandas as pd
from colorlog import ColoredFormatter
from numpy import dot
from numpy.linalg import norm

LOG_FORMAT = "%(log_color)s%(asctime)s [%(threadName)-10.10s] [%(levelname)-5.5s] %(message)s"
formatter = ColoredFormatter(LOG_FORMAT)
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
rootLogger.addHandler(consoleHandler)
jieba.setLogLevel(logging.INFO)


def cache(func):
    """ 对函数运行的结果进行缓存 """
    values = {}

    @wraps(func)
    def wrapper(*args):
        key = "".join(str(x) for x in args)
        if key not in values:
            values[key] = func(*args)
        return values[key]

    return wrapper


def time_logger(func):
    """ 记录函数执行所花费的时间 """

    @wraps(func)
    def wrapper(*arg, **kwargs):
        start = time()
        res = func(*arg, **kwargs)
        end = time()
        logging.info(f"执行函数 {func.__name__}, 用时 {(end - start):.2f} 秒,{(end - start) / 60 / 60} 小时 ")
        return res

    return wrapper


def get_files(directory: str, pattern="*.zip") -> List[Path]:
    """
    读取指定目录下指定类型的文件，这里用来读取 directory 目录下的所有 zip 文件
    """
    path = Path(directory)
    return [x for x in path.glob(pattern) if x.is_file()]


def write_csv(texts: Iterable[str], file_name: str) -> bool:
    """ 将结果写回 csv 文件 """
    df = pd.DataFrame(texts)
    df.to_csv(file_name, index=False, header=False, encoding="UTF_8_SIG")
    return True


def write_excel(groups, res_file):
    """ 将结果写回 excel 文件 """
    df = pd.DataFrame(dict([(k, pd.Series(list(v))) for k, v in groups.items()]))
    df.to_excel(res_file, index=False, header=False, encoding="UTF_8_SIG")
    return True


def _aggregate(files: List[Path], skip_rows=None) -> Set[str]:
    """ 读取多个文件，将这些文件中的内容汇集一起 """
    texts = set()
    for file in files:
        df = pd.read_csv(file, encoding="GB18030", skiprows=skip_rows)
        logging.info(f"读取 csv {file.as_posix()}")
        first_column = df.iloc[:, 0]
        first_column = first_column.apply(lambda x: re.sub(r'[^\u4e00-\u9fa5]', '', x))
        texts.update(set(first_column))

    return texts


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


@cache
def get_counter(words: str):
    """
    统计一个数组中每个词语出现的次数，键是改词语，值是该词语出现的次数
    """
    return Counter(cut_word(words))


def build_vector(first: str, second: str):
    """ 为两个短语构建向量 """
    f_counter, s_counter = get_counter(first), get_counter(second)
    keys = f_counter.keys() | s_counter.keys()
    f_vector, s_vector = [], []
    for key in keys:
        f_vector.append(f_counter.get(key, 0))
        s_vector.append(s_counter.get(key, 0))

    return f_vector, s_vector


def cos_sim(first: List[float], second: List[float]) -> float:
    """计算两个向量之间的余弦相似度"""
    return dot(first, second) / (norm(first) * norm(second))


@time_logger
def group(file_name: str, threshold=0.8):
    """对所有短语进行分组"""
    df = pd.read_csv(file_name)
    keys = list(df.iloc[:, 0])
    visited, groups = set(), defaultdict(set)

    loop = 0
    batch = 500000
    start, end = time(), time()
    for x, y in combinations(keys, 2):
        loop += 1
        if not loop % batch:
            logging.info(f"处理 {x}:{y}，耗时 {(end - start):.10f} 秒,第 {(loop // batch)}个 50万对")
            start = end
        end = time()
        if ignore_visited(x, visited) or ignore_visited(y, visited):
            continue
        x_vector, y_vector = build_vector(x, y)
        sim = cos_sim(x_vector, y_vector)
        if sim >= threshold:
            groups[x].add(y)
            visited.add(y)

    logging.info(f"共有 {len(keys)} 个短语，执行了 {loop} 次循环")
    return groups


def analysis(directory: str = "./zip", aggregate=False, key_file="keys.csv", res_file="res.xlsx"):
    if aggregate:
        aggregate_files(directory, key_file)
    groups = group(key_file, threshold=0.8)
    write_excel(groups, res_file)
    return True


if __name__ == '__main__':
    analysis(aggregate=True)
