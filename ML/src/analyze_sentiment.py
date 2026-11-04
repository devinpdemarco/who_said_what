# source: https://huggingface.co/sztal/erc-newsuse-valence

# load model
from transformers import AutoModel, AutoTokenizer, pipeline

def predict_sentiment(text):
    LABELS = {
        -1 : 'negative',
        0 : 'neutral',
        1 : 'positive'
    }

    model_name = 'sztal/erc-newsuse-valence'

    # downloads pretrained model
    model = AutoModel.from_pretrained(
        model_name,
        trust_remote_code=True
    )

    # loads tokenizer the model expects
    tokenizer = AutoTokenizer.from_pretrained(
        model.config.base_name_or_path
    )

    # wraps the model and tokenizer into a reusable inference interface
    classifier = pipeline(
        'text-multi-classification',
        model=model,
        tokenizer=tokenizer
    )

    result = classifier(text, truncation=True, max_length=512)
    prediction = result['sentiment']

    return {
        'label' : LABELS[prediction['label']],
        'confidence' : float(prediction['score'])
    }

def run_sentiment_analysis(articles):
    sentiment_results = []

    for article in articles:
        article_id = article['id']
        text = article['cleaned_text']

        sentiment_analysis = predict_sentiment(text)
        label = sentiment_analysis['label']
        confidence = sentiment_analysis['confidence']
        sentiment_results.append(
            {
                'article_id' : article_id,
                'sentiment_scoring': {
                    'label' : label,
                    'confidence' : confidence
                }
            }
        )

    return sentiment_results
