from datetime import datetime
from typing import Optional
#from urllib.parse import urlparse --dont need yet

from data_pipeline.models import Article


def normalize_source(source: Optional[str]) -> str:
    #Normalize the news source name
    if not source:
        return ""

    return " ".join(source.strip().split())


def normalize_author(author: Optional[str]) -> Optional[str]:
    #Normalize an article author's name
    if not author:
        return None

    author = " ".join(author.strip().split())
    return author if author else None


def normalize_url(url: str) -> str:
    #Normalize an article URL
    if not url:
        return ""

    return url.strip()


def normalize_date(date_value) -> Optional[datetime]:
    #Convert common date formats into a datetime object
    if not date_value:
        return None

    if isinstance(date_value, datetime):
        return date_value

    if isinstance(date_value, str):
        date_value = date_value.strip()

        #Handle ISO dates such as 2026-09-08 or 2026-09-08T14:30:00
        try:
            return datetime.fromisoformat(date_value.replace("Z", "+00:00"))
        except ValueError:
            pass

        #Handle a common date format such as September 8, 2026
        try:
            return datetime.strptime(date_value, "%B %d, %Y")
        except ValueError:
            pass

    return None


def normalize_article(article: dict) -> Article:
    #Convert a raw article dictionary into our standard Article format
    return Article(
        title=" ".join(article.get("title", "").strip().split()),
        url=normalize_url(article.get("url", "")),
        source=normalize_source(article.get("source")),
        author=normalize_author(article.get("author")),
        published_date=normalize_date(article.get("published_date")),
        cleaned_text=article.get("cleaned_text", "").strip(),
    )