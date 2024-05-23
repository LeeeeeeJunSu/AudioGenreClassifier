'''
메인 실행 파일
데이터 수집, 전처리, 학습, 예측을 실행한다.
StartProcess 변수 변경을 통해 이전 단계를 건너뛸 수 있다.
FeatureSelection 변수 변경을 통해 어떤 피처를 사용할지 결정할 수 있다.

시작점이 FEATURE_EXTRACTION인 경우
    - Define.PATH_TRAIN_DATA, Define.PATH_VALIDATION_DATA에 데이터가 없는 경우 에러 발생

시작점이 TRAINING인 경우
    - Define.PATH_TRAIN_FEATURE, Define.PATH_VALIDATION_FEATURE에 데이터가 없는 경우 에러 발생

시작점이 VALIDATE인 경우
    - Define.PATH_VALIDATION_FEATURE에 데이터가 없는 경우 에러 발생
    - Define.PATH_MODEL에 모델, 스케일러가 없는 경우 에러 발생

이전에 실행했던 Feature Selection과 다른 Feature Selection을 사용할 경우 FEATURE_EXTRACTION 단계부터 다시 시작해야 한다.

To Do
    1. MFCC, OSC Class를 FeatureExtraction로 통합
        - FeatureExtraction에서 Feature Selection을 결정할 수 있도록 변경
        - FeatureExtraction에서 MFCC, OSC 진행 시 필요한 파라미터를 설정 하는 함수 추가
        - FeatureExtraction에서 extract 함수 진행 시 Feature Selection에 따라 다른 피처를 추출하도록 변경
        - FeatureExtraction에서 extract 함수 반환 값은 dictionary로 변경 ({MFCC: [], OSC: []} 형태)
    2. 각 단계 별 시각화 및 시각화 저장 추가
    3. 진행 상황 출력 추가
'''

import sys
import os
import numpy as np
import yt_dlp
from collections import Counter
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Root Folder를 Python Path에 추가
import Module.Define as Define
from Module import FeatureExtractor
from Module import Classifier
from Module import Util

# 시작 지점 및 사용할 피처 설정
startProcess = Define.Process.FEATURE_EXTRACTION
featureSelection = Define.Feature.MFCC

# 시작 지점에 따른 사전 데이터 설정
trainPathByGenre = None # {Genre: [Path]}
validationPathByGenre = None # {Genre: [Path]}
trainData = None # [Feature]
trainLabel = None # [Label]
validationData = None # {Path : ([feature], [label)}
svmClassifier = None
if startProcess == Define.Process.FEATURE_EXTRACTION:
    trainPathByGenre = Util.loadLastTrainPathByGenre()
    validationPathByGenre = Util.loadLastValidationPathByGenre()
elif startProcess == Define.Process.TRAINING:
    trainData, trainLabel = Util.loadLastTrainFeature()
    validationData = Util.loadLastValidationFeature()
elif startProcess == Define.Process.VALIDATE:
    validationData = Util.loadLastValidationFeature()
    svmClassifier = Util.loadLastModel()

