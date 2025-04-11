import os
import pandas as pd
import numpy as np
import json

files = os.listdir('tokens')
files = list(map(lambda x: int(x.split('.')[0]), files))
files.sort()

with open('rev_index.txt', 'r', encoding='utf-8') as f:
    rev_index = json.load(f)

with open('index.txt', 'r', encoding='utf-8') as f:
    index = f.read()
    index = index.split('\n')

tf_matrix = np.zeros((len(rev_index), len(index)))
terms = [term for term in rev_index]
# for i, term in enumerate(terms):
#     tf_matrix[i][0] = term

docs = []
for file in files:
    with open(f"tokens/{file}.txt", "r", encoding='utf-8') as page:
        docs.append(page.read().split())

for i, term in enumerate(rev_index):
    for occ in rev_index[term]:
        tf_matrix[i][occ-1] = round(docs[occ-1].count(term) / len(docs[occ-1]), 5)

df = pd.DataFrame(tf_matrix, columns=files)
df.insert(0, 'term', terms)
df.to_csv('tf_matrix.csv')

idf_vector = np.zeros((len(rev_index)))
for i, term in enumerate(rev_index):
    idf_vector[i] = round(np.log2(len(files) / len(rev_index[term])), 5)

df = pd.DataFrame(idf_vector)
df.insert(0, 'term', terms)
df.to_csv('idf_matrix.csv')

tf_idf_matrix = np.round(np.matmul(np.diag(idf_vector), tf_matrix), 5)
df = pd.DataFrame(tf_idf_matrix, columns=files)
df.insert(0, 'term', terms)
df.to_csv('tf_idf_matrix.csv')