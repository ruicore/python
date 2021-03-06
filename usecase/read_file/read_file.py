import re


class BatchReadFile:
    def __init__(self):
        self.BATCH_SIZE = 100

    def _read(self, content, last_word):
        text = re.sub(
            r'[^\w ]', ' ', last_word + content
        )  # filter out non-words and non-space
        word_list = text.split(' ')
        f_word_list, last_word = word_list[:-1], word_list[-1]

        return list(filter(lambda x: x, f_word_list)), last_word

    def process(self, file_path):
        with open(file_path, 'r') as f:
            last_word = ''
            while True:
                chars = f.read(self.BATCH_SIZE)
                if not chars:
                    break
                full_words, last_word = self._read(chars, last_word)
                if full_words:
                    print(full_words)

        return


batch_read_file = BatchReadFile()
batch_read_file.process('large.txt')
