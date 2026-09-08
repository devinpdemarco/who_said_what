from data_pipeline.clean import clean_text
from data_pipeline.deduplicate import deduplicate_articles
from data_pipeline.ingest import load_articles_from_json
from data_pipeline.models import Article
from data_pipeline.normalize import normalize_article
from data_pipeline.validate import validate_articles


def process_articles(raw_articles: list[dict]) -> tuple[list[Article], list[Article]]:
    """
    Run raw articles through the complete data processing pipeline.

    Steps:
        1. Clean article text
        2. Normalize metadata
        3. Deduplicate articles
        4. Validate required fields

    Returns:
        valid_articles: Articles ready for storage/ML.
        invalid_articles: Articles that failed validation.
    """

    processed_articles = []

    for raw_article in raw_articles:
        #Clean the raw article text first
        cleaned_text = clean_text(raw_article.get("raw_content", ""))

        #Add cleaned text so normalize_article can use it
        raw_article = raw_article.copy()
        raw_article["cleaned_text"] = cleaned_text

        #Convert raw data into our standard Article format
        article = normalize_article(raw_article)

        processed_articles.append(article)

    #Remove duplicate articles
    unique_articles = deduplicate_articles(processed_articles)

    #Separate valid and invalid articles
    valid_articles, invalid_articles = validate_articles(unique_articles)

    return valid_articles, invalid_articles


def run_pipeline(file_path: str) -> tuple[list[Article], list[Article]]:
    #Load articles from JSON and process them through the pipeline.

    raw_articles = load_articles_from_json(file_path)

    return process_articles(raw_articles)


if __name__ == "__main__":
    valid, invalid = run_pipeline("data/sample_articles.json")

    print(f"Valid articles: {len(valid)}")
    print(f"Invalid articles: {len(invalid)}")

    for article in valid:
        print("\n--- Article ---")
        print(f"Title: {article.title}")
        print(f"Source: {article.source}")
        print(f"URL: {article.url}")
        print(f"Text: {article.cleaned_text}")