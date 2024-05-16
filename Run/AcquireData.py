'''
Implement the Data Crawling
1. 유튜브 뮤직의 장르 별 플레이 리스트를 통해 음원을 RootFolder/Data/ALL/장르명/곡명.wav 형식으로저장
2. 각 장르 별 200곡 씩 저장되도록 파일 삭제
3. 150곡은 RootFolder/Data/Train/장르명/곡명.wav 저장
4. 50곡은 RootFolder/Data/Validate/장르명/곡명.wav 저장
5. RootFolder/Data/ALL 폴더 삭제
'''




import yt_dlp

ydl_opts = {'format': 'm4a/bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'wav',}]}


url = "https://music.youtube.com/playlist?list=PL4fGSI1pDJn6jXS_Tv_N9B8Z0HTRVJE0m&si=oS_NV6vs0ZHDAwJG"
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
