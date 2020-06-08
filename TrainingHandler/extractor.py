# ugliest thing ever

def extractor(idx, words, tags, parse, stack):
    # keep in mind that we are working with STRING INDEXES instead of VERTICE INDEXES in this function

    def t(x):
        if x == None or x == -1: 
            return ''
        return tags[x]
    
    def d(x):
        if x == None or x == -1:
            return ''
        return words[x]

    def getLastElem(lst, id):
        if len(lst) < id:
            return None
        return lst[-id] - 1
    
    def getLeftSize(x):
        if x == None or x == -1:
            return "0"
        return str(len(parse.left[x]))
    
    def getRightSize(x):
        if x == None or x == -1:
            return "0"
        return str(len(parse.right[x]))
        

    # all the below values will be ints of the indexes of the positions
    ## top elements in stack
    s0 = None if len(stack) < 1 else stack[-1] - 1
    s1 = None if len(stack) < 2 else stack[-2] - 1
    s2 = None if len(stack) < 3 else stack[-3] - 1

    ## top elements in buffer
    w0 = None if idx >= len(words) else idx
    w1 = None if idx + 1 >= len(words) else idx + 1
    w2 = None if idx + 2 >= len(words) else idx + 2

    # get children of s0 and w0
    s0l1 = None if s0 == None else getLastElem(parse.left[s0 + 1], 1)
    s0l2 = None if s0 == None else getLastElem(parse.left[s0 + 1], 2)

    s0r1 = None if s0 == None else getLastElem(parse.right[s0 + 1], 1)
    s0r2 = None if s0 == None else getLastElem(parse.right[s0 + 1], 2)

    w0l1 = None if w0 == None else getLastElem(parse.left[w0 + 1], 1)
    w0l2 = None if w0 == None else getLastElem(parse.left[w0 + 1], 2)

    # SHOW TIME


    Dn0s0 = min(5, w0 - s0) if s0 != 0 and w0 != None else 0
    features = []

    # unigram
    for i, w in enumerate((w0, w1, w2, s0, s1, s2, s0l1, s0l2, s0r1, s0r2, w0l1, w0l2)):
        if w is not None and len(d(w)) > 1:
            features.append((d(w), str(i)))
    
    ## (word, tag) pairs
    for i, w in enumerate((w0, w1, w2, s0)):
        if w is not None:
            features.append((str(i) + '>' + d(w) + '>' + t(w), ))
            features.append((str(i) + '>' + d(w) + '>' + t(w), ))
            features.append((str(i) + '>' + d(w) + '>' + t(w), ))
            features.append((str(i) + '>' + d(w) + '>' + t(w), ))
            features.append((str(i) + '>' + d(w) + '>' + t(w), ))
            features.append((str(i) + '>' + d(w) + '>' + t(w), ))

    ## bigrams

    features.append((d(w0), d(w1)))
    features.append((d(w0) + t(w0), d(s0)))
    features.append((d(w0) + t(w0), t(s0)))
    features.append((d(s0) + t(s0), d(w0)))
    features.append((d(s0) + t(s0), t(w0)))
    features.append((d(s0) + t(s0), d(w0) + t(w0)))
    features.append((t(s0), t(w0)))
    features.append((t(w0), t(w1)))

    features.append((d(w0), d(w1)))
    features.append((d(w0) + t(w0), d(s0)))
    features.append((d(w0) + t(w0), t(s0)))
    features.append((d(s0) + t(s0), d(w0)))
    features.append((d(s0) + t(s0), t(w0)))
    features.append((d(s0) + t(s0), d(w0) + t(w0)))
    features.append((t(s0), t(w0)))
    features.append((t(w0), t(w1)))

    features.append((d(w0), d(w1)))
    features.append((d(w0) + t(w0), d(s0)))
    features.append((d(w0) + t(w0), t(s0)))
    features.append((d(s0) + t(s0), d(w0)))
    features.append((d(s0) + t(s0), t(w0)))
    features.append((d(s0) + t(s0), d(w0) + t(w0)))
    features.append((t(s0), t(w0)))
    features.append((t(w0), t(w1)))

    # trigrams
    trigrams = ((t(w0), t(w1), t(w2)), (t(s0), t(w0), t(w1)), (t(s0), t(s1), t(w0)), 
                (t(s0), t(s0r1), t(w0)), (t(s0), t(s0r2), t(w0)), (t(s0), t(w0), t(w0l1)),
                (t(s0), t(s0l1), t(s0l2)), (t(s0), t(s0r1), t(s0r2)), (t(w0), t(w0l1), t(w0l2)),
                (t(s0), t(s1), t(s2)))
    
    for i, (t1, t2, t3) in enumerate(trigrams):
        ## enumerate is for distinguishing between trigrams
        if len(t1) > 0 and len(t2) > 0:
            features.append((str(i) + '-' + t1, t2, t3))
    
    for i, (t1, t2, t3) in enumerate(trigrams):
        ## enumerate is for distinguishing between trigrams
        if len(t1) > 0 and len(t2) > 0:
            features.append((str(i) + '-' + t1, t2, t3))
            features.append((str(i) + '-' + t1, t2, t3))

    sl = getLeftSize(s0 + 1)
    sr = getRightSize(s0 + 1)
    wl = getLeftSize(w0)

    sw = ((sl, d(s0)), (sr, d(s0)), (wl, d(w0)))
    st = ((sl, t(s0)), (sr, t(s0)), (wl, t(w0)))
    Dn0s0 = str(Dn0s0)

    # distances
    ds = ((Dn0s0, d(s0)), (Dn0s0, t(s0)), (Dn0s0, d(w0)), (Dn0s0, t(w0)),
        (Dn0s0, d(s0) + d(w0)), (Dn0s0, t(s0) + t(w0)))

    # for i, (x, y) in enumerate(sw + st + ds):
    #     if x and y and len(y) > 0 and i != 4 and i != 7:
    #         features.append((str(i) + '-' + x, y))

    return features