import nltk
from nltk.tokenize import word_tokenize

spacex = open("spacex.txt","r");
text = str(spacex.readlines()[0:5])
spacexT = str(spacex.readlines())
print(text)
spacex.close()
text = text.strip('\\n')
tokens = word_tokenize(text)
tekst = nltk.pos_tag(tokens)
grammar = r"""
        NP: 
        {< NNP > ∗}
        {< DT >? < JJ >? < NNS >}
        {< NN >< NN >}
        """
cp = nltk.RegexpParser(grammar)
result = cp.parse(tekst)
print(result)

