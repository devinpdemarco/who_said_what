from sklearn.cluster import KMeans
import numpy as np
# source: https://www.geeksforgeeks.org/machine-learning/clustering-text-documents-using-k-means-in-scikit-learn/

def create_clusters(embeddings, n_clusters):
        
    # applying clustering
    num_clusters = n_clusters
    kmeans= KMeans(n_clusters=num_clusters, n_init=5, max_iter=500, random_state=42)
    kmeans.fit(embeddings)
    cluster_labels = kmeans.labels_

    return cluster_labels, kmeans

def package_cluster_info(labels, articles, clustered_keywords, valid_labels):
    cluster_labels, counts = np.unique(labels, return_counts=True)

    cluster_info = []

    for label, count in zip(cluster_labels, counts):
        article_ids = []
        num_articles = count.item()
        
        for index,l in enumerate(labels):
            if l==label:
                article_ids.append(articles[index]['id'])

        if label in valid_labels:
            keywords = clustered_keywords[label]
            keyword_info = []
            for kw, score in keywords:
                keyword_info.append(
                    {
                        'text' : kw,
                        'weight' : score.item()
                    }
                )
        else:
            keyword_info = []
        
        cluster_info.append(
            {
                'cluster_id' : label.item(),
                'num_articles' : num_articles,
                'article_ids' : article_ids,
                'keywords' : keyword_info
            }
        )

    return cluster_info

