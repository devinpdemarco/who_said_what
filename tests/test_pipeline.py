from data_pipeline.clean import clean_text
from data_pipeline.deduplicate import deduplicate_articles
from data_pipeline.models import Article
from data_pipeline.normalize import normalize_article
from data_pipeline.pipeline import process_articles
from data_pipeline.validate import validate_article


def test_clean_text():
    text = "<p>Hello   world!</p>"
    result = clean_text(text)

    assert result == "Hello world!"


def test_normalize_article():
    raw_article = {
        "title": "  Example   Article  ",
        "url": "https://example.com/article",
        "source": "  Example News  ",
        "author": " John Smith ",
        "published_date": "2026-09-08",
        "cleaned_text": " Some article text. ",
    }

    article = normalize_article(raw_article)

    assert article.title == "Example Article"
    assert article.url == "https://example.com/article"
    assert article.source == "Example News"
    assert article.author == "John Smith"
    assert article.cleaned_text == "Some article text."


def test_deduplicate_articles():
    article1 = Article(
        title="News Story",
        url="https://example.com/story",
        source="Example News",
        author="John Smith",
        published_date=None,
        cleaned_text="This is the article text.",
    )

    article2 = Article(
        title="Same Story",
        url="https://example.com/story",
        source="Example News",
        author="Jane Doe",
        published_date=None,
        cleaned_text="This is the article text.",
    )

    result = deduplicate_articles([article1, article2])

    assert len(result) == 1


def test_validate_article():
    valid_article = Article(
        title="News Story",
        url="https://example.com/story",
        source="Example News",
        author="John Smith",
        published_date=None,
        cleaned_text="This is the article text.",
    )

    invalid_article = Article(
        title="",
        url="https://example.com/story",
        source="Example News",
        author="John Smith",
        published_date=None,
        cleaned_text="This is the article text.",
    )

    assert validate_article(valid_article) is True
    assert validate_article(invalid_article) is False


def test_pipeline_processes_articles():
    raw_articles = [
        {
            "title": "  Example   Article  ",
            "url": "https://example.com/article",
            "source": "  Example News  ",
            "author": " John Smith ",
            "published_date": "2026-09-08",
            "raw_content": "<p>This is   an article.</p>",
        }
    ]

    valid, invalid = process_articles(raw_articles)

    assert len(valid) == 1
    assert len(invalid) == 0

    article = valid[0]

    assert article.title == "Example Article"
    assert article.source == "Example News"
    assert article.author == "John Smith"
    assert article.cleaned_text == "This is an article."


def test_pipeline_rejects_invalid_article():
    raw_articles = [
        {
            "title": "",
            "url": "https://example.com/article",
            "source": "Example News",
            "author": "John Smith",
            "published_date": "2026-09-08",
            "raw_content": "<p>This article is missing a title.</p>",
        }
    ]

    valid, invalid = process_articles(raw_articles)

    assert len(valid) == 0
    assert len(invalid) == 1
    def test_clean_text_handles_messy_html():
        text = """
        <html>
            <head>
                <style>body { color: red; }</style>
            </head>
            <body>
                <h1>Breaking News</h1>
                <p>This is   the article content.</p>
                <script>someJavascript();</script>
                <p>More information is available here.</p>
            </body>
        </html>
        """

        result = clean_text(text)

        assert "Breaking News" in result
        assert "This is the article content." in result
        assert "More information is available here." in result
        assert "someJavascript" not in result
        assert "body { color: red; }" not in result
def test_deduplicate_articles_with_same_content():
    article1 = Article(
        title="News Story",
        url="https://example.com/story-1",
        source="Example News",
        author="John Smith",
        published_date=None,
        cleaned_text="This is the same article content.",
    )

    article2 = Article(
        title="News Story",
        url="https://example.com/story-2",
        source="Example News",
        author="John Smith",
        published_date=None,
        cleaned_text="This is the same article content.",
    )

    result = deduplicate_articles([article1, article2])

    assert len(result) == 1
