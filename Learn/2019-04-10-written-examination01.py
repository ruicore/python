import sys


class toutiao:
    def __init__(self):
        self.table = {chr(i + 65): 0 for i in range(10)}
        self.head = set()

    def get_weight(self, words: [chr]) -> None:
        for word in words:
            weight = 1
            self.head.add(word[0])
            for c in word[::-1]:
                self.table[c] += weight
                weight *= 10
        return

    def get_correspondence(self) -> None:
        order = [
            item[0]
            for item in sorted(
                self.table.items(), key=lambda word: word[1], reverse=True
            )
        ]
        index, num = 9, 9
        while order[index] in self.head:
            index -= 1
        for i in range(0, index):
            self.table[order[i]] = num
            num -= 1
        for i in range(index + 1, 10):
            self.table[order[i]] = num
            num -= 1
        self.table[order[index]] = 0

    def driver(self, words: [chr]) -> int:
        self.get_weight(words)
        self.get_correspondence()
        res = 0
        for word in words:
            weight = 1
            for char in word[::-1]:
                res += self.table[char] * weight
                weight *= 10
        return res


if __name__ == "__main__":
    words = [line.strip() for line in sys.stdin.readlines()]
    so = toutiao()
    res = so.driver(words[1:])
    print(res)
