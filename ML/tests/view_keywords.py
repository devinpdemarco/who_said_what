from src import keyword_extraction as ke

# testing keywords
for kw, score in ke.keywords:
    print(f'{kw}:{score}')