# 시작 지점에 따른 프로세스 실행
while startProcess != Define.Process.End:
    if startProcess == Define.Process.DATA_COLLECTION:
        # URL 설정
        urlByGenre = Util.getURLByGenre()
        # 폴더 생성
        pathTemp = 'temp/'
        if not os.path.exists(pathTemp):
            os.makedirs(pathTemp)
        pathTrain = Define.PATH_TRAIN_DATA + Util.getTimeString() + '/'
        if not os.path.exists(pathTrain):
            os.makedirs(pathTrain)
        pathValidate = Define.PATH_VALIDATE_DATA + Util.getTimeString() + '/'
        if not os.path.exists(pathValidate):
            os.makedirs(pathValidate)
        # 전체 음원 다운로드
        for genre, lstURL in urlByGenre.items():
            strFolder = pathTemp + genre
            if not os.path.exists(strFolder):
                os.makedirs(strFolder)
            ydl_opts = {
                'format': 'm4a/bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'wav'}],
                'outtmpl': strFolder + '/%(title)s.%(ext)s'
            }
            for i, url in enumerate(lstURL):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
        # 장르별 200곡이 넘는 경우 200곡이 되도록 파일 삭제
        for genre in urlByGenre.keys():
            strFolder = pathTemp + genre
            lstFiles = os.listdir(strFolder)
            if len(lstFiles) > 200:
                for i in range(200, len(lstFiles)):
                    os.remove(f'{strFolder}/{lstFiles[i]}')
        # Train, Validate 데이터 분리
        for genre in urlByGenre.keys():
            strFolder = pathTrain + genre
            if not os.path.exists(strFolder):
                os.makedirs(strFolder)
            strFolder = pathValidate + genre
            if not os.path.exists(strFolder):
                os.makedirs(strFolder)
            strFolder = pathTemp + genre
            lstFiles = os.listdir(strFolder)
            for i in range(150):
                os.rename(f'{strFolder}/{lstFiles[i]}', pathTrain + f'{genre}/{lstFiles[i]}')
            for i in range(150, 200):
                os.rename(f'{strFolder}/{lstFiles[i]}', pathValidate + f'{genre}/{lstFiles[i]}')
        # All 폴더 삭제
        os.rmdir(pathTemp)
    elif startProcess == Define.Process.FEATURE_EXTRACTION:
        # 예외 처리
        if trainPathByGenre is None or validationPathByGenre is None:
            print('trainPathByGenre or validationPathByGenre is None')
            break
        # 추출기 생성
        featureExtractor = FeatureExtractor.MFCC(n_fft=1024, n_mfcc=13, segment_length=6)
        # 트레이닝 데이터 추출
        trainData = []
        trainLabel = []
        for genre, lstPath in trainPathByGenre.items():
            for i, path in enumerate(lstPath):
                audio = Util.loadAudio(path)
                feature = featureExtractor.extract(audio)
                for f in feature:
                    meanVector = np.mean(f, axis=0)
                    varVector = np.var(f, axis=0)
                    one_train = np.concatenate([meanVector, varVector])
                    trainData.append(one_train)
                    trainLabel.append(genre)
                print(f'Training : {genre}-{i+1} Complete')
        # 트레이닝 데이터 저장
        Util.saveTrainFeature(trainData, trainLabel)
        print('Training Data Feature Extraction Complete')
        # 검증 데이터 추출
        validationData = {}
        for genre, lstPath in validationPathByGenre.items():
            for i, path in enumerate(lstPath):
                audio = Util.loadAudio(path)
                feature = featureExtractor.extract(audio)
                featureInAudio = []
                for f in feature:
                    meanVector = np.mean(f, axis=0)
                    varVector = np.var(f, axis=0)
                    one_train = np.concatenate([meanVector, varVector])
                    featureInAudio.append(one_train)
                validationData[path] = (featureInAudio, genre)
                print(f'Validation : {genre}-{i+1} Complete')
        # 검증 데이터 저장
        Util.saveValidationFeature(validationData)
        print('Validation Data Feature Extraction Complete')
    elif startProcess == Define.Process.TRAINING:
        # 예외 처리
        if trainData is None or trainLabel is None or validationData is None:
            print('trainData or trainLabel or validationData is None')
            break
        # SVM 학습
        svmClassifier = Classifier.SVM()
        svmClassifier.train(trainData, trainLabel)
        print('Training Complete')
        # 모델 저장
        Util.saveModel(svmClassifier)
        print('Model Save Complete')
    elif startProcess == Define.Process.VALIDATE:
        # 예외 처리
        if validationData is None or svmClassifier is None:
            print('validationData or svmClassifier is None')
            break
        # 예측
        predictResult = {} # {Path: (PredictedGenre, RealGenre)}
        for path, (feature, genre) in validationData.items():
            predict = svmClassifier.predict(feature)
            most_frequent = Counter(predict).most_common(1)[0][0]
            predictResult[path] = (most_frequent, genre)
        # 전체 예측 정확도 계산 (%)
        totalAccuracy = len([path for path in predictResult.keys() if predictResult[path][0] == predictResult[path][1]]) / len(predictResult) * 100
        # 장르별 정확도 계산 (%)
        genreAccuracy = {}
        for path, (predict, real) in predictResult.items():
            if real not in genreAccuracy:
                genreAccuracy[real] = [0, 0]
            genreAccuracy[real][1] += 1
            if predict == real:
                genreAccuracy[real][0] += 1
        for genre, (correct, total) in genreAccuracy.items():
            genreAccuracy[genre] = correct / total * 100
        # 결과 출력 및 저장
        print(f'Total Accuracy: {totalAccuracy}%')
        for genre, accuracy in genreAccuracy.items():
            print(f'{genre} Accuracy: {accuracy}%')
        Util.saveValidationResult(predictResult, totalAccuracy, genreAccuracy)
        print('Validation Save Complete')
    else:
        print('Process Error')
        break
    startProcess = startProcess + 1