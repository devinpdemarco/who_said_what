from preprocessing import preprocess_data, structure_data
from embeddings import create_embeddings
from clustering import find_best_k, create_clusters, package_cluster_info
from keyword_extraction import extract_keywords
from analyze_sentiment import run_sentiment_analysis

import numpy as np
import json
''' uncomment this when integrating with data pipeline
import os
from supabase import create_client
'''

def load_dev_test_data():
    with open('ML/news_sentiment_20_labeled.json', 'r', encoding='utf-8') as file:
        articles = json.load(file)

        data = []

        for doc in articles:
            data.append(
                doc['text']
            )

    return data

'''
for integration with data pipeline
uncomment when ready to integrate

def load_articles():
    client = create_client(
        os.environ['SUPABASE_URL']
        os.environ['SUPABASE_KEY']
    )

    response = (
        client.table('articles')
        .select('id', 'title', 'cleaned_text')
        .limit(20)
        .execute()
    )

    return [
        {
            'id' : str(row['id']),
            'title' : row['title'],
            'text' : row['cleaned_text']
        }

        for row in response.data
    ]

    
articles = load_articles()
'''

# for development and testing ML pipeline
data = load_dev_test_data()


# preprocessing data
data = preprocess_data(data)
# structuring sample data to match how i will use the real data from data pipeline
articles = structure_data(data)

'''
input data received from data pipeline
table name is articles

{
    'id':'123',
    'title':'...',
    'source':'...',
    'cleaned_text':'...'
}
'''

# will replace sample data will real data soon
# not quite sure how the ingestion is working
# will update by EOD on 11/01


# create sentence transformer embeddings
embeddings = create_embeddings(data)

# create clusters using k-means
k = find_best_k(embeddings)
labels = create_clusters(embeddings, k)

# discarding clusters for keyword extraction if not sufficient data for extraction
# may change this later
cluster_labels, counts = np.unique(labels, return_counts=True)
min_cluster_size = 3 # at least 100 docs in each cluster
valid_labels = [
    label for label, count in zip(cluster_labels, counts)
    if count >= min_cluster_size
]

# performing the keyword extraction using yake
clustered_keywords = extract_keywords(labels, valid_labels, data)

cluster_info = package_cluster_info(labels, articles, clustered_keywords, valid_labels)

sentiment_results = run_sentiment_analysis(articles)

ml_results = {
    'articles' : sentiment_results,
    'clusters' : cluster_info
}

for i in range(20):
    print(ml_results['articles'][i])

print(ml_results['clusters'])