
import sys
import itertools
import operator


class toutiao:
    def get_next(self, _next: [int], string: str) -> None:
        j, i, count = 0, 1, len(string)
        while i < count:
            if operator.eq(string[i], string[j]):
                _next[i] = j + 1
                i, j = i + 1, j + 1
            else:
                if operator.eq(j, 0):
                    _next[i] = 0
                    i += 1
                else:
                    j = _next[j - 1]
        return

    def driver(self, strings: [str], k: int) -> int:
        result, length = 0, 0
        for item in strings:
            length += len(item)
        _next = [0 for _ in range(length)]
        for item in itertools.permutations(strings):
            string = "".join(item)
            self.get_next(_next, string)
            circle = length - _next[-1]
            if length // circle == k:
                result += 1
        return result


if __name__ == "__main__":
    lines = [line.strip() for line in sys.stdin.readlines()]
    so = toutiao()
    res = so.driver(lines[1:], int(lines[0].split()[1]))
    print(res)

