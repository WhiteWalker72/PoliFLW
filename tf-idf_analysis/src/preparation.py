import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tag.perceptron import PerceptronTagger

import os
import pandas as pd
import re
from typing import Union


class Preparation:

    def __init__(self):
        nltk.download('punkt')
        self.stemmer = SnowballStemmer("dutch")
        self.stop_words = self._get_stopwords()
        self.tagger = self._get_tagger()

    @staticmethod
    def _get_stopwords():
        stop_words = set(stopwords.words('Dutch'))
        extra_stop_words = ['waar', 'onze', 'weer', 'daarom']
        stop_words.update(extra_stop_words)
        return stop_words

    @staticmethod
    def _get_tagger():
        # TODO: Instead of manually downloading the dutch_tagger, download it from an external source if it isn't installed at Data/
        try:
            os.chdir(r"Data")
            tagger = PerceptronTagger(load=False)
            tagger.load('model.perc.dutch_tagger_small.pickle')
            return tagger
        except (IndexError, FileNotFoundError):
            return None

    @staticmethod
    def jsonfile_to_dataframe(json_file) -> pd.DataFrame:
        """
        This function converts a json-file into a pandas dataframe.
        The most important information per article will be stored in the dataframe.
        """

        # Empty lists to fill with article data
        dates = []
        date_granularities = []
        descriptions = []
        enrichments = []
        locations = []
        parties = []
        politicians = []
        sources = []
        titles = []

        all_lists = [dates,
                     date_granularities,
                     descriptions,
                     enrichments,
                     locations,
                     parties,
                     politicians,
                     sources,
                     titles]

        all_searches = ['date',
                        'date_granularity',
                        'description',
                        'enrichments',
                        'location',
                        'parties',
                        'politicians',
                        'source',
                        'title']

        # Loop through requested articles
        for i in range(len(json_file)):
            for j, searchkey in enumerate(all_searches):
                try:
                    all_lists[j].append(json_file[i][searchkey])
                except KeyError:
                    all_lists[j].append(None)

        # Save as DataFrame and return
        dataframe = pd.DataFrame(
            {'date': dates,
             'date granularity': date_granularities,
             'description': descriptions,
             'enrichments': enrichments,
             'location': locations,
             'parties': parties,
             'politicians': politicians,
             'source': sources,
             'title': titles
             })

        return dataframe

    @staticmethod
    def refine_dataframe(dataframe):
        """
        This function removes the entries from the dataframe that do not contain a description.
        """
        empty_list = []

        # loop over dataframe to record the empty entries
        for i in range(len(dataframe)):
            if dataframe.description[i] is None:
                empty_list.append(i)

        # remove the empty entries by index and reset the index
        dataframe.drop(empty_list, inplace=True)
        dataframe = dataframe.reset_index()

        return dataframe

    @staticmethod
    def _text_mining_clean_text_regex(text, regex_statement, replacement):
        """
        This function removes the html-language from the article. Using a regex statement the function
        clears all the text that is between '<' and '>'.
        """
        pattern = re.compile(regex_statement)
        return re.sub(pattern, replacement, text)

    @staticmethod
    def _text_mining_tokenize_text(text):
        """
        This function tokenizes the text.
        """
        return nltk.word_tokenize(text)

    @staticmethod
    def _text_mining_clean_non_nouns(text, word_tagger):
        """
        This function removes all non-noun words. Using a tagger loaded with a model that was trained using 8
        million records of dutch sentences / words. The tagger labels all the words in the article and then the
        function will only keep the words that are labeled as nouns.
        """
        tagged = word_tagger.tag(text)
        return [t[0] for t in tagged if 'noun' in t[1]]

    @staticmethod
    def _text_mining_clean_stop_words(tokenized_text, stop_words):
        """
        This function removes all the stop words from an article. Stop words are frequently occuring words that
        have a relativly low meaning / weight.
        """
        return [word.lower() for word in tokenized_text if word.lower() not in stop_words]

    @staticmethod
    def _text_mining_clean_small_words(tokenizetext, min_wordsize=2):
        """
        This function removes all words that are smaller than two characters.
        """
        return [word for word in tokenizetext if len(word) >= min_wordsize]

    @staticmethod
    def _create_filter(options_list):
        """
        This functions creates a word list with all party names.
        """
        return [opt.lower() for opt in options_list]

    def _text_mining_clean_cities_parties(self, tokenizetext, party_list, city_list):
        """
        This function removes all words that are party names.
        This function removes all words that are city names and occur as a city in the dataframe.
        """
        party_filter = self._create_filter(party_list)
        city_filter = self._create_filter(city_list)
        return [word for word in tokenizetext if word not in set(party_filter) and word not in set(city_filter)]

    def _text_mining_stem_words(self, tokenized_text):
        """
        This functions stems all the words in the article.
        """
        return [self.stemmer.stem(word) for word in tokenized_text]

    def text_mining_all(self, texts_list, party_list, city_list):
        """
        This function combines all the text cleaning steps and cleans the articles.
        """
        # remove html code
        step = [self._text_mining_clean_text_regex(text, '<.*?>', '') for text in texts_list]

        # remove newlines ('\n') with a space
        step = [self._text_mining_clean_text_regex(text, '\n', ' ') for text in step]

        # remove urls
        step = [self._text_mining_clean_text_regex(text, r'http\S+', '') for text in step]

        # remove everything that doesn't contain letters
        step = [self._text_mining_clean_text_regex(text, r"[^a-zA-Z]+", ' ') for text in step]

        # tokenize text with nltk function and convert all words to lowercase
        step = [self._text_mining_tokenize_text(text) for text in step]

        if self.tagger is not None:
            # remove all words that are not nouns
            step = [self._text_mining_clean_non_nouns(text, self.tagger) for text in step]

        # remove the words that are contained within the list called stopwords
        step = [self._text_mining_clean_stop_words(text, self.stop_words) for text in step]

        # removes all words that have a length of 3 or less
        step = [self._text_mining_clean_cities_parties(text, party_list, city_list) for text in step]

        # removes all small words with length 3 or lower
        step = [self._text_mining_clean_small_words(text, 4) for text in step]

        return step
