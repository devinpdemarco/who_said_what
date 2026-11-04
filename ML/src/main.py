import json
from pathlib import Path

import numpy as np

try:
    from .analyze_sentiment import run_sentiment_analysis
    from .clustering import create_clusters, find_best_k, package_cluster_info
    from .embeddings import create_embeddings
    from .keyword_extraction import extract_keywords
    from .preprocessing import preprocess_data
except ImportError:
    from analyze_sentiment import run_sentiment_analysis
    from clustering import create_clusters, find_best_k, package_cluster_info
    from embeddings import create_embeddings
    from keyword_extraction import extract_keywords
    from preprocessing import preprocess_data


def analyze_articles(articles):
    """Run the ML pipeline on article dictionaries and return its results."""
    if not articles:
        raise ValueError("articles must be a non-empty list")

    prepared_articles = []
    article_text = []

    for index, article in enumerate(articles):
        if not isinstance(article, dict):
            raise ValueError("each article must be a dictionary")

        text = article.get("cleaned_text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("each article must include non-empty cleaned_text")

        prepared_article = article.copy()
        prepared_article.setdefault("id", index)
        prepared_articles.append(prepared_article)
        article_text.append(text)

    processed_text = preprocess_data(article_text)

    for article, text in zip(prepared_articles, processed_text):
        article["cleaned_text"] = text

    embeddings = create_embeddings(processed_text)
    k = find_best_k(embeddings)
    labels = create_clusters(embeddings, k)

    cluster_labels, counts = np.unique(labels, return_counts=True)
    min_cluster_size = 3
    valid_labels = [
        label
        for label, count in zip(cluster_labels, counts)
        if count >= min_cluster_size
    ]

    clustered_keywords = extract_keywords(labels, valid_labels, processed_text)
    cluster_info = package_cluster_info(
        labels, prepared_articles, clustered_keywords, valid_labels
    )
    sentiment_results = run_sentiment_analysis(prepared_articles)

    return {
        "articles": sentiment_results,
        "clusters": cluster_info,
    }


def load_dev_test_articles():
    data_path = Path(__file__).parents[1] / "news_sentiment_20_labeled.json"
    with data_path.open("r", encoding="utf-8") as file:
        documents = json.load(file)

    return [
        {
            "id": document.get("id", index),
            "title": document.get("title", ""),
            "cleaned_text": document["text"],
        }
        for index, document in enumerate(documents)
    ]


def main():
    ml_results = analyze_articles(load_dev_test_articles())

    for article_result in ml_results["articles"]:
        print(article_result)

    print(ml_results["clusters"])


if __name__ == "__main__":
    main()
