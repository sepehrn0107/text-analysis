import nltk
from nltk.probability import FreqDist
from nltk.corpus import brown as brown

def getAllWordsKTimesNFirst(k,n):
    tekst = [word.lower() for word in brown.words()]
    fdist1 = FreqDist(tekst[:n])
    most_common = fdist1.most_common()
    most_common_atleast_k = [x for x in most_common if x[1]>=k]
    return list(map(lambda x:x[0],most_common_atleast_k))
    
    

def main():
    getAllWordsKTimesNFirst(5,200)

main()
