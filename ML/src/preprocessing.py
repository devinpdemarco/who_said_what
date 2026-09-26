from sklearn.datasets import fetch_20newsgroups
import numpy as np

# data import
# importing sample categories from train data
sample_categories = ['soc.religion.christian', 'sci.space', 'sci.med', 'sci.electronics', 'rec.sport.baseball']
# only doing one category for now to ensure that the clusters make sense
ng_train = fetch_20newsgroups(subset='train',
                              categories=sample_categories[:3],
                              remove=('headers', 'footers', 'quotes'),
                              random_state=42
                              )

# data preprocessing
# basic cleaning of document text and removal of basic punctuation
punctuation = '\n.,;/\\()?-!'

for p in punctuation:
    for i in range(len(ng_train.data)):
        ng_train.data[i] = ng_train.data[i].replace(p, '')
        ng_train.data[i] = ng_train.data[i].lower()

