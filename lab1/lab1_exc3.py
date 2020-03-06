import tweepy
import json
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.twitter import Twitter


consumer_key = "zkQZ4djk5UP7wVXseob8jJ6Vm"
consumer_secret = "umeeVPom6lC32sCthGcu8k1lsbAdEVKxUaHp2KtDUxb5VZAcnb"

access_token = "2255553137-uGEGeqc9lqYUQaYBwmzh4fJQHcGVbLDlH0d7FPF"
access_token_secret = "4f7PNLX4Hsnxcugc5BZLpVh4qfajWhHRV9Pt2MHFMc9UO"


def tweetApiCall():
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth,parser=tweepy.parsers.JSONParser())
    tweets2 = api.search(["Run"],count=100)
    api2 = tweepy.API(auth)
    tweets = tweets2



def makeTxt(filename):
    with open(filename,"w") as file:
        for tweet in tweets:
            file.write(tweet.text)

def makeJson(filename):
    with open(filename,"w") as json_file:
        print(type(tweets2))
        json.dump(tweets2,json_file)

def loadJson(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data




def getAllUniqueHashtags(dicto):
    uniques = {} 
    for i in range(len(dicto["statuses"])):
        for j in range(len(dicto["statuses"][i]["entities"]["hashtags"])):
            if not dicto["statuses"][i]["entities"]["hashtags"][j]["text"] in uniques:
                uniques[dicto["statuses"][i]["entities"]["hashtags"][j]["text"]] = 1
            else:
                uniques[dicto["statuses"][i]["entities"]["hashtags"][j]["text"]] +=1
    return uniques



def getFromTxt():
    stringen = getData("data.txt")
    tokens = tokenize(stringen)
    filtered_sentence = removeStopWords(tokens)
    print(getNMostCommon(filtered_sentence,5))


def getData(filename):
    with open(filename) as readfile:
        stringen = readfile.read()
    return stringen
    

def tokenize(stringen):
    word_tokens = nltk.word_tokenize(stringen)
    word_tokens = [word.lower() for word in word_tokens if word.isalpha()]
    return word_tokens

def removeStopWords(word_tokens):
    stop_words = set(stopwords.words("english"))
    extra = [":",",",":","https",".","@","!","#","´",";"]
    for item in extra:
        stop_words.add(item)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return filtered_sentence

def getNMostCommon(filtered_sentence,n):
    fdist1 = FreqDist(filtered_sentence)
    return fdist1.most_common(n)

def getNMostCommonFiltered(word_tokens,n):
    return getNMostCommon(removeStopWords(word_tokens),n)

def getNMostCommonHashtags(n,dicto):
    dk = {}
    for i in range(n):
        biggest = max(dicto,key=dicto.get)
        print(biggest)
        dk[biggest] = dicto[biggest]
        del dicto[biggest]
    return dk

def main():
    x = 5

main()
