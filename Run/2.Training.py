'''
Implement the SVM Classifier Training
1. RootFolder/Data/Train 폴더 내 음원을 특징추출기(MFCC, OSC)를 통해 특징 추출
2. 추출된 특징과 라벨 정보를 이용하여 SVM 분류기를 학습
3. 학습된 모델을 RootFolder/Data/Model/Model_시간 형식으로 저장
'''
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Root Folder를 Python Path에 추가