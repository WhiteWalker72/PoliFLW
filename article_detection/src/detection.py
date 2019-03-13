import pickle
import re, string


class Detection:

    def __init__(self):
        self.model = self._get_model("model/political.sav")

    @staticmethod
    def _get_model(filename: str):
        return pickle.load(open(filename, 'rb'))

    def is_political(self, data: str) -> bool:

        re_tok = re.compile(f'([{string.punctuation}“”¨«»®´·º½¾¿¡§£₤‘’])')

        def tokenize(s):
            return re_tok.sub(r' \1 ', s).split()

        vector = pickle.load(open("model/vector.sav", 'rb'))
        vector.tokenizer = tokenize
        tfidf = vector.transform([data])
        result = self.model.predict(tfidf)[0]
        if result >= 0.5:
            return True
        if result < 0.5:
            return False