def dec3(fuc):
    print(3)

    def wrap():
        print("decs")
        fuc(1, 2)

    return wrap


def dec2(fuc):
    print(2)

    def wrap():
        print("dec2")
        fuc()

    return wrap


def dec1(fuc):
    print(1)

    def warp():
        print("dec1")
        fuc()

    return warp


@dec1
@dec2
@dec3
def test(a, b):
    print("test")


# test = dec1(dec2(dec3(test)))

test()
