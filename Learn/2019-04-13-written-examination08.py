import sys
import math
import itertools


class kuaishou:
    def get_bc(self, x: int, d1: int, d2: int, case: int) -> tuple:
        if case == 0:
            return (x + d1, x + d1 + d2)
        if case == 1:
            return (x + d1, x + d1 - d2)
        if case == 2:
            return (x - d1, x - d1 + d2)
        if case == 3:
            return (x - d1, x - d1 - d2)

    def judge(self, n: int, k: int, d1: int, d2: int) -> bool:
        if n % 3:
            return False
        x = [k - 2 * d1 - d2, k - 2 * d1 + d2, k + 2 * d1 - d2, k + 2 * d1 + d2]
        for i in range(4):
            if x[i] % 3 == 0:
                a = x[i] // 3
                m = n // 3
                b, c = self.get_bc(a, d1, d2, i)
                if 0 <= a <= m and 0 <= b <= m and 0 <= c <= m:
                    return True
        return False

    def recirlcle(self, nums: [[int]]) -> None:
        for item in nums:
            n, k, d1, d2 = item[0], item[1], item[2], item[3]
            if self.judge(n, k, d1, d2):
                print("yes")
            else:
                print("no")
        return


if __name__ == "__main__":
    lines = [list(map(int, line.strip().split())) for line in sys.stdin.readlines()]
    so = kuaishou()
    so.recirlcle(lines[1:])
