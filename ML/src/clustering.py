from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import davies_bouldin_score
import numpy as np
# source: https://www.geeksforgeeks.org/machine-learning/clustering-text-documents-using-k-means-in-scikit-learn/


# source: https://www.geeksforgeeks.org/machine-learning/clustering-text-documents-using-k-means-in-scikit-learn/
def find_best_k(embeddings):
    best_sil_score = -1
    best_db_score = 99999
    best_k = 2
    for k in range(2,8):
        kmeans=KMeans(n_clusters=k, n_init=5, max_iter=500, random_state=42)
        labels = kmeans.fit_predict(embeddings)

        if len(set(labels)) != k:
            continue

        silh_score=silhouette_score(embeddings, labels)
        db_score = davies_bouldin_score(embeddings, labels)
        if (round(silh_score,2) > best_sil_score) or (round(db_score,2)< best_db_score):

            best_sil_score = silh_score
            best_db_score = db_score
            best_k = k


    #print(f'Best silhouette score: {best_sil_score:.2f}')
    return best_k

def create_clusters(embeddings, n_clusters):
        
    # applying clustering
    kmeans= KMeans(n_clusters=n_clusters, n_init=5, max_iter=500, random_state=42)
    labels = kmeans.fit_predict(embeddings)

    return labels

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

