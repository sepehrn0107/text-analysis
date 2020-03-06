import nltk 
from nltk.corpus import brown as brown
from nltk import FreqDist

brown_tagged = brown.tagged_words()
def findMostFrequent(): 
    frequent = nltk.FreqDist(tag for (word, tag) in brown_tagged)
    return frequent.most_common(1)
   


def findAmountAmbiguous():
    count = 0
    frequent = nltk.ConditionalFreqDist((word.lower(), tag) for (word, tag) in brown_tagged)
    for word in sorted(frequent.conditions()):
        if len(frequent[word]) >= 2:
            tags = [tag for (tag, _) in frequent[word].most_common()]
            count += 1
    return count

def findAmbiguousPercent():
    brown_words = brown.words()
    am = findMostAmbiguous()
    return (am/len(brown_words) *100)

def findMostTaggedWord():
    frequent = nltk.ConditionalFreqDist((word.lower(),tag) for(word,tag) in brown_tagged)
    tagged = {}
    for word in sorted(frequent.conditions()):
        tags = [tag for (tag, _) in frequent[word].most_common()]
        tagged[word] = tags
    mostTagged = sorted(tagged,key = lambda key: len(tagged[key]))
    dictOfWords = {item: tagged[item] for item in mostTagged[-10:]}    
    return dictOfWords


def findPercentageAmbigiousBrown():
    brown_words = brown.words()
    print(100*findAmountAmbigious()/len(brown_words),"%")



x = 2