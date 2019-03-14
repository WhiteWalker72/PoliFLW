import pandas as pd
import json
from tfidf import TFIDF
from preparation import Preparation


class Analysis:

    def __init__(self):
        self.preparation = Preparation()
        self.tfidf = TFIDF()

    def get_dataframe_from_json(self, json_data) -> pd.DataFrame:
        # convert json file to a pandas dataframe
        dataframe = self.preparation.jsonfile_to_dataframe(json.load(json_data))

        # refine the dataframe by removing entries that containt no articles
        dataframe = self.preparation.refine_dataframe(dataframe)
        return dataframe

    def get_tfidf_from_dataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        return self.tfidf.get_tfidf_dataframe(dataframe)
