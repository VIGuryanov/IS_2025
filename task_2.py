import os
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
nltk.download('stopwords')

rus_stopwords = stopwords.words("russian")
stemmer = SnowballStemmer("russian")

for file in os.listdir('web_pages'):
    with open(f"web_pages/{file}", "r", encoding='utf-8') as page:
        tokens = page.read().split()

    lemmas = []
    for token in tokens:
        if token not in rus_stopwords:
            lemmas.append(stemmer.stem(token))
                
    with open(f"tokens/{file}", "w", encoding='utf-8') as tokens_file:
        tokens_file.write(' '.join(lemmas))