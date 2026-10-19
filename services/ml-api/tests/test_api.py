from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_reports_adapter_ready() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "ml-api",
        "pipeline_connected": False,
    }


def test_analyze_rejects_empty_article_list() -> None:
    response = client.post("/analyze", json={"articles": []})

    assert response.status_code == 422


def test_analyze_reports_pipeline_not_connected() -> None:
    response = client.post(
        "/analyze",
        json={
            "articles": [
                {
                    "title": "Example",
                    "url": "https://example.com/article",
                    "source": "Example News",
                    "cleaned_text": "Example article text.",
                }
            ]
        },
    )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "ML pipeline is not connected yet. Contact the ML owner."
    }
