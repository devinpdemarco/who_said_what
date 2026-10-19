"""Stable HTTP boundary for the machine-learning pipeline.

Kynnedy's pipeline will be connected behind ``/analyze`` once its callable
entry point and runtime dependencies are agreed. Until then, the endpoint
fails explicitly instead of returning invented analysis data.
"""

from typing import Annotated

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, HttpUrl


app = FastAPI(title="Who Said What ML API", version="0.1.0")


class Article(BaseModel):
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
        "pipeline_connected": False,
    }


@app.post("/analyze")
def analyze(_: AnalyzeRequest) -> None:
    raise HTTPException(
        status_code=503,
        detail="ML pipeline is not connected yet. Contact the ML owner.",
    )
