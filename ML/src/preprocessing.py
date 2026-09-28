import nltk
from nltk.corpus import stopwords
#nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

def preprocess_data(data):

    # data preprocessing
    # basic cleaning of document text and removal of basic punctuation
    # source: https://medium.com/@danielafrimi/text-clustering-using-nlp-techniques-c2e6b08b6e95

    # remove hyperlinks
    for i, doc in enumerate(data):
        # remove hyperlinks
        data[i] = doc.replace(r'http\S+','')
        # remove special characters and numbers
        data[i] = doc.replace('[^A-Za-z]+','')
        # remove stopwords
        tokens = nltk.word_tokenize(doc)
        #tokens = [w for w in tokens if not w.lower() in stopwords.words('english')]
        data[i] = ' '.join(tokens)
        data[i] = doc.lower().strip()
    
    return data