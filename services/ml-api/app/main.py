"""HTTP boundary for the machine-learning pipeline."""

from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel, Field, HttpUrl

from app.pipeline import run_pipeline


app = FastAPI(title="Who Said What ML API", version="0.1.0")


class Article(BaseModel):
    id: str | int | None = None
    title: str
    url: HttpUrl
    source: str
    cleaned_text: str


class AnalyzeRequest(BaseModel):
    articles: Annotated[list[Article], Field(min_length=1)]


@app.get("/health")
def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "service": "ml-api",
        "pipeline_connected": True,
    }


@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> dict:
    articles = [
        article.model_dump(mode="json", exclude_none=True)
        for article in request.articles
    ]
    return run_pipeline(articles)
