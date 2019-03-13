import glob
import numpy


class Initialization:

    def __init__(self):
        self.path = "dataset"
        self.training_files = [f.replace("\\", "/") for f in glob.glob("dataset\\training\\*.txt")]
        self.test = self.path + "/" + "test.txt"
        self.validation = self.path + "/" + "validation.txt"
        self.vocab = self.path + "/" + "vocabulary.txt"

    def get_words(self) -> [list, list, list]:
        train = self._retrieve_words(self.training_files)
        valid = self._retrieve_words([self.validation])
        test = None
        return train, valid, test

    def get_vocabulary(self):
        vocab = {}
        with open(self.vocab) as f:
            for i, word in enumerate(f):
                vocab[word.strip()] = i
        return vocab

    def create_vocabulary(self) -> None:
        words = self._load_words(self.training_files)
        vocab = {}
        index = 0
        with open(self.vocab, 'w') as f:
            for word in words:
                if word not in vocab:
                    vocab[word] = index
                    index += 1
                    f.write(word + '\n')

    def _retrieve_words(self, files: list):
        vocab = self.get_vocabulary()
        words = self._load_words(files)
        x = numpy.empty(len(words), dtype=numpy.int32)
        for i, word in enumerate(words):
            x[i] = vocab[word]
        return x

    def _load_words(self, files: list) -> list:
        words = []
        for file in files:
            with open(file, encoding="utf8") as words_file:
                for line in words_file:
                    if line:
                        words += self._tokenize(line)
        return words

    def _tokenize(self, text: str) -> list:
        import re
        # obtains tokens with a least 1 alphabet
        pattern = re.compile(r'[A-Za-z]+[\w^\']*|[\w^\']*[A-Za-z]+[\w^\']*')
        return pattern.findall(text.lower())
