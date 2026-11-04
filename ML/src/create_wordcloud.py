from wordcloud import WordCloud

def generate_wordcloud(label, keywords): # label determines which cluster and keywords is a dict
    weights = {
        keyword: 1/max(score, 1e-10)
        for keyword, score in keywords[label]
    }

    wordcloud = WordCloud(width=800, height=400,
                      background_color='black', colormap='BuPu').generate_from_frequencies(weights)

    return wordcloud