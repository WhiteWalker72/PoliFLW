from mongodb import sources_collection as collection


def find_all_articles():
    return list(collection.find())


def get_articles(keyword: str) -> list:
    return list(collection.find({'tfidf': {'$regex': keyword}}).limit(10))


def add_article(tfidf):
    collection.insert_one(tfidf)
