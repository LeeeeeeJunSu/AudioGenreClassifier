#Implement Feature Extractor
 
import librosa
import numpy as np

class MFCC:
    '''
    MFCC 클래스 초기화
    Parameters:
        n_mfcc : 추출할 MFCC 계수의 수 (기본값: 13)
        n_fft : FFT 컴포넌트의 수 (기본값: 2048)
        segment_length : 분리할 길이 (초)
    '''
    def __init__(self, n_mfcc = 13, n_fft = 2048, segment_length = 6):
        self.n_mfcc = n_mfcc
        self.n_fft = n_fft
        self.segment_length = segment_length

    '''
    Func: 
        MFCC 특징 추출 메소드
    Parameters:
        audio : 오디오 신호
        sampling_rate : 샘플링 레이트
    Returns:
        각 Segment 별로 추출한 MFCC 리스트
    Description
        audio를 Segment 단위로 분리 후 MFCC 추출하여 리스트로 반환
        MFCC 추출에는 librosa 라이브러리 사용
        MFCC 추출에 사용되는 파라미터는 생성자를 통해 결정
        Segment 분리 시 남는 부분은 제거
    '''
    def extract(self, audio, sampling_rate):
        norm_audio = audio.astype(float) / np.iinfo(audio.dtype).max
        segment_samples = int(self.segment_length * sampling_rate)
        mfcc_list = []
        for start in range(0, len(norm_audio), segment_samples):
            end = start + segment_samples
            if end > len(norm_audio):
                continue
            segment = norm_audio[start:end]
            if len(segment) < self.n_fft:
                continue
            mfcc = librosa.feature.mfcc(y=segment, sr=sampling_rate, n_mfcc=self.n_mfcc, hop_length=int(self.n_fft / 4), n_fft=self.n_fft)
            mfcc_list.append(mfcc.T)
        return mfcc_list
