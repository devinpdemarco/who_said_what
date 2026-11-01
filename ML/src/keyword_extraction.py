import yake

def extract_keywords(labels, valid_labels, data):
    # source: https://medium.com/@linz07m/yake-simple-and-smart-keyword-extraction-16089f235d64
    cluster_texts = {}
    for label in valid_labels:
        docs=[]
        for i, doc in enumerate(data):
            if label == labels[i]:
                docs.append(doc)
        cluster = '\n'.join(docs)
        cluster_texts[label] = cluster

    keyword_extractor = yake.KeywordExtractor(top=10)
    cluster_keywords = {}

    for id, cluster in cluster_texts.items():

        keywords = keyword_extractor.extract_keywords(cluster)
        cluster_keywords[id] = keywords

    return cluster_keywords