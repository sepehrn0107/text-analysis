import urllib
import nltk
import time
from nltk.tokenize import sent_tokenize,word_tokenize
from bs4 import BeautifulSoup
import requests
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import sys
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from collections import Counter
from string import punctuation

driver = webdriver.Chrome()
driver.get("https://openreview.net/group?id=ICLR.cc/2020/Conference#reject")
time.sleep(10);
rejected_notes = driver.find_elements_by_class_name("note")

rejected = len(rejected_notes)
text = ""
authors = []

inputElement = driver.find_element_by_css_selector("a[href*='accept-poster']")
inputElement.send_keys("\n") #send enter for links, buttons
time.sleep(5)
accepted_notes = driver.find_elements_by_class_name("note")
accepted = len(accepted_notes)

for note in accepted_notes:
    text += note.find_element_by_tag_name('a').get_attribute('innerHTML')
    print(text)
    for author in note.find_elements_by_class_name('profile-link'):
        author_name = author.get_attribute('innerHTML')
        authors.append(author_name)


inputElement = driver.find_element_by_css_selector("a[href*='accept-spotlight']")
inputElement.send_keys("\n") #send enter for links, buttons
time.sleep(5)
accepted_notes = driver.find_elements_by_class_name("note")
accepted += len(accepted_notes)

for note in accepted_notes:
    text += note.find_element_by_tag_name('a').get_attribute('innerHTML')
    print(text)
    for author in note.find_elements_by_class_name('profile-link'):
        author_name = author.get_attribute('innerHTML')
        authors.append(author_name)

inputElement = driver.find_element_by_css_selector("a[href*='accept-talk']")
inputElement.send_keys("\n") #send enter for links, buttons
time.sleep(5)
accepted_notes = driver.find_elements_by_class_name("note")
accepted += len(accepted_notes)

for note in accepted_notes:
    text += note.find_element_by_tag_name('a').get_attribute('innerHTML')
    print(text)
    for author in note.find_elements_by_class_name('profile-link'):
        author_name = author.get_attribute('innerHTML')
        authors.append(author_name)

driver.close()
print("the amount of accepted requests is: ", accepted , "\nThe amount of rejected requests is: ", rejected ,"\nThe rate of accepted to rejected is accepted /rejected =",accepted/rejected)

def findMostCommonWords(text):
    allWords = nltk.tokenize.word_tokenize(text)
    allWordDist = nltk.FreqDist(w.lower() for w in allWords)
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.append(":")
    allWordExceptStopDist = nltk.FreqDist(w.lower() for w in allWords if w not in stopwords) 
    mostCommon= allWordDist.most_common(10)
    mostCommon2 = allWordExceptStopDist.most_common(10)
    print("The 10 most common words with stopwords: ",mostCommon)
    print("\nThe 10 most common words without stopwords: ",mostCommon2)

def findTopTenAuthors(authors):
    with_stp = Counter()
    for item in authors:
        item = item.rstrip("*")
        with_stp[item] +=1
    print("The 10 authors with the most number of papers: ",with_stp.most_common(10))

findTopTenAuthors(authors)
findMostCommonWords(text)


