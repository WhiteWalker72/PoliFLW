import json
import requests

from analysis import Analysis


def find_all_documents_poliflow():
    """
    This function searches for all possible articles through the API of Poliflow.
    """
    BASE_URL = 'https://api.poliflw.nl/v0/search?scroll=1m'

    scroll_id = ''
    total_results, total_size, size = 0, 0, 100

    all_data = []
    while not total_size or total_results < total_size:
        try:
            if scroll_id:
                result = requests.get(BASE_URL + '&size=' + str(size) + '&scroll_id=' + scroll_id)
            else:
                result = requests.get(BASE_URL + '&size=' + str(size))

            data = result.json()

            scroll_id = data['meta']['scroll']
            total_size = data['meta']['total']

            total_results += size

            print('%s/%s' % (total_results, total_size))

            if total_results > 1000:
                break

            if 'item' in data:
                all_data += data['item']
        except:
            print('Error')

    return all_data


def save_all_documents_poliflow(data):
    """
    This function dumps the found data in a json-file.
    """
    with open('data.json', 'w') as OUT:
        json.dump(data, OUT)


anal = Analysis()

# Get data from Poliflw and save it.
# This should be in input from the article filter later
data = find_all_documents_poliflow()
save_all_documents_poliflow(data)

# load the data by opening the json file
with open('data.json', encoding='utf-8') as data:
    dataframe = anal.get_dataframe_from_json(data)

tfidf_dateframe = anal.get_tfidf_from_dataframe(dataframe)
tfidf_json = tfidf_dateframe.to_json(orient='records')
print('We are done!')
