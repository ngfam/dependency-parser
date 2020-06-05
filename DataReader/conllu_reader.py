from conllu import parse_incr

class Reader():
    def __init__(self, path):
        self.data_file = open(path, "r", encoding="utf-8")
    
    def sentenceReader(self):
        for tokenList in parse_incr(self.data_file):
            yield tokenList