from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.metrics import adjusted_rand_score

def evaluate_clustering(embeddings, labels, target_labels):
    num_clusters = len(set(labels))
    num_noise = list(labels).count(-1)
    silh_score = silhouette_score(embeddings, labels)
    adj_rand_ind = adjusted_rand_score(target_labels, labels)

    # source: https://medium.com/@mehdirt/mastering-text-clustering-with-python-a-comprehensive-guide-f8617f53c327#evaluation-and-comparison
    data = PCA(n_components=2).fit_transform(embeddings)

    plt.figure(figsize=(5,3))
    plt.scatter(data[:,0], data[:,1], c=labels, cmap='viridis', s=5)
    plt.title('K-Means Clustering Results')
    plt.show()