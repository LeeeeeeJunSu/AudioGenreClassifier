# 상위 폴더 Import를 위한 경로 추가
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 필요한 Module Import
import re
import time
import pickle
import numpy as np
import scipy.io.wavfile as wavfile
import scipy.signal as signal

# Custom Module Import
import Module.Define as Define
import Module.Classifier as Classifier

'''
Utility Function 구현 파일
Run.py에서 사용되는 함수들을 구현
    - loadLastTrainPathByGenre(): 마지막 데이터 추출 시 트레이닝 데이터 경로 반환
    - loadLastValidationPathByGenre(): 마지막 데이터 추출 시 검증 데이터 경로 반환
    - loadLastTrainFeature(): 마지막 특징 추출 시 트레이닝 데이터 반환
    - loadLastValidationFeature(): 마지막 특징 추출 시  검증 데이터 반환
    - loadLastModel(): 마지막 트레이닝 시 모델 반환
    - loadAudio(path): path 경로의 오디오 파일을 로드하여 반환
    - saveTrainFeature(data, label): 트레이닝 데이터 저장
    - saveValidationFeature(data): 검증 데이터 저장
    - saveModel(model): 모델 저장
    - saveValidationResult(result, totalAccuracy, genreAccuracy): 검증 결과 저장
    - getURLByGenre(): 장르 별 유튜브 플레이 리스트 URL 반환
'''

def loadLastTrainPathByGenre():
    base_path = Define.PATH_TRAIN_DATA
    all_folders = [os.path.join(base_path, folder) for folder in os.listdir(base_path)]
    latest_folder = max(all_folders, key=os.path.getmtime)
    dictPath = {}
    for genre in os.listdir(latest_folder):
        lstPath = []
        for i, file in enumerate(os.listdir(latest_folder + '/' + genre)):
            lstPath.append(latest_folder + '/' + genre + '/' + file)
        dictPath[genre] = lstPath
    return dictPath

def loadLastValidationPathByGenre():
    base_path = Define.PATH_VALIDATE_DATA
    all_folders = [os.path.join(base_path, folder) for folder in os.listdir(base_path)]
    latest_folder = max(all_folders, key=os.path.getmtime)
    dictPath = {}
    for genre in os.listdir(latest_folder):
        lstPath = []
        for i, file in enumerate(os.listdir(latest_folder + '/' + genre)):
            lstPath.append(latest_folder + '/' + genre + '/' + file)
        dictPath[genre] = lstPath
    return dictPath

def loadLastTrainFeature():
    base_path = Define.PATH_TRAIN_FEATURE
    all_files = [os.path.join(base_path, file) for file in os.listdir(base_path)]
    latest_file = max(all_files, key=os.path.getmtime)
    x = []
    y = []
    with open(latest_file, 'r') as f:
        for line in f:
            line = line.strip().split(',')
            x.append(list(map(float, line[:-1])))
            y.append(line[-1])
    return x, y

def loadLastValidationFeature():
    base_path = Define.PATH_VALIDATE_FEATURE
    all_files = [os.path.join(base_path, file) for file in os.listdir(base_path)]
    latest_file = max(all_files, key=os.path.getmtime)
    dictData = {}
    with open(latest_file, 'r') as f:
        for line in f:
            line = line.strip().split(',')
            path = line[-1]
            feature = list(map(float, line[:-2]))
            label = line[-2]
            if path not in dictData:
                dictData[path] = ([], label)
            dictData[path][0].append(feature)
    return dictData

