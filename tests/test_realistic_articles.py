
from data_pipeline.normalize import normalize_article
from data_pipeline.validate import validate_article
from data_pipeline.deduplicate import deduplicate_articles
from data_pipeline.pipeline import process_articles


def test_normalize_realistic_article():
    raw_article = {
        "title": "  Breaking   News  ",
        "url": " https://example.com/news ",
        "source": " Example   News ",
        "author": " Jane Doe ",
        "published_date": "2026-10-19",
        "cleaned_text": " Article text here. "
    }

    article = normalize_article(raw_article)

    assert article.title == "Breaking News"
    assert article.source == "Example News"
    assert article.author == "Jane Doe"
    assert article.url == "https://example.com/news"
    assert article.cleaned_text == "Article text here."
    assert article.published_date is not None


def test_article_with_missing_optional_fields():
    raw_article = {
        "title": "Example News",
        "url": "https://example.com",
        "source": "Example",
        "cleaned_text": "Some article text."
    }

    article = normalize_article(raw_article)

    assert article.author is None
    assert article.published_date is None
    assert validate_article(article)


def test_article_missing_required_field():
    raw_article = {
        "title": "",
        "url": "https://example.com",
        "source": "Example",
        "cleaned_text": "Some article text."
    }

    article = normalize_article(raw_article)

    assert not validate_article(article)


def test_duplicate_articles():
    article1 = normalize_article({
        "title": "News One",
        "url": "https://example.com/1",
        "source": "Example",
        "cleaned_text": "This is the same article."
    })

    article2 = normalize_article({
        "title": "News Two",
        "url": "https://example.com/1",
        "source": "Example",
        "cleaned_text": "Different article text."
    })

    unique = deduplicate_articles([article1, article2])

    assert len(unique) == 1


def test_complete_pipeline():
    raw_articles = [
        {
            "title": "  Example News  ",
            "url": "https://example.com/1",
            "source": "Example News",
            "raw_content": "  This is an example article.  "
        },
        {
            "title": "Duplicate News",
            "url": "https://example.com/1",
            "source": "Example News",
            "raw_content": "Different article text."
        },
        {
            "title": "",
            "url": "https://example.com/3",
            "source": "Example News",
            "raw_content": "Article with missing title."
        }
    ]

    valid, invalid = process_articles(raw_articles)

    assert len(valid) == 1
    assert len(invalid) == 1

    assert valid[0].title == "Example News"
    assert valid[0].cleaned_text == "This is an example article."

    assert invalid[0].title == ""