from difflib import SequenceMatcher


def get_similarity_score(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio()


def is_similar(text1, text2, min_score):
    return get_similarity_score(text1, text2) >= min_score

