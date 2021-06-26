import io
import re
import json
import numpy as np
import pandas as pd

from normalise import normalise

import tensorflow as tf
from tensorflow.keras import layers

from src.config import logging
from src import parameters as p

logging.info('loading json data')

with io.open('data/intents.json') as f:
    intents = json.load(f)

logging.info('preprocessing the data')


def preprocessing(text: str) -> str:

    tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='', 
                                                      oov_token='<unk>')
    tokenizer.fit_on_texts(text)

    text = normalise(text, verbose=True)
    text = ' '.join(t for t in text)

    text = re.sub(r'[^a-zA-z.?!\']', ' ', text)
    text = re.sub(r'[ ]+', ' ', text)

    return text


inputs, targets = [], []

for intent in intents['intents']:
    for text in intent['text']:
        inputs.append(preprocessing(text))
        targets.append(intent['intent'])


def tokenize_data(input_list):
    tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='',
                                                      oov_token='<unk>')

    tokenizer.fit_on_texts(input_list)

    input_seq = tokenizer.texts_to_sequences(input_list)

    input_seq = tf.keras.preprocessing.sequence.pad_sequences(
        input_seq, padding='pre')

    return tokenizer, input_seq


def create_categorical_target(targets):
    word = {}
    categorical_target = []
    counter = 0
    for trg in targets:
        if trg not in word:
            word[trg] = counter
            counter += 1
        categorical_target.append(word[trg])

    categorical_tensor = tf.keras.utils.to_categorical(
        categorical_target, num_classes=len(word), dtype='int32')

    return categorical_tensor, dict((v, k) for k, v in word.items())


tokenizer, input_tensor = tokenize_data(inputs)
target_tensor, trg_index_word = create_categorical_target(targets)

# saving categorial to target index into json file to showing prediction output

with open(p.INDEX_CAT_VAL_PAIR, "w") as outfile:
    json.dump(trg_index_word, outfile)

logging.info('input shape: {} and output shape: {}'.format(
    input_tensor.shape, target_tensor.shape))

epochs = 50
vocab_size = len(tokenizer.word_index) + 1
embed_dim = 512
units = 128
target_length = target_tensor.shape[1]

logging.info('creating intent classification model')
model = tf.keras.models.Sequential([
    layers.Embedding(vocab_size, embed_dim),
    layers.Bidirectional(layers.LSTM(units, dropout=0.2)),
    layers.Dense(units, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(target_length, activation='softmax')
])

optimizer = tf.keras.optimizers.Adam(lr=1e-2)
model.compile(optimizer=optimizer,
              loss="categorical_crossentropy", metrics=['accuracy'])

logging.info(model.summary())

early_stop = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=5)

logging.info('starting model training')
model.fit(input_tensor, target_tensor, epochs=epochs, callbacks=[early_stop])

logging.info('Saving new model')
model.save(p.INTENT_CLASSIFICATION_MODEL)

logging.info('saving inputs and outputs to csv')

df = pd.DataFrame()
df["inputs"] = inputs
df["targets"] = targets

df.to_csv("data/intents.csv")
