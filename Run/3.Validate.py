'''
Implement the SVM Classifier Validation
1. RootFolder/Data/Model 폴더 내 가장 최근에 저장된 모델을 불러옴
2. RootFolder/Data/Validate 폴더 내 음원을 특징추출기(MFCC, OSC)를 통해 특징 추출
3. 추출된 특징과 라벨 정보를 이용하여 SVM 분류기를 통해 예측
4. 예측 결과 CSV 파일로 저장
5. 예측 결과에 대한 Accuracy(전체, 장르별) 계산, 시각화, 저장
'''
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Root Folder를 Python Path에 추가