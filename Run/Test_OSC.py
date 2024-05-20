'''
OSC 특징 추출
1. RootFolder/Data/Train 폴더 내 일부 음원을 OSC 특징 추출기를 통해 특징 추출
2. 추출된 특징을 데이터프레임 형식으로 변환
3. 밴드 별 대비값을 박스 플롯으로 시각화
'''
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Root Folder를 Python Path에 추가
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import Define
from Module import FeatureExtractor
from Module import Util

# 각 폴더 별 음악 20 개씩 파일 경로 리스트 생성
dictPath = {} # {장르명: pathList}
for genre in os.listdir(Define.PATH_TRAIN_DATA):
    lstPath = []
    for i, file in enumerate(os.listdir(Define.PATH_TRAIN_DATA + genre)):
        if i >= 20:
            break
        lstPath.append(Define.PATH_TRAIN_DATA + genre + '/' + file)
    dictPath[genre] = lstPath

# 각 장르별 OSC 리스트 생성
dictOSC = {} # {장르명: oscList}
featureExtractor = FeatureExtractor.OSC()
for genre, lstPath in dictPath.items():
    lstOSC = []
    for i, path in enumerate(lstPath):
        audio, samplingRate = Util.load_audio_file(path)
        osc = featureExtractor.extract(audio, samplingRate)
        lstOSC.append(osc)
        print(f'{genre} {i+1}번째 음악 OSC 추출 완료')
    dictOSC[genre] = lstOSC


# dictOSC 데이터 구조 파싱
data = []
for genre, audio_list in dictOSC.items():
    for seg_list, band_ranges in audio_list:
        for seg, (low, high) in zip(seg_list, band_ranges):
            band_label = f"{low}-{high}"
            for value in seg:
                data.append({
                    '장르': genre,
                    '밴드 범위': band_label,
                    '대비값': value
                })
df = pd.DataFrame(data)

plt.figure(figsize=(12, 8))
sns.boxplot(x='밴드 범위', y='대비값', hue='장르', data=df, palette='Set3')
plt.title('밴드 범위별 대비값 박스 플롯')
plt.xlabel('밴드 범위')
plt.ylabel('대비값')
plt.legend(title='장르', loc='upper right')
plt.xticks(rotation=45)  # 밴드 범위 레이블이 긴 경우, 가독성을 위해 회전
plt.yscale('log')  # 대비값의 스케일이 클 경우 로그 스케일로 표시
plt.grid(True)
plt.show()




