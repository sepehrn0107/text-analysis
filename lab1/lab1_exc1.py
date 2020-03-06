#!/usr/bin/env python3

import nltk
from collections import Counter

MALE = 'male'
FEMALE = 'female'
UNKNOWN = 'unknown'
BOTH = 'both'

MALE_WORDS = set([
    'guy','spokesman','chairman',"men's",'men','him',"he's",'his',
    'boy','boyfriend','boyfriends','boys','brother','brothers','dad',
    'dads','dude','father','fathers','fiance','gentleman','gentlemen',
    'god','grandfather','grandpa','grandson','groom','he','himself',
    'husband','husbands','king','male','man','mr','nephew','nephews',
    'priest','prince','son','sons','uncle','uncles','waiter','widower',
    'widowers'
]) #set with words assosiated with male

FEMALE_WORDS = set([
    'heroine','spokeswoman','chairwoman',"women's",'actress','women',
    "she's",'her','aunt','aunts','bride','daughter','daughters','female',
    'fiancee','girl','girlfriend','girlfriends','girls','goddess',
    'granddaughter','grandma','grandmother','herself','ladies','lady',
    'lady','mom','moms','mother','mothers','mrs','ms','niece','nieces',
    'priestess','princess','queens','she','sister','sisters','waitress',
    'widow','widows','wife','wives','woman'
]) # set with words assosiated woth female


def genderize(words):

    mwlen = len(MALE_WORDS.intersection(words))
    fwlen = len(FEMALE_WORDS.intersection(words))
    # returns the string MALE if all the words is intersected with the male set
    if mwlen > 0 and fwlen == 0:
        return MALE
    # returns the string FEMALE if the words is intersected with the female set
    elif mwlen == 0 and fwlen > 0:
        return FEMALE
    # returns the string BOTH if the words is intersected with both the male set and the female set
    elif mwlen > 0 and fwlen > 0:
        return BOTH
    # if there is no intersection with either of the sets, return UNKNOWN
    else:
        return UNKNOWN

# counts the number of genderized sentenses and the amount of words in a sentence
# returns the length of the sentences which are genderized
def count_gender(sentences):

    sents = Counter()
    words = Counter()

    for sentence in sentences:
        gender = genderize(sentence)
        sents[gender] += 1
        words[gender] += len(sentence)

    return sents, words


def parse_gender(text):
    #splits the text into tokens of words with lower case for each sentence
    sentences = [
        [word.lower() for word in nltk.word_tokenize(sentence)]
        for sentence in nltk.sent_tokenize(text)
    ]

    sents, words = count_gender(sentences)
    total = sum(words.values())
    # prints percentage of genderized words, amount of sentences and percentile on how many sentences that are genderized
    for gender, count in words.items():
        pcent = (count / total) * 100
        nsents = sents[gender]        
        print(
            "{:0.3f}% {} ({} sentences)".format(pcent, gender, nsents)
        )

if __name__ == '__main__':
    with open('sample.txt', 'r') as f:
        parse_gender(f.read())
