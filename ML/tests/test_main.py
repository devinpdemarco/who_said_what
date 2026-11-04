import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


MAIN_PATH = Path(__file__).parents[1] / "src" / "main.py"


def load_main_module(calls):
    preprocessing = types.ModuleType("preprocessing")

    def preprocess_data(data):
        calls.append("preprocess")
        return [text.lower() for text in data]

    preprocessing.preprocess_data = preprocess_data
    preprocessing.structure_data = lambda data: [
        {"id": index, "cleaned_text": text}
        for index, text in enumerate(data)
    ]

    embeddings = types.ModuleType("embeddings")
    embeddings.create_embeddings = lambda data: calls.append("embed") or data

    clustering = types.ModuleType("clustering")
    clustering.find_best_k = lambda data: 2
    clustering.create_clusters = lambda data, k: [0, 0, 0]
    clustering.package_cluster_info = lambda labels, articles, keywords, valid: [
        {"cluster_id": 0, "article_ids": [article["id"] for article in articles]}
    ]

    keywords = types.ModuleType("keyword_extraction")
    keywords.extract_keywords = lambda labels, valid, data: {0: [("news", 0.1)]}

    sentiment = types.ModuleType("analyze_sentiment")
    sentiment.run_sentiment_analysis = lambda articles: [
        {"article_id": article["id"], "sentiment_scoring": {"label": "neutral"}}
        for article in articles
    ]

    numpy = types.ModuleType("numpy")
    numpy.unique = lambda labels, return_counts: ([0], [3])

    modules = {
        "preprocessing": preprocessing,
        "embeddings": embeddings,
        "clustering": clustering,
        "keyword_extraction": keywords,
        "analyze_sentiment": sentiment,
        "numpy": numpy,
    }

    with patch.dict(sys.modules, modules):
        spec = importlib.util.spec_from_file_location("ml_main_under_test", MAIN_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


class AnalyzeArticlesTests(unittest.TestCase):
    def test_import_does_not_run_pipeline(self):
        calls = []

        load_main_module(calls)

        self.assertEqual(calls, [])

    def test_rejects_empty_article_list(self):
        module = load_main_module([])

        with self.assertRaisesRegex(ValueError, "non-empty"):
            module.analyze_articles([])

    def test_returns_article_and_cluster_results(self):
        calls = []
        module = load_main_module(calls)
        articles = [
            {"id": "a1", "title": "One", "cleaned_text": "FIRST ARTICLE"},
            {"id": "a2", "title": "Two", "cleaned_text": "SECOND ARTICLE"},
            {"id": "a3", "title": "Three", "cleaned_text": "THIRD ARTICLE"},
        ]

        result = module.analyze_articles(articles)

        self.assertEqual(
            [item["article_id"] for item in result["articles"]],
            ["a1", "a2", "a3"],
        )
        self.assertEqual(result["clusters"][0]["article_ids"], ["a1", "a2", "a3"])
        self.assertEqual(calls, ["preprocess", "embed"])


if __name__ == "__main__":
    unittest.main()
