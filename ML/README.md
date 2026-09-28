# Article Clustering and RNN Sentiment Analysis

## Overview
The machine learning pipeline will consist of clustering, keyword extraction, and RNN sentiment scoring to effectively analyze different articles and group them based on similarities in their sentiments, wording, and potential biases.

## Steps
1. Text Preprocessing
2. Document Embedding
3. DBSCAN Clustering
4. Keyword Extraction with YAKE
5. Sentiment Analysis
6. Bias Analysis

## Run and Test Instructions
Run main.py to see current keyword extractions over a set of mock data from scikit-learn's 20newsgroup dataset.

## Status
Currently Implemented:
- Mini preprocessing for basic text cleaning
- Sentence Transformer embeddings
- K-Means clustering
- YAKE keyword extraction 

In Development:
- Sentiment Model
- Bias Model