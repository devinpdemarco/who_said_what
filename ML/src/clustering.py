from sklearn.cluster import KMeans
# source: https://www.geeksforgeeks.org/machine-learning/clustering-text-documents-using-k-means-in-scikit-learn/

def create_clusters(embeddings, n_clusters):
        
    # applying clustering
    num_clusters = n_clusters
    kmeans= KMeans(n_clusters=num_clusters, n_init=5, max_iter=500, random_state=42)
    kmeans.fit(embeddings)
    cluster_labels = kmeans.labels_

    return cluster_labels, kmeans
