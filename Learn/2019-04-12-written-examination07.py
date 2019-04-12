import sys


class toutiao:
    def combine(self, string: str, operations: [[int, int]]) -> str:
        str_list = list(string)
        for item in operations:
            num1, num2 = int(item[0]), int(item[1])
            index = num1 + num2
            for i in range(num1 + num2 - 1, num1 - 1, -1):
                str_list.insert(index, str_list[i])
                index += 1
        return "".join(str_list)


if __name__ == "__main__":
    lines = [line.strip().split() for line in sys.stdin.readlines()]
    so = toutiao()
    res = so.combine(lines[0][0], lines[2:])
    print(res)
