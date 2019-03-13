import pandas as pd
import math
import os
from definitions import ROOT_DIR


def get_root_path():
    return os.path.abspath(os.sep)


df = pd.read_csv(ROOT_DIR + '/src/data/osf_urls.csv', names=[
    'RegioNaam', 'RegioCode', 'Amsterdamsecode', 'Partij', 'AantalZetels', 'Website', 'Facebook', 'Engine'
    , 'Feed', 'Full_content'
])

websites = [row["Website"] for index, row in df[['Website']].iterrows()]
websites = list(filter(lambda x: type(x) is str or not math.isnan(x), websites))


def main():
    for website in websites:
        print(website)


if __name__ == "__main__":
        main()


