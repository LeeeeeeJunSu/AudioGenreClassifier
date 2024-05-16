#Import Utility Function

import scipy.io.wavfile as wavfile


# Audio File Save (Wav)
def save_audio_file(path, audio, samplingRate = 16000):
    wavfile.write(path, 16000, audio)

# Audio File Load (Wav)
def load_audio_file(path):
    samplingRate, audio = wavfile.read(path)
    # mono channel
    if len(audio.shape) > 1:
        audio = audio[:, 0]
    return audio, samplingRate

# Feature Save (Numpy)