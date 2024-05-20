'''
Implement the Data Crawling
1. 유튜브 뮤직의 장르 별 플레이 리스트를 통해 음원을 RootFolder/Data/All/장르명/곡명.wav 형식으로저장
2. 각 장르 별 200곡 씩 저장되도록 파일 삭제
3. 150곡은 RootFolder/Data/Train/장르명/곡명.wav 저장
4. 50곡은 RootFolder/Data/Validate/장르명/곡명.wav 저장
5. RootFolder/Data/All 폴더 삭제
'''
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Root Folder를 Python Path에 추가

import yt_dlp
import Define

# URL 생성
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
    # 폴더 체크 및 생성
    strFolder = Define.PATH_TRAIN_DATA + genre
    if not os.path.exists(strFolder):
        os.makedirs(strFolder)
    strFolder = Define.PATH_VALIDATE_DATA + genre
    if not os.path.exists(strFolder):
        os.makedirs(strFolder)
    # 파일 이동
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