def loadLastModel():
    base_path = Define.PATH_MODEL
    all_folders = [os.path.join(base_path, folder) for folder in os.listdir(base_path)]
    latest_folder = max(all_folders, key=os.path.getmtime)
    with open(latest_folder + '/Model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open(latest_folder + '/Scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    svm = Classifier.SVM()
    svm.svm_model = model
    svm.scaler = scaler
    return svm

def loadAudio(path):
    samplingRate, audio = wavfile.read(path)
    if len(audio.shape) > 1 and audio.shape[1] == 2:
        audio = np.mean(audio, axis=1)
    audio = signal.resample(audio, int(len(audio) * Define.SAMPLING_RATE / samplingRate))
    return audio

def saveTrainFeature(data, label):
    strFeaturePath = Define.PATH_TRAIN_FEATURE + getTimeString() + '.csv'
    strFolderPath = os.path.dirname(strFeaturePath)
    if not os.path.exists(strFolderPath):
        os.makedirs(strFolderPath)
    with open(strFeaturePath, 'w') as f:
        for i in range(len(data)):
            line = ','.join(map(str, data[i])) + ',' + label[i] + '\n'
            f.write(line)

def saveValidationFeature(data):
    strFeaturePath = Define.PATH_VALIDATE_FEATURE + getTimeString() + '.csv'
    strFolderPath = os.path.dirname(strFeaturePath)
    if not os.path.exists(strFolderPath):
        os.makedirs(strFolderPath)
    with open(strFeaturePath, 'w') as f:
        for path, (feature, label) in data.items():
            safe_path_str = re.sub(r'[\\/*?:"<>|,]', '', path)
            for i in range(len(feature)):
                line = ','.join(map(str, feature[i])) + ',' + label + ',' + safe_path_str + '\n'
                f.write(line)        

def saveModel(model):
    strModelPath = Define.PATH_MODEL + getTimeString() + '/'
    if not os.path.exists(strModelPath):
        os.makedirs(strModelPath)
    with open(strModelPath + 'Model.pkl', 'wb') as f:
        pickle.dump(model.svm_model, f)
    with open(strModelPath + 'Scaler.pkl', 'wb') as f:
        pickle.dump(model.scaler, f)

def saveValidationResult(result, totalAccuracy, genreAccuracy):
    strResultPath = Define.PATH_RESULT + getTimeString() + '.txt'
    strFolderPath = os.path.dirname(strResultPath)
    if not os.path.exists(strFolderPath):
        os.makedirs(strFolderPath)
    with open(strResultPath, 'w') as f:
        f.write(f'Total Accuracy: {totalAccuracy}\n')
        for genre, accuracy in genreAccuracy.items():
            f.write(f'{genre} Accuracy: {accuracy}\n')
        for path, (label, pred) in result.items():
            safe_path_str = re.sub(r'[\\/*?:"<>|,]', '', path)
            f.write(f'{safe_path_str} {label} {pred}\n')

def getURLByGenre():
    lstURL_Jazz = [
        'https://music.youtube.com/playlist?list=RDCLAK5uy_lFtS4IOgcFt0ba5bLlzgaRer3eZxzUViQ', #63
        'https://music.youtube.com/playlist?list=RDCLAK5uy_kQhKviYMP4sYcy2RH3VYd-1dyW4gzrTAo', #58
        'https://music.youtube.com/playlist?list=RDCLAK5uy_ldZHTCRFn2hQZ0FGOUB7CSKJ63VpwpsXg', #68
        'https://music.youtube.com/playlist?list=RDCLAK5uy_mQHYdV2Vf3lFugUQfkpSsiSfgGdweAV4c', #55
        'https://music.youtube.com/playlist?list=RDCLAK5uy_k7a3ErfM0mejMiVztB0eN4NdTGJMKf9mQ', #57
    ]
    lstURL_Hiphop = [
        'https://music.youtube.com/playlist?list=RDCLAK5uy_mrsOoMkoxlxytLvSxicawMdC3TdBjGIe0', #65
        'https://music.youtube.com/playlist?list=RDCLAK5uy_nop3Tuox6usw3lploMNSliVcytOQnokbQ', #59
        'https://music.youtube.com/playlist?list=RDCLAK5uy_kP2172rQNb3KFXz880xp6M98R_ME5CIKA', #89
        'https://music.youtube.com/playlist?list=RDCLAK5uy_l0pAECrSAnyfXn-bgZ6XveIzAjDixOiX0', #65
        'https://music.youtube.com/playlist?list=RDCLAK5uy_kN4eY_ibobGvCBwIJGEGpDjuwzYHIG_iE', #129
    ]
    lstURL_Rock = [
        'https://music.youtube.com/playlist?list=RDCLAK5uy_khMA5iC_Hy79mWTECnc3-SNeJSt5SlZGg', #50
        'https://music.youtube.com/playlist?list=RDCLAK5uy_kx0d2-VPr69KAkIQOTVFq04hCBsJE9LaI', #132
        'https://music.youtube.com/playlist?list=RDCLAK5uy_klX-lb-R_tprKuViujvMW7iwlx_uP2c0k', #105
    ]
    lstURL_Classic = [
        'https://music.youtube.com/playlist?list=RDCLAK5uy_n9hGvSNdO2TpX8jJuiThvnfrfIi1qNRnY', #81
        'https://music.youtube.com/playlist?list=RDCLAK5uy_k83Q0BJ_yGLX2nTNKxOXb3BP3Pb7uMIN0', #71
        'https://music.youtube.com/playlist?list=RDCLAK5uy_migtKgYrl-JBY2xg7m6mqvJG-g4QsFyIs', #60
        'https://music.youtube.com/playlist?list=RDCLAK5uy_ldLj_raotpFCQGWiQ7L-Ag5GTbGOyjgRY', #77

    ]
    lstURL_EDM = [
        'https://music.youtube.com/playlist?list=RDCLAK5uy_lWfuEE9muOjxNxKnvVL_KZOhsMG7-FxMI', # 298
    ]
    dictURL = {
        'Jazz': lstURL_Jazz,
        'Hiphop': lstURL_Hiphop,
        'Rock': lstURL_Rock,
        'Classical': lstURL_Classic,
        'EDM': lstURL_EDM,
    }
    return dictURL

def getTimeString():
    return time.strftime('%Y%m%d%H%M')






















