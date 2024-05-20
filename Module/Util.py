import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Root Folder를 Python Path에 추가
import scipy.io.wavfile as wavfile
import scipy.signal as signal
import numpy as np
import Define

# Audio File Load (Wav)
def load_audio_file(path):
    # Wav 원본 데이터
    samplingRate, audio = wavfile.read(path)
    # 스테레오면 모노로 변경
    if len(audio.shape) > 1 and audio.shape[1] == 2:
        audio = np.mean(audio, axis=1)
    # 샘플링 레이트 변경
    audio = signal.resample(audio, int(len(audio) * Define.SAMPLING_RATE / samplingRate))
    return audio