def run_pipeline(articles: list[dict]) -> dict:
    """Load and call the ML pipeline only when analysis is requested."""
    from ML.src.main import analyze_articles

    return analyze_articles(articles)
