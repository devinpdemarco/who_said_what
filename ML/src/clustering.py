from preprocessing import ng_train
from embeddings import embeddings
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbor # may not even need this
from sklearn.metrics import silhouette_score
from sklearn.metrics import davies_bouldin_score


def run_dbscan(embeddings, eps, min_samples):
    dbs = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
    clusters = dbs.fit(embeddings)
    labels = dbs.labels_

    return dbs, clusters, labels

#finetuning
def finetune_dbscan(embeddings):
    eps = 10
    #min_noise = 2**20
    #max_clusters = 0
    max_sc = 0

    best_eps = 0.5
    best_ms = 5

    for ms in range(1,10):
        while eps > 0:
            dbscan, clusters, labels = run_dbscan(embeddings, eps, ms)
            n_clusters_found = len(set(labels)) - (1 if -1 in labels else 0)
            if (n_clusters_found <= 1) or ( n_clusters_found >= len(ng_train.data)):
                eps -= 0.05
                continue
            n_noise = list(labels).count(-1)
            # maximizing the silhouette score, but honestly may change this
            # there needs to be a better evaluation tradeoff
            sc = silhouette_score(embeddings, labels)
            if sc > max_sc:
                best_eps = eps
                best_ms = ms
                max_sc = sc

            eps -= 0.05

    return best_eps, best_ms

epsilon, min_samples = finetune_dbscan(embeddings)
dbscan, clusters, labels = run_dbscan(embeddings, epsilon, min_samples)

n_clusters_found = len(set(labels)) - (1 if -1 in labels else 0)
n_noise = list(labels).count(-1)


# measures how similar a data point is to its own cluster compared to other clusters
# a score near 1 denotes the best meaning that the data point is very compact within its cluster
# the worst value is -1 and near 0 denotes overlapping clusters
sil_score = silhouette_score(embeddings, labels)

# considers intra-cluster compactness and inter-cluster separation
db_score = davies_bouldin_score(embeddings, labels)
