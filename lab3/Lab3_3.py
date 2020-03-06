from collections import defaultdict
'''
The base model
'''
class Model(object):
	def __init__(self):
		self.counts = defaultdict(float)
		self.counts['total'] = 0.0
		self.wordcounts = defaultdict(float)
		self.wordcounts['total'] = 0.0
		self.words = defaultdict(float)
		self.allwords = defaultdict(float)
	
	def train(self, type, examples):
		if not type in self.counts:
			self.counts[type] = 0.0
		if not type in self.wordcounts:
			self.wordcounts[type] = 0.0
		for example in examples:
			self.counts['total'] += 1.0
			self.counts[type] += 1.0
			if not type in self.words:
				self.words[type] = defaultdict(float)
			for word in example.split(' '):
				self.wordcounts['total'] += 1.0
				self.wordcounts[type] += 1.0
				self.allwords[word] = True
				if not word in self.words[type]:
					self.words[type][word] = 1.0
				else:
					self.words[type][word] += 1.0

	def prior(self, type):
		return self.implementation.prior(type)

	def probability(self, word, type):
		return self.implementation.probability(word, type)

	def classify(self, type, data):
		return self.implementation.classify(type, data)
'''
Model with smoothing option
'''
class Smoothing(Model):
	def __init__(self, k = 1):
		Model.__init__(self)
		self.k = k

	def prior(self, type):
		return (self.counts[type] + self.k) / (self.counts['total'] + (self.k * len(self.words.keys())))

	def probability(self, word, type):
		a = self.words[type][word] + self.k
		b = self.wordcounts[type] + (self.k * len(self.allwords))
		return a / b

	def classify(self, type, data):
		if not isinstance(data, list):
			a = self.probability(data, type) * self.prior(type)
			b = 0.0
			for _type in self.words:
				b += self.probability(data, _type) * self.prior(_type)
			return a / b
		else:
			a = self.prior(type)
			for word in data:
				a *= self.probability(word, type)
			b = 0.0
			for _type in self.words:
				bb = self.prior(_type)
				for word in data:
					bb *= self.probability(word, _type)
				b += bb
			return a/b
		    
class MaximumLikelihood(Smoothing):
    def __init__(self, k = 0):
        Smoothing.__init__(self,k)
		
#####################################################################################################################################
# Read me: The classifier model:																												#
#	funtions:																														#
#	1- initialization(k) of the model																								#
#       - k == 0: no-smooth mode 																									#
#       - k != 0: smooth mode																										#
#	2- prior(label) : get prior probability of label in the model																	#
#	3- probability(feature, label) :  the probability that input values with that label will have that feature						#
#	4- classify(label, data) :  the probability that input data is classified as label						 						#
#####################################################################################################################################

def Lab3_3a():
    print ('Lab3_3a')
    MOVIE = ['a perfect world', 'my perfect woman', 'pretty woman']
    SONG = ['a perfect day', 'electric storm', 'another rainy day']

    model = MaximumLikelihood(1)    
    model.train('movie', MOVIE)
    model.train('song', SONG)

    #1. Prior probability of labels used in training. (movie, song)
    print("Movie: ", Smoothing.prior(model,"movie"))
    print("Song: ", Smoothing.prior(model,"song"))

    #2. Probability of word under given prior label (i.e., P(word|label)) according to this model.
            #a. P(perfect|movie)
    print("perfect|movie: ", Smoothing.probability(model,"perfect", "movie"))

            #b. P(storm|movie)
    print("storm|movie: ", Smoothing.probability(model,"storm", "movie"))

            #c. P(perfect|song)
    print("perfect|song: ", Smoothing.probability(model,"perfect", "song"))

            #d. P(storm|song)
    print("storm|song: ", Smoothing.probability(model,"storm", "song"))

    #3. Probability of the title 'perfect storm' is labeled as 'movie' and 'song' with no-smooth mode and smooth mode (k=1).
    print("Likelyhood of prefetct storm being both a movie and a song title smooth: ",Smoothing.classify(model, "song", "perfect storm") * Smoothing.classify(model, "movie", "perfect storm"))
    try:
        model2 = MaximumLikelihood(0)
        model2.train('movie', MOVIE)
        model2.train('song', SONG)
        print("Likelyhood of prefetct storm being both a movie and a song title no-smooth: ",Smoothing.classify(model2, "song", "perfect storm") * Smoothing.classify(model2, "movie", "perfect storm"))
    except:
        print("Does not work")
    
def Lab3_3b():
    print ('\nLab3_3b')

    HAM = ["play sport today", "went play sport", "secret sport event", "sport is today", "sport costs money"]
    SPAM = ["offer is secret", "click secret link", "secret sport link"]

    model = MaximumLikelihood()
    model.train('S', SPAM)
    model.train('H', HAM)
    
        #1. Prior probability of labels for SPAM, HAM data.
    print("Prior SPAM: ", Smoothing.prior(model, "S"))
    print("Prior HAM: ", Smoothing.prior(model, "H"))
        #2. Probability of word 'secret', 'sport' under given prior label (SPAM, HAM)
    print("Secret SPAM: ", Smoothing.probability(model, "secret", "S"))
    print("Secret HAM: ", Smoothing.probability(model, "secret", "H"))
    print("Sport SPAM:", Smoothing.probability(model, "sport", "S"))
    print("Sport HAM: ", Smoothing.probability(model, "sport", "H"))
        #3. Probabilities of: The word 'today is secret' is labeled as SPAM, HAM with no-smooth mode and smooth mode (k=1)  
    try:
        print("Today is secret, no-smooth SPAM: ",Smoothing.classify(model, "S","today is secret"))
        print("Today is secret, no-smooth HAM: ", Smoothing.classify(model, "H","today is secret"))  
    except:
        print("error")

    model2 = MaximumLikelihood(1)
    model2.train('S', SPAM)
    model2.train('H', HAM)
    print("Today is secret, smooth SPAM: ", Smoothing.classify(model2, "S","today is secret"))
    print("Today is secret, smooth HAM: ", Smoothing.classify(model2, "H","today is secret"))  


    
if __name__ == '__main__':
    Lab3_3a()
    Lab3_3b()
