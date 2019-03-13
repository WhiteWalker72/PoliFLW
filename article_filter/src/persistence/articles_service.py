from src.persistence.mongodb import articles_collection as collection


def find_articles():
    return list(collection.find())


def find_similar_articles(text, minimum_score):
    articles_found = list(collection.find({"$text": {"$search": text}}, {'score': {"$meta": "textScore"}}))
    filtered = list(filter(lambda x: x['score'] >= minimum_score, articles_found))
    return sorted(filtered, key=lambda x: x['score'], reverse=True)


def find_article(url):
    return collection.find_one({'url': url})


def insert_article(article):
    collection.insert_one(article)


def delete_article(url):
    return collection.delete_one({'url': url})

