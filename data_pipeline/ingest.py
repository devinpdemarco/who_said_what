import json
from pathlib import Path


def load_articles_from_json(file_path: str) -> list[dict]:
    """
    Load raw articles from a JSON file.

    The JSON file should contain a list of article objects.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Article file not found: {file_path}")

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Article JSON must contain a list of articles.")

    return data