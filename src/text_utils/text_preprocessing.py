import re
import json
from normalise import normalise
import tensorflow as tf
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

with open('data/custom_abbreviations.json') as outfile:
    my_abbreviations = json.load(outfile)

def removing_number(text: str) -> str:

    text = re.sub(r'[^a-zA-z?!\']', ' ', text)
    text = re.sub(r'[ ]+', ' ', text)

    return text

def text_normalization(text: str) -> str:
    tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='', 
                                                      oov_token='<unk>')
    tokenizer.fit_on_texts(text)
    text = normalise(text, user_abbrevs=my_abbreviations)
    text = ' '.join(t for t in text)

    return text

def text_steamming(text: str) -> str:
    text = ' '.join([stemmer.stem(word) for word in text.split()])

    return text

def text_lemmatization(text: str) ->str:
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])
    return text

def preprocessing(text: str) -> str:
    text = removing_number(text)
    text = text_normalization(text)
    text = text_lemmatization(text)

    return text
