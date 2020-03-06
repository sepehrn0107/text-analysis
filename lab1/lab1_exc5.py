import urllib
import nltk
from nltk.tokenize import sent_tokenize,word_tokenize
import requests
url = "https://www.ntnu.edu/vacancies"
r = requests.get(url)
html = r.text


from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")

def getAmountOfVacancies():
    counter = 0
    for vacancies in soup.find_all("div",attrs={"class":"vacancies"}):
        for description in vacancies.find_all("span",attrs={"class":"rss_entry_description"}):
            counter+=1
    return counter

def getAllTitlesOfVacancies():
    titles_vacancies = []
    for vacancies in soup.find_all("div",attrs={"class":"vacancies"}):
        for description in vacancies.find_all("span",attrs={"class":"rss_entry_description"}):
            titles_vacancies.append(description.text)
    return titles_vacancies

def printAllTitles(input):
    for item in input:
        print(item)

def getAllDeadlines():
    deadlines = []
    for vacancies in soup.find_all("div",attrs={"class","vacancies"}):
        for header in foo.find_all("h3"):
            deadlines.append(header.text[header.text.index("Søknadsfrist"):])

if __name__ == "__main__":
    x = 5
