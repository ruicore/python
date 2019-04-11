import sys


class toutiao:
    def find(self, x: int, k: int) -> int:
        result, one = 0, 1
        while k:
            while one & x:
                one <<= 1
            result += one * (k & 1)
            k >>= 1
            one <<= 1
        return result


if __name__ == "__main__":
    lines = [line.strip().split() for line in sys.stdin.readlines()]
    so = toutiao()
    res = so.find(int(lines[0][0]), int(lines[0][1]))
    print(res)
