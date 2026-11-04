# Article Clustering and Sentiment Analysis

## Overview
The machine learning pipeline will consist of clustering, keyword extraction, and sentiment scoring to effectively analyze different articles and group them based on similarities in their sentiments, wording, and potential biases.

## Steps
1. Text Preprocessing
2. Document Embedding
3. K-Means Clustering
4. Keyword Extraction with YAKE
5. Sentiment Analysis
6. Bias Analysis

## Run and Test Instructions
Run main.py to see current clustering and sentiment analysis results over a set of curated mock data that mimics news articles syntax and topics.

The pipeline can also be called directly from another Python program:

```python
from ML.src.main import analyze_articles

ml_results = analyze_articles(articles)
```

Each article must contain `cleaned_text`. Existing `id` values are kept in the returned article and cluster results; if an article has no `id`, its list index is used.

## Status
Currently Implemented:
- Mini preprocessing for basic text cleaning
- Sentence Transformer embeddings
- K-Means clustering
- YAKE keyword extraction 
- Sentiment Analysis

In Development:
- Bias Model
