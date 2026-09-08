from data_pipeline.pipeline import process_articles


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