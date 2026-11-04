import re
from bs4 import BeautifulSoup


def clean_text(text: str) -> str:
    
    #Clean article text by removing HTML, URLs, and unnecessary whitespace.
    
    if not text:
        return ""

    #Remove HTML tags
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text(" ")

    #Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", "", text)

    #Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    #Remove leading/trailing whitespace
    return text.strip()