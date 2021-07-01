""" File for loading json text data for intent classification """
import io
import os
import json
import numpy as np

import src.utils.parameters as p
from src.text_utils.text_preprocessing import preprocessing

def load_text_data_from_json():
    
    inputs, targets = [], []
    for file in os.listdir(p.JSON_DATA_DIR):
        if file.endswith(".json"):
            with io.open(os.path.join(p.JSON_DATA_DIR, file), 'r') as f:
                intents = json.load(f)

                for intent in intents['intents']:
                    for text in intent['text']:
                        np.array(inputs.append(preprocessing(text)))
                        np.array(targets.append(intent['intent']))
    
    return inputs, targets