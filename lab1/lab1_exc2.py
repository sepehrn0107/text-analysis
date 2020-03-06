from nltk.book import text9 as txt
from nltk.corpus import webtext
from nltk.tokenize import sent_tokenize, word_tokenize
wordIndex = []
wordArray = []
txt2 = txt

def iterativeSearch(newIndex, word):
    try:
        txt2 = txt[newIndex:]
        hhIndex = txt2.index(word)
        wordIndex.append(newIndex+hhIndex)
        iterativeSearch(hhIndex + newIndex+1,word)
    except ValueError:
        return
def searchWord(word):
    iterativeSearch(0,word)
    print(wordIndex)
    for index in wordIndex:
        wordArray.append(conjureSent(index))
def conjureSent(index):
    startStringIndex = index
    srcForward = 0
    srcBackward = 0
    targetText = ""
    while targetText != ".":
        srcForward += 1
        targetText = txt[startStringIndex+srcForward]
    targetText = ""
    while (targetText != "."):
        srcBackward -= 1
        targetText = txt[startStringIndex+srcBackward]
    returnString = ""
    for i in range(srcBackward+1,srcForward):
        returnString = returnString+" "+ txt[startStringIndex+i+1]
    return returnString
    
if __name__ == "__main__":
    searchWord("sunset")
    wordArray = list(set(wordArray))
    for sen in wordArray:
        print(sen)