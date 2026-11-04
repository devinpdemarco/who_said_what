
import os
from dataclasses import asdict, is_dataclass
from datetime import datetime

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()


def get_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY")

    return create_client(url, key)


def save_articles(articles, client=None):
    """Save valid processed articles to Supabase."""

    if not articles:
        print("No articles to save.")
        return []

    rows = []

    for article in articles:
        row = asdict(article) if is_dataclass(article) else article.copy()

        published_date = row.get("published_date")

        if isinstance(published_date, datetime):
            row["published_date"] = published_date.isoformat()

        rows.append(row)

    database = client or get_client()
    response = database.table("articles").insert(rows).execute()

    print(f"Successfully saved {len(response.data)} articles!")
    return response.data
