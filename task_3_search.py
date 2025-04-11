import json
from nltk.stem.snowball import SnowballStemmer

class logicFunction:
    _doc_count = sum(1 for _ in open('index.txt', 'r', encoding='utf-8'))

    def search(self, index:dict):
        pass

class AND(logicFunction):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def search(self, index:dict) -> set:
        if isinstance(self.left, logicFunction):
            left = self.left.search(index)
        elif self.left in index:
            left = set(index[self.left])
        else:
            return set()

        if isinstance(self.right, logicFunction):
            right = self.right.search(index)
        elif self.right in index:
            right = set(index[self.right])
        else:
            return set()

        return left.intersection(right)

class OR(logicFunction):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def search(self, index:dict):
        if isinstance(self.left, logicFunction):
            left = self.left.search(index)
        elif self.left in index:
            left = set(index[self.left])
        else:
            left =  set()

        if isinstance(self.right, logicFunction):
            right = self.right.search(index)
        elif self.right in index:
            right = set(index[self.right])
        else:
            right = set()
            
        return left.union(right)

class NOT(logicFunction):
    def __init__(self, element):
        self.element = element

    def search(self, index:dict):
        if isinstance(self.element, logicFunction):
            el = self.element.search(index)
        elif self.element in index:
            el = set(index[self.element])
        else:
            el = set()

        return set(range(1, logicFunction._doc_count + 1)).difference(el)

class boolParser:
    lemma = SnowballStemmer("russian")

    def parse(req:str) -> logicFunction:
        req.replace(' ИЛИ ', '|')
        req = req.split('|', 1)
        if len(req) > 1:
            return OR(boolParser.parse(req[0].strip()), boolParser.parse(req[1].strip()))
        
        req = req[0]
        req.replace(' И ', '&')
        req = req.split('&', 1)
        if len(req) > 1:
            return AND(boolParser.parse(req[0].strip()), boolParser.parse(req[1].strip()))
        
        req = req[0]
        req.replace('НЕ', '!')
        req = req.strip()
        if req[0] == '!':
            return NOT(boolParser.parse(req[1:].strip()))          
                
        return boolParser.lemma.stem(req)
        

with open('rev_index.txt', 'r', encoding='utf-8') as f:
    rev_index = json.load(f)

res = boolParser.parse(input("Введите булево выражение: ")).search(rev_index)
with open('index.txt', 'r', encoding='utf-8') as f:
    index = f.read()
    index = index.split('\n')
    for r in res:
        print(index[r-1].split(' ', 1)[1])