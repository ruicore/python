import os
from collections import defaultdict
from itertools import chain
from pathlib import Path
from typing import List

import pandas as pd
from sklearn.cluster import KMeans
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from common import time_logger, cut_word, write_excel, aggregate_files, get_path, get_stop_words
from logger import logger

import warnings

warnings.filterwarnings('ignore')


@time_logger
def parse_keys(keys: List[str]) -> List[str]:
    space = " "
    return [space.join(cut_word(key)) for key in keys]


@time_logger
def group(file_name: str, clusters_count=1000, calc_times: bool = False):
    """
    对所有短语进行分组
    :param file_name: 关键词文件，只有一列，全部为关键词
    :param clusters_count: 最终分成的组数
    """
    df = pd.read_csv(file_name)
    keys = list(filter(lambda x: 5 <= len(x) <= 20, df.iloc[:, 0]))
    split_keys = parse_keys(keys)

    if calc_times:
        times = Counter(chain.from_iterable([key.split() for key in split_keys]))
        df = pd.DataFrame({"关键词": k, "词频": v} for k, v in times.items())
        file_name = os.path.join(Path(__file__).parent.absolute(), "times.xlsx")
        df.to_excel(file_name, index=False, header=True, encoding="UTF_8_SIG")
        logger.info(f"写 excel 文件  {file_name}")

    logger.info(f"一共有 {len(keys)} 个词语需要分组")

    cv = CountVectorizer(stop_words=get_stop_words())
    cv_vec = cv.fit_transform(split_keys)
    kmeans = KMeans(n_clusters=clusters_count, random_state=0).fit(cv_vec)
    clusters: List[int] = kmeans.predict(cv_vec)

    groups = defaultdict(set)

    for idx, key in zip(clusters, keys):
        groups[idx].add(key)

    return groups


@time_logger
def analysis(directory: str = "./zip", aggregate=False, clusters_count=2, file_count: int = 10,
             calc_times: bool = False, key_file="keys.csv", res_file="res.xlsx"):
    """ 对所有的 zip 文件进行分析，输出为到 res.xlsx 文件中"""
    if aggregate:
        aggregate_files(directory, key_file)
    file_path = get_path("keys.csv")
    groups = group(file_path, clusters_count=clusters_count, calc_times=calc_times)
    if file_count > clusters_count:
        file_count = clusters_count
    each = clusters_count // file_count
    for i in range(file_count):
        subgroup = {t: groups.get(t) for t in range(i * each, (i + 1) * each)}
        write_excel(subgroup, f"res/{i + 1}_{res_file}")
    return True


if __name__ == '__main__':
    """使用 kmeans 的方法对关键词进行分裂"""
    # 这个参数控制最终分成的组的数量，50w 关键词，建议设置为 1000，示例文件的关键词数量很少，所以这里设置成了 10 ，建议修改
    clusters_count = 10
    file_count = 10  # 最后输出的 excel 数量，如果 file_count > clusters_count，那么只会输出  clusters_count 个文件
    calc_times = True  # 是否需要统计词频，不需要请改成 False
    analysis(aggregate=True, clusters_count=clusters_count, file_count=file_count, calc_times=calc_times)
