import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).parents[1] / "src" / "analyze_sentiment.py"


class SentimentModelTests(unittest.TestCase):
    def test_model_is_loaded_once_for_multiple_predictions(self):
        calls = {"model": 0, "tokenizer": 0, "pipeline": 0}
        transformers = types.ModuleType("transformers")

        class Model:
            config = types.SimpleNamespace(base_name_or_path="base-model")

        class AutoModel:
            @staticmethod
            def from_pretrained(*args, **kwargs):
                calls["model"] += 1
                return Model()

        class AutoTokenizer:
            @staticmethod
            def from_pretrained(*args, **kwargs):
                calls["tokenizer"] += 1
                return object()

        def pipeline(*args, **kwargs):
            calls["pipeline"] += 1
            return lambda *args, **kwargs: {
                "sentiment": {"label": 0, "score": 0.9}
            }

        transformers.AutoModel = AutoModel
        transformers.AutoTokenizer = AutoTokenizer
        transformers.pipeline = pipeline

        with patch.dict(sys.modules, {"transformers": transformers}):
            spec = importlib.util.spec_from_file_location(
                "sentiment_under_test", MODULE_PATH
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.predict_sentiment("first")
            module.predict_sentiment("second")

        self.assertEqual(calls, {"model": 1, "tokenizer": 1, "pipeline": 1})


if __name__ == "__main__":
    unittest.main()
