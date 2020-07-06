# a = [1,2,3]
# b = [1,3,2,4,5,6] check if all num in a is in b, ordered
# [1,2,3] is in [1,2,3,4] but [1,2,3] is not in [1,3,2,4]


def check(a, b):
    b = iter(b)
    return all(i in b for i in a)
