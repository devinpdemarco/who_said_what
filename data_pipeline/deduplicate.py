import hashlib
import re
from typing import List

from data_pipeline.models import Article


def normalize_for_comparison(text: str) -> str:
    #Normalize text so similar articles can be compared
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_content_hash(text: str) -> str:
    #Create a hash from article text
    normalized_text = normalize_for_comparison(text)
    return hashlib.sha256(normalized_text.encode("utf-8")).hexdigest()


def deduplicate_articles(articles: List[Article]) -> List[Article]:
    """
    Remove duplicate articles.

    Articles are considered duplicates if they have the same URL
    or identical cleaned article text.
    """
    seen_urls = set()
    seen_content = set()
    unique_articles = []

    for article in articles:
        url = article.url.strip().lower()
        content_hash = get_content_hash(article.cleaned_text)

        if url and url in seen_urls:
            continue

        if content_hash in seen_content:
            continue

        if url:
            seen_urls.add(url)

        seen_content.add(content_hash)
        unique_articles.append(article)

    return unique_articles