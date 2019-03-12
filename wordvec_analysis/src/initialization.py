import os

import numpy

from chainer.dataset import download


class Initialization:

    def __init__(self, path: str, training: str, validation: str, test: str, vocab: str):
        self.training = path + "/" + training
        self.validation = path + "/" + validation
        self.test = path + "/" + test
        self.vocab = path + "/" + vocab

    def get_words(self) -> [list, list, list]:
        train = self._retrieve_words(self.training)
        valid = self._retrieve_words(self.validation)
        test = None #self._retrieve_words(self.test)
        return train, valid, test

    def get_vocabulary(self) -> list:
        vocab = {}
        with open(self.vocab) as f:
            for i, word in enumerate(f):
                vocab[word.strip()] = i
        return vocab

    def create_vocabulary(self) -> None:
        words = self._load_words(self.training)
        vocab = {}
        index = 0
        with open(self.vocab, 'w') as f:
            for word in words:
                if word not in vocab:
                    vocab[word] = index
                    index += 1
                    f.write(word + '\n')

    def _retrieve_words(self, file: str):
        vocab = self.get_vocabulary()
        words = self._load_words(file)
        x = numpy.empty(len(words), dtype=numpy.int32)
        for i, word in enumerate(words):
            x[i] = vocab[word]
        return x
        #
        # numpy.savez_compressed(file, x=x)
        # return numpy.load({'x': x})

    def _load_words(self, file: str) -> list:
        words = []
        with open(file) as words_file:
            for line in words_file:
                if line:
                    words += self._tokenize(line)  #+= line.strip().split()
                    words.append('<eos>')
        return words

    def _tokenize(self, text: str) -> list:
        import re
        # obtains tokens with a least 1 alphabet
        pattern = re.compile(r'[A-Za-z]+[\w^\']*|[\w^\']*[A-Za-z]+[\w^\']*')
        return pattern.findall(text.lower())

