import os
import pickle

import numpy as np

from scipy.io.wavfile import read

from src.voiceauth2.feature_extracter import extract_features
import src.utils.parameters as p

def recognize_user_v2(audio_path):

	gmm_files = [os.path.join(p.GMM_MODEL_PATH, fname) for fname in
				os.listdir(p.GMM_MODEL_PATH) if fname.endswith('.gmm')]

	models    = [pickle.load(open(fname, 'rb')) for fname in gmm_files]

	speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname
				in gmm_files]

	#read test file
	sr, audio = read(audio_path)

	# extract mfcc features
	vector = extract_features(audio, sr)
	log_likelihood = np.zeros(len(models))

	#checking with each model one by one
	for i in range(len(models)):
		gmm = models[i]
		scores = np.array(gmm.score(vector))
		log_likelihood[i] = scores.sum()

	print(speakers)
	print(log_likelihood)
	
	pred = np.argmax(log_likelihood)
	identity = speakers[pred]

	print(identity)

	#print("Recognized as - ", identity)

	return True, identity