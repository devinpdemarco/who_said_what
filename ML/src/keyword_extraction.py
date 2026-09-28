import yake

def extract_keywords(labels, data):
    # source: https://medium.com/@linz07m/yake-simple-and-smart-keyword-extraction-16089f235d64
    cluster_texts = []
    for label in set(labels):
        cluster=''
        for i, doc in enumerate(data):
            if label == labels[i]:
                cluster += doc
        
        cluster_texts.append(cluster)


    keyword_extractor = yake.KeywordExtractor()
    cluster_keywords = []

    for cluster in cluster_texts:
        cluster_keywords.append(keyword_extractor.extract_keywords(cluster))

    return cluster_keywords
