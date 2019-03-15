from src.persistence import article_service


def get_articles():
    articles = article_service.find_articles()
    for article in articles:
        article.pop('_id', None)
    return articles
