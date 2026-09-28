from sklearn.datasets import fetch_20newsgroups
from preprocessing import preprocess_data
from embeddings import create_embeddings
from clustering import create_clusters
from keyword_extraction import extract_keywords


# data import
# importing sample categories from train data
sample_categories = ['soc.religion.christian', 'sci.space', 'sci.med', 'sci.electronics', 'rec.sport.baseball']
# only doing one category for now to ensure that the clusters make sense
ng_train = fetch_20newsgroups(subset='train',
                            categories=sample_categories[:3],
                            remove=('headers', 'footers', 'quotes'),
                            random_state=42
                            )

# preprocessing data
data = preprocess_data(ng_train.data)

# create sentence transformer embeddings
embeddings = create_embeddings(ng_train.data)

# create clusters using k-means
# will determine a better algorithm to determine how to decide preset number of clusters
# using three for now to work with the mock data
labels, km = create_clusters(embeddings, 3)

# performing the keyword extraction using yake
clustered_keywords = extract_keywords(labels, ng_train.data)

# display top 5 keywords in each cluster
# lower numbers indicate higher importance/frequency of keywords in text
for i, cluster in enumerate(clustered_keywords):
    count=0
    print(f'Cluster {i}')
    for kw, score in cluster:
        count+=1
        print(f'{kw}:{score}')
        if count >= 5:
            break