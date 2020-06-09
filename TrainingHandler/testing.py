import math
from DataReader.conllu_reader import Reader
from TrainingHandler.extractor import extractor
from sklearn.preprocessing import MinMaxScaler

read = Reader('Data/dev.conllu')

def sentences():
    for x in read.sentenceReader():
        sentence = []
        flag = True
        for y in x:
            sentence.append((y["id"], y["lemma"].lower(), y["xpos"], y["head"]))
            if type(y["id"]) is not int:
                flag = False
        if flag == False:
            continue

        yield sentence
        # return [sentence]

SHIFT = 0 
RIGHT = 1
LEFT = 2

class Parse:
    def __init__(self, n):
        self.n = n
        self.heads = [None] * (n + 1)
        self.left = []
        self.right = []
        for i in range(n + 1):
            self.left.append(list())
            self.right.append(list())
        
    
    def add_deps(self, head, child):
        self.heads[child] = head
        if child < head:
            self.left[head].append(child)
        else:
            self.right[head].append(child)

class Testing:
    def __init__(self, ngram, weights):
        self.ngram = ngram
        self.weights = weights
        self.correct = 0
        self.total = 0
        self.allCorrect = 0
        self.countSentence = 0

        print(self.weights)

    def trainsition(self, move, idx, stack, deps, rid, heads):
        if move == RIGHT:
            if len(stack) < 2:
                return -1
            heads[stack[-1]] = stack[-2]
            deps.add_deps(stack[-2], stack.pop())
            return idx
        elif move == LEFT:
            heads[stack[-1]] = rid
            deps.add_deps(rid, stack.pop()) 
            return idx
        else:
            stack.append(rid)
            return idx + 1
    
    def getFeatureScore(self, features):
        scores = [0] * 3
        for x in features:
            cur = self.ngram.queryTuple(x[1])
            # print(x, "->", cur)
        
            for i in range(3):
                if cur[i] > 0:
                    scores[i] += math.log2(cur[i]) * self.weights[x[0]]

        return scores

    def getValidMove(self, n, idx, stack):
        moves = []
        if idx < n:
            moves.append(SHIFT)
        if len(stack) > 1:
            moves.append(RIGHT)
        if idx < n and len(stack) > 1:
            moves.append(LEFT)
        return moves

    def sentenceTester(self, ids, words, tags, heads):
        n = len(words)
        stack = [0]
        deps = Parse(n)
        idx = 0
        result = [-1] * (n + 1)


        while idx < n or len(stack) > 1:
            features = extractor(idx, words, tags, deps, stack)

            ## identify valid moves
            moves = self.getValidMove(n, idx, stack)
            scores = self.getFeatureScore(features)

            if len(moves) == 0:
                break

            bestMove = max(moves, key = lambda k : scores[k])
            idx = self.trainsition(bestMove, idx, stack, deps, None if idx == n else ids[idx], result)            
            if idx == -1:
                idx += 1
        
        all = 0
        for i in range(n):
            if heads[i] == result[i + 1]:
                self.correct += 1
            else:
                all += 1
            self.total += 1
        if all < 3:
            self.allCorrect += 1
        self.countSentence += 1


    def process(self):
        # sentences get
        for s in sentences():
            ids = []
            words = []
            tags = []
            heads = []
            flag = True
            for w in s:
                if (w is not None) and (w[0] is not None) and (w[1] is not None) and (w[2] is not None):
                    ids.append(w[0])
                    words.append(w[1])
                    tags.append(w[2])
                    if w[3] is not None:
                        heads.append(w[3])
                    else: 
                        heads.append(0)  
                else:
                    flag = False
                    print(w, w[0], w[1], w[2], w[3])

            if flag == True:
                self.sentenceTester(ids, words, tags, heads)