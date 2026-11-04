from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel, Field

from data_pipeline.pipeline import process_articles
from supabase_client import save_articles


app = FastAPI(title="Who Said What Data API", version="0.1.0")


class RawArticle(BaseModel):
    title: str = ""
    url: str = ""
    source: str = ""
    author: str | None = None
    published_date: str | None = None
    raw_content: str = ""


class ProcessRequest(BaseModel):
    articles: Annotated[list[RawArticle], Field(min_length=1)]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "data-api"}


@app.post("/process")
def process(request: ProcessRequest) -> dict:
    raw_articles = [article.model_dump() for article in request.articles]
    valid_articles, invalid_articles = process_articles(raw_articles)
    saved_articles = save_articles(valid_articles)

    return {
        "valid_articles": saved_articles,
        "invalid_count": len(invalid_articles),
    }
