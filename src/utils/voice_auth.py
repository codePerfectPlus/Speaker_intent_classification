import os
import numpy as np
from scipy.spatial.distance import cdist, euclidean, cosine 

import logging
import warnings
from tensorflow.keras.models import load_model

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # FATAL
logging.getLogger('tensorflow').setLevel(logging.FATAL)

# IMPORT USER-DEFINED FUNCTIONS
from src.utils.feature_extraction import get_embedding
import src.utils.parameters as p

def enroll_user(name, file):
    """ 
    Enroll a user with an audio file

        inputs: str (Name of the person to be enrolled and registered)
                str (Path to the audio file of the person to enroll)
                
        outputs: response
    """
    try:
        model = load_model(p.MODEL_FILE)
        logging.info("Loading model weights from [{}]....".format(p.MODEL_FILE))
    except:
        return "Failed to load weights from the weights file, please ensure *.pb file is present in the MODEL_FILE directory"
    try:
        logging.info("Processing enroll sample....")
        enroll_result = get_embedding(model, file, p.MAX_SEC)
        
        enroll_embs = np.array(enroll_result.tolist())
        speaker = name
    except:
        return "Error processing the input audio file. Make sure the path."
    try:
        np.save(os.path.join(p.EMBED_LIST_FILE, speaker + ".npy"), enroll_embs)
        return f"Successfully enrolled the {speaker} on server"
    except:
        return "Unable to save the user into the database."


def recognize_user(file):
    """
    Recognize the input audio file by comparing to saved users' voice prints

        inputs: str (Path to audio file of unknown person to recognize)
        outputs: str (Name of the person recognized)"""
    
    if os.path.exists(p.EMBED_LIST_FILE):
        embeds = os.listdir(p.EMBED_LIST_FILE)
    if len(embeds) == 0:
        logging.info("No enrolled users found")
        exit()
    logging.info("Loading model weights from [{}]....".format(p.MODEL_FILE))
    try:
        model = load_model(p.MODEL_FILE)

    except:
        logging.info("Failed to load weights from the weights file, please ensure *.pb file is present in the MODEL_FILE directory")
        exit()
        
    distances = {}
    logging.info("Processing test sample....")
    logging.info("Comparing test sample against enroll samples....")

    test_result = get_embedding(model, file, p.MAX_SEC)
    test_embs = np.array(test_result.tolist())

    for emb in embeds:
        enroll_embs = np.load(os.path.join(p.EMBED_LIST_FILE, emb))
        speaker = emb.replace(".npy", "")
        distance = euclidean(test_embs, enroll_embs)
        distances.update({speaker : distance})

    if min(list(distances.values()))<p.THRESHOLD:
        response = min(distances, key=distances.get)
        return response

    else:
        logging.info("Could not identify the user, try enrolling again with a clear voice sample")
        response = ("Score: ", min(list(distances.values())))
        return response
        
#Helper functions
def file_choices(choices, filename):
    ext = os.path.splitext(filename)[1][1:]
    if ext not in choices:
        logging.info("file doesn't end with one of {}".format(choices))
    return filename

def get_extension(filename):
    return os.path.splitext(filename)[1][1:]




