import nltk
from nltk import FreqDist
from nltk.probability import ConditionalFreqDist
from nltk.corpus import brown as brown
from nltk.corpus import nps_chat as chat
from nltk import RegexpTagger
from nltk import UnigramTagger
from nltk import BigramTagger
from nltk import TrigramTagger

sizeB = len(brown.tagged_sents()) #length of size of brown corpus
sizeC = len(chat.tagged_posts())  #length of size of NPS corpus

brownTS = brown.tagged_sents() 
brownTW = brown.tagged_words() #partition sentences into a list with each word containing its tag

chatTP = chat.tagged_posts()#partition words into a list with each post containing its tag
chatTW = chat.tagged_words() #partition words into a list with each word containing its tag

def splitSen(c,p): #function to partition corpus
        if c == "brown":
                t1 = brownTS[:int(sizeB*p)]
                t2 = brownTS[int(sizeB*p):]
                return t1, t2
        if c == "chat":
                t1 = chatTP[:int(sizeC*p)]
                t2 = chatTP[int(sizeC*p):]
                return t1, t2


brownT50, brownT50 = splitSen("brown",0.5)
brownT90, brownT90 = splitSen("brown",0.9)

chatT50, chatT50 = splitSen("chat",0.5)
chatT90, chatT90 = splitSen("chat",0.5)

# 2
# a)
freqBrown50 = FreqDist([tag for (word, tag) in brownTW[:int(sizeB/2)]]).max()
defaultTB50 = nltk.DefaultTagger(freqBrown50)
print(defaultTB50)
#print(defaultTB50.evaluate(brownT50))

freqBrown90 = FreqDist([tag for (word, tag) in brownTW[:int(sizeB*0.9)]]).max()
defaultTB90 = nltk.DefaultTagger(freqBrown90)
#print(defaultTB90.evaluate(brownT90))

freqChat50 = FreqDist([tag for (word, tag) in chatTW[:int(sizeC/2)]]).max()
defaultTChat50 = nltk.DefaultTagger(freqChat50)
#print(defaultTChat50.evaluate(chatT50))

freqChat90 = FreqDist([tag for (word, tag) in chatTW[:int(sizeC*0.9)]]).max()
defaultTChat90 = nltk.DefaultTagger(freqChat90)
#print(defaultTChat90.evaluate(chatT90))

#b)
#using regex from nltk.org/book/chp05.html, 4.2
patterns = [
        (r'.*ing$', 'VBG'), #gerunds
        (r'.*ed$', 'VBD'), #simple past
        (r'.*es$', 'VBZ'), # 3rd singular present
        (r'.*ould$', 'MD'), #modal
        (r'.*\'s$', 'NN$'), # possessive nouns
        (r'.*s$', 'NNS'),    #plural nouns
        (r'^-?[0-9]+(\.[0-9]+)?$', 'CD'), # cardinal numbers
        (r'.*', 'NN') #nouns (default)
]
regexp_tagger = RegexpTagger(patterns)
uniB = UnigramTagger(brownT90, backoff=defaultTB90)  
biB = BigramTagger(brownT90, backoff=uniB)
triB = TrigramTagger(brownT90, backoff=biB)

uniC = UnigramTagger(chatT50, backoff = defaultTChat50)
biC = BigramTagger(chatT50, backoff = uniC)
triC = TrigramTagger(chatT50, backoff = uniC)


print("Regextag50/50: ",regexp_tagger.evaluate(brownT50))
print("Default: ", defaultTB90.evaluate(brownT50))

print("Bigram Brown 50/50: ", BigramTagger(brownT50, backoff=defaultTB50).evaluate(brownT50))
print("Default: ", defaultTB50.evaluate(brownT50))

print("Bigram Brown 90/10: ", BigramTagger(brownT90, backoff=defaultTB90).evaluate(brownT90))
print("Default: ", defaultTB90.evaluate(brownT90))

print("Unigram chat 50/50: ", UnigramTagger(chatT50, backoff=defaultTChat50).evaluate(chatT50))
print("Default: ", defaultTChat50.evaluate(chatT50))

print("Unigram chat 90/10: ", UnigramTagger(chatT90, backoff=defaultTChat90).evaluate(chatT90))
print("Default: ", defaultTChat90.evaluate(chatT90))

print("Trigram to Bigram to Unigram Brown 90/10: ", triB.evaluate(brownT50))
print("Default: ", defaultTB90.evaluate(brownT90))

print("Trigram to Bigram to Unigram with chat 50/50: ", triB.evaluate(chatT50))
print("Default: ", defaultTChat50.evaluate(chatT50))

#3
def lookupTagger(r, c): # r = range, c = corpus
        if (c =="brown"):
                fDist = ConditionalFreqDist(brownTW)
                freqDist = FreqDist(brown.words())
                wordsR = freqDist.most_common(r)
                likely_tags = dict((word, fDist[word].max()) for (word, _) in wordsR)
                baseline_tagger = UnigramTagger(model= likely_tags, backoff = nltk.DefaultTagger("NN"))
                return baseline_tagger
        if (c == "chat"):
                fDist = ConditionalFreqDist(chatTW)
                freqDist = FreqDist(chat.words())
                wordsR = freqDist.most_common(r)
                likely_tags = dict((word, fDist[word].max()) for (word, _) in wordsR)
                baseline_tagger = UnigramTagger(model= likely_tags, backoff = nltk.DefaultTagger("NN"))
                return baseline_tagger

print("Bigram Brown 50/50: ", BigramTagger(brownT50, backoff=lookupTagger(200,"brown")).evaluate(brownT50))
print("Default: ", defaultTB50.evaluate(brownT50))

print("Bigram Brown 90/10: ", BigramTagger(brownT90, backoff=lookupTagger(200,"brown")).evaluate(brownT90))
print("Default: ", defaultTB90.evaluate(brownT90))

print("Unigram chat 50/50: ", UnigramTagger(chatT50, backoff=lookupTagger(200,"chat")).evaluate(chatT50))
print("Default: ", defaultTChat50.evaluate(chatT50))

print("Unigram chat 90/10: ", UnigramTagger(chatT90, backoff=lookupTagger(200,"chat")).evaluate(chatT90))
print("Default: ", defaultTChat90.evaluate(chatT90))

print("Trigram to Bigram to Unigram Brown 90/10: ", triB.evaluate(brownT50))
print("Default: ", defaultTB90.evaluate(brownT90))

print("Trigram to Bigram to Unigram with chat 50/50: ", triB.evaluate(chatT50))
print("Default: ", defaultTChat50.evaluate(chatT50))
