from dataclasses import dataclass

import supabase_client


@dataclass
class SavedArticle:
    title: str
    published_date: object = None


def test_save_articles_uses_injected_client() -> None:
    inserted = {}

    class Query:
        def insert(self, rows):
            inserted["rows"] = rows
            return self

        def execute(self):
            return type("Response", (), {"data": inserted["rows"]})()

    class Client:
        def table(self, name):
            inserted["table"] = name
            return Query()

    result = supabase_client.save_articles(
        [SavedArticle(title="Example")], client=Client()
    )

    assert inserted == {
        "table": "articles",
        "rows": [{"title": "Example", "published_date": None}],
    }
    assert result == inserted["rows"]
