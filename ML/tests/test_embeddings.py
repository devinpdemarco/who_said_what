
# source: https://medium.com/@mehdirt/mastering-text-clustering-with-python-a-comprehensive-guide-f8617f53c327#evaluation-and-comparison
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from src import preprocessing as p
from src import embeddings as e

def plot_clusters(data, labels, title):
    plt.figure(figsize=(5,3))
    plt.scatter(data[:,0], data[:,1], c=labels, cmap='viridis', s=5)
    plt.title(title)
    plt.colorbar()
    plt.show()

data_pca = PCA(n_components=2).fit_transform(e.embeddings)
plot_clusters(data_pca, p.ng_train.target, f'Topic Distribution Analysis')