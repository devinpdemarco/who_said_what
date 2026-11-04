from typing import List

from data_pipeline.models import Article


REQUIRED_FIELDS = [
    "title",
    "url",
    "source",
    "cleaned_text",
]


def validate_article(article: Article) -> bool:
    #Check whether an article contains all required fields.
    

    for field in REQUIRED_FIELDS:
        value = getattr(article, field, None)

        if not value or not str(value).strip():
            return False

    return True


def validate_articles(articles: List[Article]) -> tuple[List[Article], List[Article]]:
    """
    Separate valid articles from invalid articles.

    Returns:
        valid_articles: Articles that contain all required fields.
        invalid_articles: Articles missing one or more required fields.
    """

    valid_articles = []
    invalid_articles = []

    for article in articles:
        if validate_article(article):
            valid_articles.append(article)
        else:
            invalid_articles.append(article)

    return valid_articles, invalid_articles