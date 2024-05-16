import IO
import FeatureExtractor
import matplotlib.pyplot as plt
import numpy as np

# 파일을 데이터 수집, 학습, 검증,    추출기, 분류기, 유틸(IO, 시각화) 으로 나누기




# 장르, 장르 별 시각화 색상 설정
genre_color = {
    'R': 'red',
    'H': 'blue',
    'B': 'green'
}

# 음원, 샘플링 레이트, 장르
inputList = []

audio, samplingRate = IO.load_audio_file('Test\\R_DAY6_Welcome to the Show.wav')
inputList.append([audio, samplingRate, 'R'])

audio, samplingRate = IO.load_audio_file('Test\\R_QWER_Discord.wav')
inputList.append([audio, samplingRate, 'R'])

audio, samplingRate = IO.load_audio_file('Test\\R_QWER_고민중독.wav')
inputList.append([audio, samplingRate, 'R'])

audio, samplingRate = IO.load_audio_file('Test\\R_SPYAIR_Some Like It Hot.wav')
inputList.append([audio, samplingRate, 'R'])

audio, samplingRate = IO.load_audio_file('Test\\H_BLACKPINK _마지막처럼.wav')
inputList.append([audio, samplingRate, 'H'])

audio, samplingRate = IO.load_audio_file('Test\\H_Creepy_Nuts_Bling-Bang-Bang-Born.wav')
inputList.append([audio, samplingRate, 'H'])

audio, samplingRate = IO.load_audio_file('Test\\H_KISS OF LIFE_Midas Touch.wav')
inputList.append([audio, samplingRate, 'H'])

audio, samplingRate = IO.load_audio_file('Test\\H_pH-1_BEAUTIFUL.wav')
inputList.append([audio, samplingRate, 'H'])

audio, samplingRate = IO.load_audio_file('Test\\H_ZICO_SPOT.wav')
inputList.append([audio, samplingRate, 'H'])

audio, samplingRate = IO.load_audio_file('Test\\B_이찬원_하늘 여행.wav')
inputList.append([audio, samplingRate, 'B'])

audio, samplingRate = IO.load_audio_file('Test\\B_임영웅_Do or Die.wav')
inputList.append([audio, samplingRate, 'B'])

audio, samplingRate = IO.load_audio_file('Test\\B_임영웅_모래 알갱이.wav')
inputList.append([audio, samplingRate, 'B'])

audio, samplingRate = IO.load_audio_file('Test\\B_임영웅_온기.wav')
inputList.append([audio, samplingRate, 'B'])

# 장르 별 MFCC 특징 추출
featureExtractor = FeatureExtractor.MFCC(n_fft=1024, n_mfcc=26, segment_length=6)
features = {} # str:Gerne, list:Feature
features['R'] = []
features['H'] = []
features['B'] = []
for i in range(len(inputList)):
    featureInAudio = featureExtractor.extract(inputList[i][0], inputList[i][1])
    for feature in featureInAudio:
        features[inputList[i][2]].append([np.mean(feature), np.var(feature)])

# 장르 별 MFCC 특징 시각화
plt.scatter(*zip(*features['R']), label='R', color=genre_color['R'])
plt.scatter(*zip(*features['H']), label='H', color=genre_color['H'])
plt.scatter(*zip(*features['B']), label='B', color=genre_color['B'])
plt.legend()
plt.show()




































# Load the data
audio1, samplingRate1 = IO.load_audio_file('IVE-아이브-_해야-_HEYA__-MV-_07EzMbVH3QE_.wav')
audio2, samplingRate2 = IO.load_audio_file('QWER \'고민중독\' Official MV [ImuWa3SJulY].wav')
audio3, samplingRate3 = IO.load_audio_file('ZICO (지코) ‘SPOT! (feat. JENNIE)’ Official MV [xfqBQ2XhBCg].wav')

# Extract the features
featureExtractor = FeatureExtractor.MFCC(n_fft=1024, n_mfcc=26, segment_length=6)
features1 = featureExtractor.extract(audio1, samplingRate1)
features2 = featureExtractor.extract(audio2, samplingRate2)
features3 = featureExtractor.extract(audio3, samplingRate3)

#x = feature mean
#y = feature variance
features1Statics = []
for feature in features1:
    features1Statics.append([np.mean(feature), np.var(feature)])

features2Statics = []
for feature in features2:
    features2Statics.append([np.mean(feature), np.var(feature)])

features3Statics = []
for feature in features3:
    features3Statics.append([np.mean(feature), np.var(feature)])

#show the features
plt.scatter(*zip(*features1Statics), label='IVE')
plt.scatter(*zip(*features2Statics), label='QWER')
plt.scatter(*zip(*features3Statics), label='ZICO')
plt.legend()
plt.show()
