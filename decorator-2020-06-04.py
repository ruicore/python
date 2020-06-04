class Count:
    def __init__(self, func):
        self.count = 0
        self.func = func

    def __call__(self, *arg, **kwargs):
        self.count += 1
        print(
            f"{str(self.func)} is called, already called for {self.count} times <including current>"
        )
        return self.func(*arg, **kwargs)


@Count
def test(num):
    return 1 + num


for i in range(10):
    print(test(i))
