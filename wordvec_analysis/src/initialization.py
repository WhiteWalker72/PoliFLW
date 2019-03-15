import json
import glob
import numpy
import re
import requests


class Initialization:

    training_path = "dataset/training/*.txt"
    api_url = "https://api.poliflw.nl/v0/search"
    poliflw_datasets = ["provinciale verkiezingen",
                        "terrorisme",
                        "waterschapsverkiezingen",
                        "klimaatverandering",
                        "eerste kamer",
                        "tweede kamer"
                        ]

    def __init__(self, create_poliflw_dataset=True):

        if create_poliflw_dataset:
            self._create_poliflw_datasets()

        self.path = "dataset"
        self.training_files = self._get_training_files()
        self.test = self.path + "/" + "test.txt"
        self.validation = self.path + "/" + "validation.txt"
        self.vocab = self.path + "/" + "vocabulary.txt"

    def _get_training_files(self):
        files = [f.replace("\\", "/") for f in glob.glob(self.training_path)]
        files.extend([f.replace("\\", "/") for f in glob.glob("dataset/training/**/*.txt")])
        return files

    def get_words(self) -> [list, list, list]:
        self._create_vocabulary()
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

    def _create_vocabulary(self) -> None:
        words = self._load_words(self.training_files)
        vocab = {}
        index = 0
        with open(self.vocab, 'w', encoding="utf8") as f:
            for word in words:
                if word not in vocab:
                    vocab[word] = index
                    index += 1
                    f.write(word + '\n')

    def _create_poliflw_datasets(self) -> None:
        for dataset in self.poliflw_datasets:
            self._create_poliflw_dataset(dataset)

    def _create_poliflw_dataset(self, subject: str) -> None:
        payload = {"query": subject, "size": 100}
        headers = {'content-type': 'application/json'}

        r = requests.post(self.api_url, data=json.dumps(payload), headers=headers)
        data = r.json()
        f = open("dataset/training/poliflw/{0}.txt".format(subject), "w+", encoding="utf8")
        for item in data['item']:
            f.write(self._clean_html(item['description']))
        f.close()

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

    @staticmethod
    def _tokenize(text: str) -> list:
        # obtains tokens with a least 1 alphabet
        text = text.lower()
        pattern = re.compile(r'[A-Za-z]+[\w^\']*|[\w^\']*[A-Za-z]+[\w^\']*')
        return pattern.findall(text.lower())

    @staticmethod
    def _clean_html(text: str) -> str:
        pattern = re.compile(r'<.*?>')
        return pattern.sub('', text)
