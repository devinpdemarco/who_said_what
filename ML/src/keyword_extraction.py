import yake
from preprocessing import ng_train

# this will be different once i do it over the clusters
# the clustering is not functioning correctly yet
# but the keyword extraction will make way more sense once they do
text = ''

keyword_extractor = yake.KeywordExtractor()
for doc in ng_train.data:
    text += doc

keywords = keyword_extractor.extract_keywords(text)
