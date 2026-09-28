
from sentence_transformers import SentenceTransformer

def create_embeddings(data):
    # source: https://medium.com/@dingusagar/text-clustering-using-sentence-embeddings-abcb6048fc36
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(data)

    return embeddings
