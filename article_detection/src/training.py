# source https://github.com/martinpella/metacritic/blob/master/sentiment.ipynb

import pandas as pd
import pickle
import string
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import TruncatedSVD


def load_dataframe(file: str, political: bool) -> pd.DataFrame:
    df = pd.read_csv('dataset/' + file, sep='\n', names=['text'])

    if political:
        df['political'] = 1
    else:
        df['political'] = 0
    return df


dfs = []
# Load a CSV that is filled with political text
df = load_dataframe("political.csv", True)
dfs.append(df)

# Load a CSV that is filled with non-political text
df = load_dataframe("non_political.csv", False)
dfs.append(df)

# Merge the two dataframes together
dataframe = pd.concat(dfs)
X_train, X_test, y_train, y_test = train_test_split(dataframe['text'].values,
                                                    dataframe['political'].values,
                                                    test_size=0.2,
                                                    random_state=42)


def tokenize(s):
    re_tok = re.compile(f'([{string.punctuation}“”¨«»®´·º½¾¿¡§£₤‘’])')
    return re_tok.sub(r' \1 ', s).split()


# TF IDF
vect = TfidfVectorizer(strip_accents='unicode', tokenizer=tokenize, ngram_range=(1, 2), max_df=0.9, min_df=3, sublinear_tf=True)
tfidf_train = vect.fit_transform(X_train)
tfidf_test = vect.transform(X_test)
svd = TruncatedSVD()
reduced_tfidf_train = svd.fit_transform(tfidf_train)

# Train the model
model = LogisticRegression(C=30, dual=True)
model.fit(tfidf_train, y_train)

# Save it
filename = 'model/vector.sav'
vect.tokenizer = None
pickle.dump(vect, open(filename, 'wb'))

filename = 'model/political.sav'
pickle.dump(model, open(filename, 'wb'))
