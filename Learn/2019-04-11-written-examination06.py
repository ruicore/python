import sys


class toutiao:
    def count(self, nums: [int]) -> int:
        dp = [2 for _ in range(len(nums))]
        nums.sort()
        for i in range(1, len(nums)):
            if dp[i - 1] == 0:
                dp[i] = 2
            elif nums[i] - nums[i - 1] > 20:
                dp[i] = dp[i - 1] + 2
            else:
                dp[i] = dp[i - 1] - 1
        return dp[-1]

if __name__ == "__main__":
    lines = [list(map(int, line.strip().split())) for line in sys.stdin.readlines()]
    so = toutiao()
    res = so.count(lines[1])
    print(res)
