import os
from collections import Counter
from collections import defaultdict
from itertools import chain
from typing import List, Set, Optional, Tuple

import pandas as pd
import xmind

from common import cut_word, aggregate_files, get_stop_words, time_logger


class Draw:
    def __init__(self, directory: str = './zip', aggregate: bool = True, key_file="keys.csv",
                 res_file: str = "res.xmind",
                 depth: int = 4, width: int = 5):
        self.index = {}
        self.invert_index = {}
        self.ignore_topics = {}
        self.key_file = key_file
        self.res_file = res_file
        self.depth = depth
        self.width = width
        if aggregate:
            texts = aggregate_files(directory, file_name="keys.csv", to_csv=False)
        else:
            texts = pd.read_csv(key_file, encoding='UTF_8_SIG')
        self._build_index(texts, get_stop_words())

    def _build_index(self, texts: Set[str], stop_words: Set[str]) -> bool:
        """
        为所有的关键词建立正排索引和倒排索引
        """
        index, invert_index = defaultdict(set), defaultdict(set)
        for text in texts:
            roots = set(cut_word(text))
            roots = roots - stop_words
            index[text] = index[text].union(roots)
            _ = [invert_index[root].add(text) for root in roots]
        self.index, self.invert_index = index, invert_index
        return True

    def _get_top(self, n: int, topics: Optional[List[str]]) -> List[str]:
        """
        为给定的关键词获取 Top N 关键词
        n: The number of most common N topic.
        topics: We find most common N topic belong to these topics.
        invert_index: Inverted Index for keys
        index: The index for keys.
        ignore_topics: When find most common N topics, ignore these Topics.
        """
        if not topics:
            topics = self.invert_index.keys()
        all_origin_keys = chain.from_iterable([self.invert_index[key] for key in topics])
        all_topics = chain.from_iterable([self.index[key] for key in all_origin_keys])
        counter = Counter(all_topics)
        for t in self.ignore_topics:
            del counter[t]

        return [t[0] for t in counter.most_common(n)]

    def _add_child_topic(self, root_node, root_topic, current):
        if current >= self.depth:
            return
        topics = self._get_top(self.width, [root_topic])
        for sub in topics:
            sub_top = root_node.addSubTopic()
            sub_top.setTitle(sub)
            self.ignore_topics = self.ignore_topics | {sub}
            self._add_child_topic(sub_top, sub, current + 1)
        return

    @time_logger
    def draw(self):
        try:
            os.remove(self.res_file)
        except FileNotFoundError:
            pass

        # 创建 sheet
        workbook = xmind.load(self.res_file)
        sheet = workbook.createSheet()

        # 创建根节点
        root = self._get_top(1, None, )[0]
        sheet.setTitle(root)
        rt = sheet.getRootTopic()
        rt.setTitle(root)

        # 创建子节点
        self.ignore_topics = {root}
        self._add_child_topic(rt, root, 0)

        xmind.save(workbook)


if __name__ == '__main__':
    directory: str = './zip'  # 存放从 5118 下载的所有压缩文件
    aggregate: bool = True  # 是否是多个文件
    key_file = "keys.csv"  # 如果已经生成了关键词文件，可以指定关键字文件的名字
    res_file: str = "res.xmind"  # 最后结果文件的名称
    depth: int = 3  # 控制思维导图的深度
    width: int = 4  # 控制每一层的节点个数
    client = Draw(directory, aggregate, key_file, res_file, depth, width)
    client.draw()
