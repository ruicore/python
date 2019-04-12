import sys
import math
import itertools


class kuaishou:
    def recirlcle(self, num1: int, num2: int) -> str:
        quo, rem = divmod(num1, num2)
        string = str(quo)
        if rem:
            string += "."
        start = len(string)
        nums = {rem: start}
        while rem:
            quo, rem = divmod(rem * 10, num2)
            string += str(quo)
            if rem in nums:
                res = string[: nums[rem]] + "(" + string[nums[rem] :] + ")"
                return res
            start += 1
            nums[rem] = start
        return string


if __name__ == "__main__":
    lines = [list(map(int, line.strip().split())) for line in sys.stdin.readlines()]
    so = kuaishou()
    res = so.recirlcle(lines[0][0], lines[0][1])
    print(res)
