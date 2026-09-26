# source: https://radimrehurek.com/gensim_3.8.3/models/doc2vec.html

from preprocessing import ng_train
from numpy._core.fromnumeric import cumulative_prod
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

# tagging documents
tagged_ng_train = [
    TaggedDocument(
        words=word_tokenize(doc.lower()),
        tags=[str(i)]
    )
    for i, doc in enumerate(ng_train.data)
]
                
d2v_model = Doc2Vec(
    vector_size=100,
    #min_count=5, default is 5
    epochs=50,
    alpha=0.05,
    dm=0 # bag of words for now, but might change to distributed memory
)

d2v_model.build_vocab(tagged_ng_train)
d2v_model.train(
    tagged_ng_train,
    total_examples=d2v_model.corpus_count,
    epochs=d2v_model.epochs
)

embeddings = [
    d2v_model.infer_vector(word_tokenize(doc.lower()))
    for doc in ng_train.data
]
