'''
MFCC 특징 추출 테스트
1. RootFolder/Data/Train 폴더 내 음원을 특징추출기(MFCC)를 통해 특징 추출
2. 추출된 특징을 시각화

To do:
어떤 축으로 평균 분산 계산
저주파 대역만 분석에 사용
'''
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Root Folder를 Python Path에 추가
import matplotlib.pyplot as plt
import Define
from Module import FeatureExtractor
from Module import Util

# 각 폴더 별 음악 20 개씩 특징 추출
dictFeature = {}
featureExtractor = FeatureExtractor.MFCC(n_fft=1024, n_mfcc=13, segment_length=6)
for genre in os.listdir(Define.PATH_ALL_DATA):
    lstFeature = []
    for i, file in enumerate(os.listdir(Define.PATH_ALL_DATA + genre)):
        if i >= 20:
            break
        audio, samplingRate = Util.load_audio_file(Define.PATH_ALL_DATA + genre + '/' + file)
        feature = featureExtractor.extract(audio, samplingRate)
        print(f'{genre} {i+1}번째 음악 특징 추출 완료')
        for f in feature:
            lstFeature.append([f.mean(), f.var()])
    dictFeature[genre] = lstFeature

# 시각화
genre_color = {'Jazz': 'red', 'Hiphop': 'blue'}
for genre, feature in dictFeature.items():
    plt.scatter(*zip(*feature), label=genre, color=genre_color[genre])
plt.legend()
plt.show()










