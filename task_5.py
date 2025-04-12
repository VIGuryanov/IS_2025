from operator import itemgetter
from numpy import dot
from numpy.linalg import norm
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
nltk.download('stopwords')

rus_stopwords = stopwords.words("russian")
stemmer = SnowballStemmer("russian")

req = input('Write query: ')
query = list(map(lambda token: stemmer.stem(token), filter(lambda token: token not in rus_stopwords, req.split())))

tf_idf = pd.read_csv('tf_idf_matrix.csv')
idf = pd.read_csv('idf_matrix.csv')
query_filtered = list(filter(lambda token: len(tf_idf.loc[tf_idf['term'] == token].values) > 0, query))

query_vector = np.zeros(len(tf_idf))
for i in range(0, len(tf_idf)):
    if tf_idf.iloc[i]['term'] in query_filtered:
        query_vector[i] = query_filtered.count(tf_idf.iloc[i]['term']) / len(query_filtered) * idf.iloc[i][0]

tf_idf.drop('term', axis=1)
tf_idf_matrix = np.array(list(map(lambda x: x[2:], tf_idf.values)), dtype = 'float').T

cos_sim = dot(tf_idf_matrix, query_vector)/(norm(tf_idf_matrix, axis=1)*norm(query_vector))
with open('index.txt', 'r', encoding='utf-8') as index:
    index = list(map(lambda x: x.split(' ')[1], index.read().split('\n')))
res = sorted(list(zip(cos_sim, index)), key=itemgetter(0), reverse=True)

for i in range(0,10):
    print(res[i])
