class Ngram:
    def __init__(self):
        self.wordCount = dict()

    def trans(self, tup):
        word = tup[0]
        for i in range(1, len(tup)):
            word += '$' + tup[i]
        return word
    
    def addTuple(self, tup, act):
        self.addWord(self.trans(tup), act)
    
    def queryTuple(self, tup):
        return self.queryWord(self.trans(tup))

    def addWord(self, word, act):
        if word not in self.wordCount:
            self.wordCount[word] = [0] * 3

        self.wordCount[word][act] += 1

    def queryWord(self, word):
        if word not in self.wordCount:
            return [0] * 3
        return self.wordCount[word]
