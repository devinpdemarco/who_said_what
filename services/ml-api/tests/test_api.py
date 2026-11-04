from fastapi.testclient import TestClient

from app import main
from app.main import app


client = TestClient(app)


def test_health_reports_adapter_ready() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "ml-api",
        "pipeline_connected": True,
    }


def test_analyze_rejects_empty_article_list() -> None:
    response = client.post("/analyze", json={"articles": []})

    assert response.status_code == 422


def test_analyze_calls_pipeline_and_returns_results(monkeypatch) -> None:
    received_articles = []
    expected = {
        "articles": [
            {
                "article_id": "article-1",
                "sentiment_scoring": {"label": "neutral", "confidence": 0.8},
            }
        ],
        "clusters": [],
    }

    def fake_pipeline(articles):
        received_articles.extend(articles)
        return expected

    monkeypatch.setattr(main, "run_pipeline", fake_pipeline)
    response = client.post(
        "/analyze",
        json={
            "articles": [
                {
                    "id": "article-1",
                    "title": "Example",
                    "url": "https://example.com/article",
                    "source": "Example News",
                    "cleaned_text": "Example article text.",
                }
            ]
        },
    )

    assert response.status_code == 200
    assert response.json() == expected
    assert received_articles == [
        {
            "id": "article-1",
            "title": "Example",
            "url": "https://example.com/article",
            "source": "Example News",
            "cleaned_text": "Example article text.",
        }
    ]
