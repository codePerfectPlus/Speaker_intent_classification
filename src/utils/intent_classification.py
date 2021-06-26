import io
import numpy as np
import pandas as pd
import spacy
import json
import tensorflow as tf

df = pd.read_csv("data/intents.csv")
inputs = df["inputs"]

model_path = "intent_classification_model/intent_classification_model.h5"
index_cat_val_pair =  "data/targets.json"

nlp = spacy.load('en_core_web_sm')

def tokenize_data(input_list):
    """ Tokenize the text """
    tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='', oov_token='<unk>')
    
    tokenizer.fit_on_texts(input_list)
        
    return tokenizer

tokenizer = tokenize_data(inputs)

def get_intent(sentence) -> str:
    """ get intent of text using text classification

        inputs: text: str
        outputs: intent: str
    """
    sent_seq = []
    doc = nlp(repr(sentence))
    
    # split the input sentences into words
    for token in doc:
        if token.text in tokenizer.word_index:
            sent_seq.append(tokenizer.word_index[token.text])

        # handle the unknown words error
        else:
            sent_seq.append(tokenizer.word_index['<unk>'])

    sent_seq = tf.expand_dims(sent_seq, 0)
    # predict the category of input sentences
    
    model = load_model(model_path)
    pred = model(sent_seq)
    pred_class = np.argmax(pred.numpy(), axis=1)
    return trg_index_word[str(pred_class[0])]

# helper functions

# loading the categorial to index key value
with io.open(index_cat_val_pair, "r") as outfile:
    trg_index_word = json.load(outfile)

def load_model(model_path):
    """ helper fucntion to load keras model """
    model = tf.keras.models.load_model(model_path)
    return model