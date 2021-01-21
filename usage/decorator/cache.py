class Count:
    def __init__(self, func):
        self.count = 0
        self.func = func

    def __call__(self, *arg, **kwargs):
        self.count += 1
        print(f"{str(self.func)} is called for {self.count} times <including current>")
        return self.func(*arg, **kwargs)


class Cache(object):
    """class decorator with args"""

    def __init__(self, function, max_hits=10, timeout=5):
        self.function = function
        self.max_hits = max_hits
        self.timeout = timeout
        self.cache = {}

    def __call__(self, *args):
        return self.function(*args)


def cache(function=None, max_hits=10, timeout=5):
    if function:
        return Cache(function)
    else:
        def wrapper(function):
            return Cache(function, max_hits, timeout)

        return wrapper


@cache(max_hits=100, timeout=50)
def double(x):
    return x * 2


@Count
def add(num):
    return 1 + num


for i in range(10):
    print(add(i))

for i in range(10):
    print(double(23))
