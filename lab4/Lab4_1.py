from nltk.corpus import brown
import nltk

tagged_brown = brown.tagged_words()

NP_PP = nltk.RegexpParser("NP_PP: {(<V.*>)(<IN>)?((<D.*>|<AT>)?<JJ>*(<N.*>))}")
result = NP_PP.parse(tagged_brown[:40])

print(result)