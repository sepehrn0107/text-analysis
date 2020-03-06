import nltk
from nltk.corpus import wordnet
from nltk.corpus import movie_reviews as mr
from nltk.probability import FreqDist
import random



all_words = FreqDist(w.lower() for w in mr.words())
word_features = list(all_words)[:2000]
documents = [(list(mr.words(fileid)), category)
    for category in mr.categories()
    for fileid in mr.fileids(category)]
random.shuffle(documents)


# Found in Piazza. could not figure out how to do it on our own. similar on NLTK chaper 6
def lexicon_features(reviews):
    review_words = set(reviews)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in review_words)
        for synset in wordnet.synsets(word):
            for name in synset.lemma_names():
                features['synset({})'.format(word)] = (name in review_words)
    return features


# print("Wait.")
# featuresets = [(lexicon_features(d), c) for (d, c) in documents]
# print(len(featuresets))
# print("Wait..")
# train_set, test_set = featuresets[500:], featuresets[:500]
# print("Wait...")
# classifier = nltk.NaiveBayesClassifier.train(train_set)
# print("Wait....")
# print("Naive Bayes: ", nltk.classify.accuracy(classifier, test_set))




