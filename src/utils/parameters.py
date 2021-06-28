# Signal processing
SAMPLE_RATE = 16000
PREEMPHASIS_ALPHA = 0.97
FRAME_LEN = 0.025
FRAME_STEP = 0.01
NUM_FFT = 512
BUCKET_STEP = 1
MAX_SEC = 10

# Model
MODEL_FILE = "voice_auth_model_cnn"
COST_METRIC = "cosine"
INPUT_SHAPE = (NUM_FFT, None, 1)

# IO
EMBED_LIST_FILE = "data/embed"

# Recognition
THRESHOLD = 0.020


# text-classification parameters
INTENT_CLASSIFICATION_MODEL = "intent_classification_model/intent_classification_model.h5"
INDEX_CAT_VAL_PAIR = "data/targets.json"
JSON_DATA_DIR = "data/IntentClassificationData"
