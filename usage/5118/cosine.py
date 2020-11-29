import logging
from collections import Counter, defaultdict
from itertools import combinations
from time import time
from typing import List, Set

import jieba
import pandas as pd
from numpy import dot
from numpy.linalg import norm

from common import cache, aggregate_files, write_excel, time_logger, cut_word

jieba.setLogLevel(logging.INFO)


def ignore_visited(x: str, visited: Set[str]):
    """ 判断一个短语是否已经被分到了一个组中 """
    return x in visited


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


@time_logger
def analysis(directory: str = "./zip", aggregate=False, key_file="keys.csv", res_file="res.xlsx"):
    if aggregate:
        aggregate_files(directory, key_file)
    groups = group(key_file, threshold=0.8)
    write_excel(groups, res_file)
    return True


if __name__ == '__main__':
    """使用余弦相似度的方法对关键词进行分类"""
    analysis(aggregate=True)
