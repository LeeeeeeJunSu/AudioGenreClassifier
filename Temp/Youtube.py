# yt-dlp를 사용해서 Youtube Music Top 100 음원 추출
# top 100 url : https://music.youtube.com/playlist?list=PL4fGSI1pDJn6jXS_Tv_N9B8Z0HTRVJE0m&si=oS_NV6vs0ZHDAwJG
import yt_dlp

url = "https://music.youtube.com/playlist?list=PL4fGSI1pDJn6jXS_Tv_N9B8Z0HTRVJE0m&si=oS_NV6vs0ZHDAwJG"
ydl_opts = {'format': 'm4a/bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'wav',}]}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
