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
## 4.遍历

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

## 5.类

需求：为了确保用户输入正确格式的数，强制用户使用函数进行访问；为了简介，通过 property 自动调用函数，实现「设置属性自动调用函数的效果」

property 为类创建可管理的属性
```py

class Control(object):
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_value(self, num: int):
        if not isinstance(num, (int, float)):
            raise ValueError("please enter num")
        self.value = num

    r = property(get_value, set_value)
```

需求：实现类的比较

```py
from functools import total_ordering
from abc import ABCMeta, abstractmethod


@total_ordering
class Shape(object):

    @abstractmethod
    def area(self):
        pass

    def __lt__(self, obj):
        if not isinstance(obj, Shape):
            raise TypeError("obj is not a shape")
        return self.area() < obj.area()

    def __eq__(self, obj):
        if not isinstance(obj, Shape):
            raise TypeError("obj is not a shape")
        return self.area() == obj.area()


class Cirlcle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14*self.radius**2


class Rect(Shape):
    def __init__(self, weight, height):
        self.weight = weight
        self.height = height

    def area(self):
        return self.weight*self.height


cricle = Cirlcle(3)
rect = Rect(3, 4)
print(cricle >= rect)
```

需求：对实例的类做类型检查

```py
class Attr(object):
    def __init__(self, name, type_):
        self.name = name
        self.type_ = type_

    def __get__(self, instance, cls):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.type_):
            raise TypeError("expect a {}".format(self.type_))
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class Monkey(object):
    name = Attr("name", str)
    age = Attr("age", int)
    gender = Attr("gender", str)

```

需求：根据字符串执行实例的函数

```py
from operator import methodcaller


class MethonCall(object):
    def get_value(self, value: int, value2: int):
        return 12*value*value2


mc = MethonCall()
fun = methodcaller("get_value", 2, -1)
print(fun(mc))
```