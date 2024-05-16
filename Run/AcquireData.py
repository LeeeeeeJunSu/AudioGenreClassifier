'''
Implement the Data Crawling
1. 유튜브 뮤직의 장르 별 플레이 리스트를 통해 음원을 RootFolder/Data/All/장르명/곡명.wav 형식으로저장
2. 각 장르 별 200곡 씩 저장되도록 파일 삭제
3. 150곡은 RootFolder/Data/Train/장르명/곡명.wav 저장
4. 50곡은 RootFolder/Data/Validate/장르명/곡명.wav 저장
5. RootFolder/Data/All 폴더 삭제
'''

import os
import yt_dlp
import Define

# URL 생성
lstURL_Jazz = [
]
lstURL_Hiphop = [
]
lstURL_Rock = [
]
lstURL_Classic = [
]
lstURL_EDM = [
]
dictURL = {
    'Jazz': lstURL_Jazz,
    'Hiphop': lstURL_Hiphop,
    'Rock': lstURL_Rock,
    'Classical': lstURL_Classic,
    'EDM': lstURL_EDM
}

# 전체 음원 다운로드
for genre, lstURL in dictURL.items():
    # 폴더 체크 및 생성
    strFolder = Define.PATH_ALL_DATA + genre
    if not os.path.exists(strFolder):
        os.makedirs(strFolder)
    # yt-dlp 설정
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'wav'}],
        'outtmpl': strFolder + '/%(title)s.%(ext)s'
    }
    # 음원 다운로드
    for i, url in enumerate(lstURL):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

# 장르별 200곡이 넘는 경우 200곡이 되도록 파일 삭제
for genre in dictURL.keys():
    strFolder = Define.PATH_ALL_DATA + genre
    lstFiles = os.listdir(strFolder)
    if len(lstFiles) > 200:
        for i in range(200, len(lstFiles)):
            os.remove(f'{strFolder}/{lstFiles[i]}')

# Train, Validate 데이터 분리
for genre in dictURL.keys():
    strFolder = Define.PATH_ALL_DATA + genre
    lstFiles = os.listdir(strFolder)
    for i in range(150):
        os.rename(f'{strFolder}/{lstFiles[i]}', Define.PATH_TRAIN_DATA + f'{genre}/{lstFiles[i]}')
    for i in range(150, 200):
        os.rename(f'{strFolder}/{lstFiles[i]}', Define.PATH_VALIDATE_DATA + f'{genre}/{lstFiles[i]}')
            
# All 폴더 삭제
for genre in dictURL.keys():
    strFolder = Define.PATH_ALL_DATA + genre
    os.rmdir(strFolder)