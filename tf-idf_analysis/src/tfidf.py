import pandas as pd
import numpy as np
from preparation import Preparation


class TFIDF:

    def __init__(self):
        self.preparation = Preparation()

    @staticmethod
    def _tfidf_unique_words(processed_texts):
        """
        This function finds all the unique words from the provided articles.
        """
        temp = set([word for text in processed_texts for word in text])
        return list(temp)

    @staticmethod
    def _tfidf_word_dictionary(unique_word_list):
        """
        This function creates a dictionary with all the unique words and gives them an index.
        """
        return {key: index for index, key in enumerate(unique_word_list)}

    @staticmethod
    def _tfidf_empty_matrix(texts_list, unique_word_list):
        """
        This function creates an empty matrix filled with zeros. The axes are the number of articles in the texts
        list and the number of unique words.
        """
        return np.zeros((len(texts_list), len(unique_word_list)))

    def _tfidf_count_matrix(self, unique_word_list, texts_list, word_dictionary):
        """
        This function filles in an empty matrix with all the occurences of every word in every article.
        """
        temp_matrix = self._tfidf_empty_matrix(texts_list, unique_word_list)
        for i in range(len(texts_list)):
            for word in texts_list[i]:
                temp_matrix[i, word_dictionary[word]] += 1

        return temp_matrix

    @staticmethod
    def _tfidf_clean_matrix(count_matrix):
        """
        This function can remove all the articles from the matrix that do not contain any words due to the text
        cleaning operations.
        """
        return count_matrix[np.where(count_matrix.sum(axis=1) != 0)]

    @staticmethod
    def _tfidf_term_frequency(count_matrix):
        """
        This function calculates the term frequency of each word per article. The outcome is a filled in matrix with
        term frequency values for every word per article.
        """
        sums = count_matrix.sum(axis=1)
        new_matrix = 0.5 + 0.5 * (count_matrix / sums[np.newaxis].T)
        return new_matrix

    @staticmethod
    def _tfidf_inversed_document_frequency(count_matrix):
        """
        This function calculates the inversed document frequency of every word. The outcome is an array with all the
        inversed document values per word.
        """
        occurences = np.count_nonzero(count_matrix, axis=0)
        new_array = np.log((len(count_matrix) / occurences))
        return new_array

    @staticmethod
    def _tfidf_calculate_tfidf(tf_matrix, idf_matrix):
        """
        This function combines the word frequency matrix with the inversed document frequency array in order to
        calculate all the term frequency-inversed document frequency values per word per article.
        """
        return tf_matrix * idf_matrix

    def _tfidf_all(self, texts_list):
        """
        This function combines all the tf-idf functions to create a process with which the tf-idf values can be
        calculated for the provided articles.
        """
        # find all the unique words in the provided texts
        step1 = self._tfidf_unique_words(texts_list)

        # convert the all the unique words to a dictionary with a given index
        step2 = self._tfidf_word_dictionary(step1)

        # create a matrix with all the word occurences per word per text
        step3 = self._tfidf_count_matrix(step1, texts_list, step2)

        # in the matrix calculate the term frequency for every word per text
        step4 = self._tfidf_term_frequency(step3)

        # calculate the inversed document frequency for each word
        step5 = self._tfidf_inversed_document_frequency(step3)

        # combine the word frequency and the inversed document frequency
        step6 = self._tfidf_calculate_tfidf(step4, step5)

        return [step2, step6]

    @staticmethod
    def _dataframe_find_uniques(dataframe, choice):
        """
        Create a list with all the unique occurences depending on the given choice. At the moment you can choose between
        'party' and 'city' to create a new list with uniques.
        """
        mega_list = []

        if choice == 'party':
            for parties in dataframe.parties:
                for party in parties:
                    mega_list.append(party)

        elif choice == 'city':
            for city in dataframe.location:
                if city is None:
                    continue
                mega_list.append(city)

        mega_list = set(mega_list)

        return list(mega_list)

    @staticmethod
    def _find_tfidf_top_words_all(analysis_result, number=5):
        """
        Find the n number of words that score the highest tf-idf rating per article. These are then presented in a list
        with the top words per article.
        """
        temp_word_dict = {}
        for value, key in enumerate(analysis_result[0]):
            temp_word_dict[value] = key

        top_words_inds = []
        for arr in analysis_result[1]:
            top_words_inds.append(list(np.argpartition(arr, -number)[-number:]))

        top_words_per_article = []
        for indexes in top_words_inds:
            temp = []
            for index in indexes:
                temp.append(temp_word_dict[index])
            top_words_per_article.append(temp)

        return top_words_per_article

    def _keyword_tagger_all(self, dataframe):
        """
        This function combines all the neccessary functions in order to create a list with the top scoring words based
        on your choice (tf-idf or count). The result is a list with the top words per article.
        """
        start_index = 0
        end_index = 1000
        result_list = []
        party_list = self._dataframe_find_uniques(dataframe, 'party')
        city_list = self._dataframe_find_uniques(dataframe, 'city')

        while start_index < len(dataframe):

            # select a subset of the dataframe with the start and end index, these change (with +1000) after every loop
            raw_articles = dataframe.description[start_index:end_index]
            # clean and prepare all the texts in the selected subset
            cleaned_articles = self.preparation.text_mining_all(raw_articles, party_list, city_list)

            # calculate the tf-idf of each word per text
            analysed_articles = self._tfidf_all(cleaned_articles)

            # find the top words based on the tf-idf
            top_words = self._find_tfidf_top_words_all(analysed_articles)

            for l in top_words:
                result_list.append(l)

            start_index += 1000
            end_index += 1000

            print('\r{}/{}'.format(start_index, len(dataframe)), end='')

        print("\nTHE END!")

        return result_list

    def get_tfidf_dataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:

        # find the top words with the tf-idf method
        top_words_per_article_list_tfidf = self._keyword_tagger_all(dataframe)

        # add the top words per article from the tf-idf method to the dataframe as a new column
        dataframe['KEYWORDS-TFIDF'] = top_words_per_article_list_tfidf

        return dataframe
