
import os

import pytest

from data_pipeline.pipeline import process_articles
from supabase_client import save_articles


@pytest.mark.skipif(
    not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"),
    reason="Supabase credentials are not configured",
)
def test_save_processed_articles():
    raw_articles = [
        {
            "title": "Example News Article",
            "url": "https://example.com/article-1",
            "source": "Example News",
            "author": "Jane Doe",
            "published_date": "2026-11-03",
            "raw_content": "This is an example article about a recent event."
        }
    ]

    valid_articles, invalid_articles = process_articles(raw_articles)

    assert len(valid_articles) == 1
    assert len(invalid_articles) == 0

    saved_articles = save_articles(valid_articles)

    assert len(saved_articles) == 1
    assert saved_articles[0]["title"] == "Example News Article"
