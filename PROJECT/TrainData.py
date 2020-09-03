import numpy as np 
import pandas as pd 
import nltk
import string
import seaborn as sns
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import tensorflow as tf
import tempfile

sid = SentimentIntensityAnalyzer()
# plotreader to visualize data
sns.set_style('whitegrid')
#read the data prepared by prepateTestData.csv into pandas dataframe (df)
df = pd.read_csv('samples/Train/samplecsv.csv', encoding='latin1', header=None, names=["ID", "Text", "Author"])


no_punct_translator=str.maketrans('','',string.punctuation)

df['Words'] = df['Text'].apply(lambda t: nltk.word_tokenize(t.translate(no_punct_translator).lower())) #tokenize each sentence without punctuation

df['WordC'] = df['Words'].apply(lambda words: len(words)) #new column which counts number of words

df['SentLenNoPun'] = df['Words'].apply(lambda w: sum(map(len, w))) #char per sentence without punctuation

df['SentLenTot'] = df['Text'].apply(lambda t: len(t))

# sns.boxplot(x = "Author", y = "WordC", data=df, color = "red")
# plt.show()

# print(df.groupby(['Author'])['WordC'].describe()) # words per sentence per author

# print(df.groupby(['Author'])['SentLenTot'].describe()) # char per sentence per author

df['PCount'] = df['Text'].apply(lambda t: len(list(filter(lambda c: c in t, string.punctuation))))
# punctuatin in each sentence

df['PPC'] = df['PCount'] / df['SentLenTot'] 
#punctuation per character

# print(df.groupby(['Author'])['PPC'].describe())
# author group by punctuation

def unique(words): # ratio of unique words to all words in a sentence
    if(len(words) > 0):
        wordC = (len(words))
        uniqueC = len(set(words))
        return uniqueC / wordC
    else:
        return 0

df['UniqueRatio'] = df['Words'].apply(unique)

# print(df.groupby(['Author'])['UniqueRatio'].describe())

#unique ratio visualized
authors = ['CD', 'OH', 'OW']
for author in authors:
    sns.distplot(df[df['Author'] == author]['UniqueRatio'], label = author, hist=False)

# plt.legend();
# plt.show();

#add sentiment column to data frame
df['Sentiment'] = df['Text'].apply(lambda t: sid.polarity_scores(t)['compound'])

df.groupby('Author')['Sentiment'].describe()

# visualize sentiment column
for author in authors:
    sns.distplot(df[df['Author'] == author]['Sentiment'], label = author, hist=False)

# plt.legend()
# plt.show()

# help function to find average length per word, if 0, return 0
avgL = lambda words: sum(map(len, words)) / len(words)  if len(words)>0 else 0#length per word

# add average len word to data frame
df['avgL'] = df['Words'].apply(avgL)

df.groupby(['Author'])['avgL'].describe()

#iterate rows and create new df with author and word
df_words = pd.concat([pd.DataFrame(data={'Author': [row['Author'] for _ in row['Words']], 'word': row['Words']})
           for _, row in df.iterrows()], ignore_index=True)

#remove rows with stop words
df_words = df_words[~df_words['word'].isin(nltk.corpus.stopwords.words('english'))]

df_words.shape

# count occurances of each word each author uses
def authorCommonWords(author, numWords):
    authorWords = df_words[df_words['Author'] == author].groupby('word').size().reset_index().rename(columns={0:'count'})
    authorWords.sort_values('count', inplace=True)
    return authorWords[-numWords:]

#find top words for each author and save to list
ATW = [] #author top words
for author in authors:
    ATW.extend(authorCommonWords(author, 10)['word'].values)

# remove duplicate words from ATW
ATW = list(set(ATW))

# set top words from each author to a ew column
df['topW'] = df['Words'].apply(lambda w: list(set(filter(set(w).__contains__, ATW))))


feature_columns = ['Author', 'WordC', 'SentLenTot', 'PPC', 'UniqueRatio', 'avgL', 'Sentiment']
df_features = df[feature_columns]
df_train=df_features.sample(frac=0.8,random_state=1)
df_dev=df_features.drop(df_train.index)

df_train.head()

FWC = tf.feature_column.numeric_column("WordC") #feature wordC
FTL = tf.feature_column.numeric_column("SentLenTot") # feature sent len
FPPC = tf.feature_column.numeric_column("PPC") #feature punctuation per char
FUR = tf.feature_column.numeric_column("UniqueRatio") #feature unique ratio
FAWL = tf.feature_column.numeric_column("avgL") #feature average len
FS = tf.feature_column.numeric_column("Sentiment") #feature sentiment

Base = [
    FWC, FTL, FPPC, FUR, FAWL, FS
]

model_dir = tempfile.mkdtemp() # base temp directory for running models

# classifying objects
labels_train = df_train['Author']

TrainF = tf.compat.v1.estimator.inputs.pandas_input_fn( #Training function to use with estimator
    x=df_train,
    y=labels_train,
    batch_size=100,
    num_epochs= None, # unlimited
    shuffle=True, # shuffle the training data around
    num_threads=5,
    )

# linear classifier
linear_model = tf.estimator.LinearClassifier(
    model_dir=model_dir, 
    feature_columns=Base,
    n_classes=len(authors),
    label_vocabulary=authors)

train_steps = 5000

# train model
linear_model.train(input_fn=TrainF, steps=train_steps)

dev_test_fn = tf.compat.v1.estimator.inputs.pandas_input_fn(
    x=df_dev,
    y=df_dev['Author'],
    batch_size=100,
    num_epochs=4, 
    shuffle=False, 
    num_threads=5)

print(linear_model.evaluate(input_fn=dev_test_fn)["accuracy"]) # get results between 42% - 70%