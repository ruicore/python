import sys

# 最长边小于其余所有边的和

class toutiao:
    def __init__(self):
        self.stick = []
        self.count = 0

    def judge(self, type: chr, num: int) -> bool:
        if type == "1":
            self.stick.append(num)
            self.count += 1
        if type == "2":
            self.stick.remove(num)
            self.count -= 1
        if self.count < 3:
            return False
        else:
            _max = max(self.stick)
            _sum = sum(self.stick)
            if _max < _sum - _max:
                return True
        return False


if __name__ == "__main__":
    lines = [line.strip().split() for line in sys.stdin.readlines()]
    so = toutiao()
    for line in lines[1:]:
        if so.judge(line[0], int(line[1])):
            print("Yes")
        else:
            print("No")
