from TrainingHandler.distributor import sentences
from Ngram.ngram import Ngram
from TrainingHandler.extractor import extractor

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

class Trainer:
    def __init__(self):
        self.ngram = Ngram()

    def trainsition(self, move, idx, stack, deps, rid):
        if move == RIGHT:
            if len(stack) < 2:
                return int(-1)
            deps.add_deps(stack[-2], stack.pop())
            
            return idx
        elif move == LEFT:
            deps.add_deps(rid, stack.pop()) 
            return idx
        else:
            stack.append(rid)
            return idx + 1
    
    #add features to ngram trainer
    def train(self, features, val):
        for key in features:
            self.ngram.addTuple(key, val)

    def sentenceTrainer(self, ids, words, tags, heads):
        # stack with root only
        n = len(words)
        stack = [0]
        deps = Parse(n)
        idx = 0    

        while idx < n or len(stack) > 1:
            features = extractor(idx, words, tags, deps, stack) 
            ## identify the moves
            move = -1
            if idx < n and heads[idx] > idx:
                move = SHIFT
            elif idx < n and heads[idx] == stack[-1]:
                move = SHIFT
            elif idx < n and len(stack) > 1 and heads[stack[-1] - 1] == ids[idx]:
                move = LEFT
            else:
                move = RIGHT

            ## add training materials
            self.train(features, move)
            rid = None if idx == n else ids[idx]
            idx = self.trainsition(move, idx, stack, deps, rid)
            if idx == -1:
                return

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
                self.sentenceTrainer(ids, words, tags, heads)
        
        return self.ngram
        