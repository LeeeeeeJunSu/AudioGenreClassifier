SAMPLING_RATE = 22050



PATH_TRAIN_DATA = 'Data/TrainData/'
PATH_VALIDATE_DATA = 'Data/ValidationData/'
PATH_TRAIN_FEATURE = 'Data/TrainFeature/'
PATH_VALIDATE_FEATURE = 'Data/ValidationFeature/'
PATH_MODEL = 'Data/Model/'
PATH_RESULT = 'Data/Result/'




class Process:
    DATA_COLLECTION = 1
    FEATURE_EXTRACTION = 2
    TRAINING = 3
    VALIDATE = 4
    End = 5

class Feature:
    MFCC = 'MFCC'
    OSC = 'OSC'
    MFCC_OSC = 'MFCC_OSC'
