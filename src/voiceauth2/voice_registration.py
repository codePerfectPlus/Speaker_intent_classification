import os
import pickle

import numpy as np

from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture

from src.voiceauth2.feature_extracter import extract_features
import src.utils.parameters as p

def enroll_user_v2(username, audio_path):
    """ Register new user

        input: 
            - username : for saving model in db using username
            - audio_path : Path for voice clip for registration

     """
    if not os.path.isfile(os.path.join(p.GMM_MODEL_PATH + username) + '.gmm'):
        features = np.array([])

        # reading audio files of speaker
        (sr, audio) = read(audio_path)

        # extract 40 dimensional MFCC & delta MFCC features
        vector  = extract_features(audio, sr)

        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))

        gmm = GaussianMixture()
        gmm.fit(features)

        # saving the trained gaussian model
    
        pickle.dump(gmm, open(p.GMM_MODEL_PATH + username + '.gmm', 'wb'))
        print(username + ' added successfully')

        return True, f"Successfully enrolled the {username} on server"
    return False, f"{username} User already exists on server. Please choose a unique username."
