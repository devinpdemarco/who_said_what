from dataclasses import replace

from fastapi.testclient import TestClient

from app import main
from app.main import app
from data_pipeline.models import Article


client = TestClient(app)


def test_health_reports_service_ready() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "data-api"}


def test_process_cleans_saves_and_returns_articles(monkeypatch) -> None:
    processed = Article(
        title="Example Article",
        url="https://example.com/article",
        source="Example News",
        author=None,
        published_date=None,
        cleaned_text="Clean article text.",
    )
    invalid = replace(processed, title="")
    saved = [{"id": "article-1", **processed.__dict__}]
    received = {}

    def fake_process(raw_articles):
        received["raw_articles"] = raw_articles
        return [processed], [invalid]

    def fake_save(valid_articles):
        received["valid_articles"] = valid_articles
        return saved

    monkeypatch.setattr(main, "process_articles", fake_process)
    monkeypatch.setattr(main, "save_articles", fake_save)

    response = client.post(
        "/process",
        json={
            "articles": [
                {
                    "title": "Example Article",
                    "url": "https://example.com/article",
                    "source": "Example News",
                    "raw_content": "<p>Clean article text.</p>",
                }
            ]
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "valid_articles": saved,
        "invalid_count": 1,
    }
    assert received["raw_articles"][0]["raw_content"] == (
        "<p>Clean article text.</p>"
    )
    assert received["valid_articles"] == [processed]


def test_process_rejects_empty_article_list() -> None:
    response = client.post("/process", json={"articles": []})

    assert response.status_code == 422
