# Python 进阶使用技巧

## 1.在列表，字典，集合中根据条件筛选数据
需求：
过滤 list 中大于 0 的数：[14, 0, -6, 0, -10, -8, -1, 19, -10, -16]
筛选出字典中值大于 0 的项目：{0: 9, 1: -3, 2: -8, 3: 6, 4: -4, 5: -4, 6: -7, 7: -8, 8: 7, 9: -3}
筛选出集合中能被 2 整除的数：{3, 4, 9, 12, 15, 17, 19, 20}

```py
list_bigger = [x for x in list_nums if x > 0]
dict_bigget = {k: v for k, v in dict_nums.items() if v > 0}
set_two = {x for x in set_nums if not x % 2}
```
## 2.命名，统计，字典
需求：在表格中，每一行的信息固定，为了访问某个位置的值，不使用索引

```py
from collections import namedtuple

stuendt = namedtuple("Student", ["name", "age", "sex"])

s1 = stuendt(name="12", age=12, sex="female")
s2 = stuendt(name="12", age=12, sex="male")
```

需求：
统计 [5, 2, 2, 3, 1, 5, 1, 3, 2, 4] 出现次数最高的 3 的元素，并找到它们的出现次数
统计一个段落中出现次数最高的前 3 个元素，并确定次数

```py
import re
from collections import Counter

nums = [5, 2, 2, 3, 1, 5, 1, 3, 2, 4]

times = Counter(nums)
com = times.most_common(3)


text = """If operators with different priorities are used, consider adding
whitespace around the operators with the lowest priority(ies). Use
your own judgment; however, never use more than one space, and
always have the same amount of whitespace on both sides of a binary
operator."""
times = Counter(re.split(r"\W+",text))
com = times.most_common(3)
```
需求：根据字典中值的大小，对字典排序

```py
nums = {0: 9, 1: -3, 2: -8, 3: 6, 4: -4, 5: -4, 6: -7, 7: -8, 8: 7, 9: -3}
res = sorted(nums.items(), key=lambda x: x[1])
```

需求：找到多个字典中的公共键

```py
from functools import reduce

a = {'b': 7, 'f': 3, 'e': 9}
b = {'d': 8, 'b': 2, 'f': 8, 'e': 10, 'g': 6}
c = {'h': 2, 'e': 7, 'b': 11}

res = reduce(lambda x, y: x & y, map(dict.keys, [a, b, c]))
```
需求：让字典保持有序

```py
from collections import OrderedDict

order = OrderedDict()
for x in sample("abcdefgh", randint(3, 6)):
    order[x] = randint(4,10)
```
## 3.字符串

需求：根据多个分隔符，拆分字符串

```py
import re

text = """If\roperators\r\n with\different<<priorities are\vused, consider adding
whitespace around the operators with the lowest priority(ies). Use
your own judgment;;\however, never use more than one space, and
always have}the\\same amount of whitespace on both sides of a binary
operator."""

res = re.split(r"[\r\n\t\v\\}; .<]+",text)
```
需求：调整文本中的字符串格式，将 07/20/2019 替换成为 2019-07-20

```py

# 使用了正则的捕获组
import re
text = "07/20/2019"

res = re.sub(r"(\d{2})\/(\d{2})\/(\d{4})", r"\3-\1-\2", text)
```
## 遍历

需求：同时遍历可迭代对象

```py
from itertools import chain


nums1 = [1, 5, 4, 5]
nums2 = [2, 3, 3]
nums3 = [4, 3, 3, 5, 7, 8, 3]

# 并行遍历
for x, y, z in zip(nums1, nums2, nums3):
    print(x, y, z)
# 串行遍历
for x in chain(nums1, nums2, nums3):
    print(x)
```