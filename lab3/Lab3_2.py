import random
import nltk
from nltk.classify import (DecisionTreeClassifier, MaxentClassifier,
                           NaiveBayesClassifier, accuracy, apply_features)
from nltk.corpus import names
from nltk.probability import ConditionalFreqDist


#Code from NLTK Chapter 6, 1.1
raw_data_names = ( [(name, 'male') for name in names.words('male.txt')] +
                  [(name, 'female') for name in names.words('female.txt')] )

random.shuffle(raw_data_names)


def genderFeatures(word):
    return {
            'last_letter': word[-1],
            'fisrt_letter': word[0],
            'last_two_leters': word[-2:],
            'last_three_leters': word[-3:]
            }

#Create training and test-sets som of code from from nltk chapter 6, 1.1
features = [(genderFeatures(n), gender) for (n, gender) in raw_data_names]
testSet, trainSet = features[:1000], features[1000:]

#Train classifier
nbc = NaiveBayesClassifier.train(trainSet)
tc = DecisionTreeClassifier.train(trainSet)
ec = MaxentClassifier.train(trainSet, trace=0)


print("Please Wait.")
print("Naive Bayes: ", nltk.classify.accuracy(nbc, testSet), "%")
print("Please Wait..")
print("Tree Classifier", nltk.classify.accuracy(tc, testSet), "%")
print("Please Wait...")
print("Entropy Classifier: ",nltk.classify.accuracy(ec, testSet), "%")
