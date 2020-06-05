from DataReader.conllu_reader import Reader

read = Reader('Data/train.conllu')

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
    
