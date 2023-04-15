import nltk 
#nltk.download('punkt') tää tarvii olla kun julkasee sivuston?
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
import numpy as np

stemmer = PorterStemmer()
finstemmer = SnowballStemmer("finnish")


# Erotellaan lauseen sanat ja muodostetaan niistä lista
def tokenize(sentence):
    return nltk.word_tokenize(sentence)


# Sanojen stemmaus, eli stem-funktio hakee samankaltaisten sanojen "runko-osan". Tää tarvii saada toimiin suomen kielellä
# Tässä myös isot kirjaimet pieniin
def stem(word):
    return stemmer.stem(word.lower())

def finstem(word):
    return finstemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, all_words):
    """
    sentence = ["hello", "how", "are", "you"] - lause, jonka käyttäjä syöttää, tokenisoitu
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"] - kaikki sanat (stemmattuna), jotka opetusdatamme sisältää
    bog =   [ 0,      1,     0,    1,     0,      0,       0  ] - täsmäävät sanat merk. 1 

    """
    tokenized_sentence = [stem(w) for w in tokenized_sentence] # syötteen sanojen stemmaus
    bag = np.zeros(len(all_words), dtype=np.float32) # kaikki sanat nolliksi
    for i, w, in enumerate(all_words): # enumerate palauttaa indexin ja alkion
        if w in tokenized_sentence: # jos sana löytyy syötteen lauseesta
            bag[i] = 1.0 # alkio muutetaan 1:ksi

    return bag

# sentence = ["hello", "how", "are", "you"]
# words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
# bog = bag_of_words(sentence, words)
#print(bog)


# a = "Kuinka kauan kuljetus kestää?"
# print(a)
# a = tokenize(a)
# print(a)

# words = ["koiramme", "koiranne", "koiriemme"]
# stemmed_words = [finstem(w) for w in words]
# print(stemmed_words)
