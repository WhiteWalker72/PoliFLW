import pandas as pd
import os
from definitions import ROOT_DIR
from src.persistence.sources_service import add_source, get_websites


def get_root_path():
    return os.path.abspath(os.sep)


df = pd.read_csv(ROOT_DIR + '/src/data/osf_urls.csv', names=[
    'RegioNaam', 'RegioCode', 'Amsterdamsecode', 'Partij', 'AantalZetels', 'Website', 'Facebook', 'Engine'
    , 'Feed', 'Full_content'
])


def add_to_collection():
    for index, row in df.iterrows():
        doc = {
            'regionName': row['RegioNaam'],
            'regionCode': row['RegioCode'],
            'amsterdamCode': row['Amsterdamsecode'],
            'politicalParty': row['Partij'],
            'numberOfSeats': row['AantalZetels'],
            'website': row['Website'],
            'facebook': row['Facebook'],
            'engine': row['Engine'],
            'feed': row['Feed'],
            'fullContent': row['Full_content']
        }
        add_source(doc)


def main():
    print(get_websites())


if __name__ == "__main__":
        main()


