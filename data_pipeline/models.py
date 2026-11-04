from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Article:
    title: str #headline
    url: str #Original article URL
    source: str #News outlet
    author: Optional[str] #Author, if available
    published_date: Optional[datetime] #Publication date, if available
    cleaned_text: str #Article text after cleaning