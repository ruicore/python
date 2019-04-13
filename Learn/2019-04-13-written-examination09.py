import sys
import math
import itertools


class toutiao:
    def __init__(self):
        self.a_num = []

    def count(self, string: str) -> None:
        self.a_num = [0 for _ in range(len(string) + 1)]
        for i in range(1, len(string) + 1):
            if string[i - 1] == "a":
                self.a_num[i] = self.a_num[i - 1] + 1
            else:
                self.a_num[i] = self.a_num[i - 1]

    def judge(self, length: int, step: int, k: int) -> bool:
        for i in range(1, length + 2 - step):
            a = self.a_num[i + step - 1] - self.a_num[i - 1]
            b = step - a
            if a <= k or b <= k:
                return True
        return False

    def sovle(self, string: str, k: int) -> int:
        self.count(string)
        length = len(string)
        left, right = 1, length
        while left <= right:
            mid = left + ((right - left) >> 1)
            if self.judge(length, mid, k):
                left = mid + 1
            else:
                right = mid - 1
        return max(1, right)


if __name__ == "__main__":
    line1 = list(map(int, sys.stdin.readline().strip().split()))
    line2 = sys.stdin.readline().strip()
    so = toutiao()
    res = so.sovle(line2, line1[1])
    print(res)

