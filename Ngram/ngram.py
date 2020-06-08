class Ngram:
    def __init__(self):
        self.wordCount = dict()

    def trans(self, tup):
        word = tup[0]
        for i in range(1, len(tup)):
            word += '$' + tup[i]
        return word
    
    def addTuple(self, tup, act):
        totalLength = 0
        for x in tup:
            totalLength += len(x)
        if totalLength == 0:
            return

        # if len(tup) == 2 and tup[0] == '' and tup[1] == '':
        #     print("YES?")
        self.addWord(self.trans(tup), act)
    
    def queryTuple(self, tup):
        return self.queryWord(self.trans(tup))

    def addWord(self, word, act):
        if word not in self.wordCount:
            self.wordCount[word] = [2] * 3

        if act != 0:
            if act == 2:
                self.wordCount[word][act] += 4
            else:
                self.wordCount[word][act] += 2.8
        else:
            self.wordCount[word][act] += 2

    def queryWord(self, word):
        if word not in self.wordCount:
            return [2] * 3
        return self.wordCount[word]
