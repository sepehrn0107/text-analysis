import nltk
import random
import re
import json

data =  ""

def loadJson(filename):
    with open(filename) as json_file:
        data = ""
        data2 = json.load(json_file)
        for item in data2:
            data+=item['text'].replace("\n","")
    return data

tweetData = loadJson("donald.json")

tweetData = data.lower()

#cleans up the output. 
tweetData = re.sub('[^A-Za-z. ]', '', tweetData)
tweetData = re.sub('(httpst.)(\w*)','',tweetData)

n_3_grams = {}
words = 3

words_tokens = nltk.word_tokenize(tweetData)
for i in range(len(words_tokens)-words):
    seq = ' '.join(words_tokens[i:i+words])
    if  seq not in n_3_grams.keys():
        n_3_grams[seq] = []
    n_3_grams[seq].append(words_tokens[i+words])

def predictNextNWords(input,maxLength):
    current = input
    result = current
    for i in range(maxLength):
        possible_words = n_3_grams[current]
        next_word = random.choice(possible_words)
        result += ' ' + next_word
        seq_words = nltk.word_tokenize(result)
        current = ' '.join(seq_words[len(seq_words)-words:len(seq_words)])
    return result

print(predictNextNWords("there will be",50))
