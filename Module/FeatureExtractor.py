#Implement Feature Extractor
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Root Folder를 Python Path에 추가
 
import librosa
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import Module.Define as Define

class MFCC:
    def __init__(self, n_mfcc = 13, n_fft = 2048, segment_length = 6):
        '''
        MFCC 클래스 초기화
        Parameters:
            n_mfcc : 추출할 MFCC 계수의 수 (기본값: 13)
            n_fft : FFT 컴포넌트의 수 (기본값: 2048)
            segment_length : 분리할 길이 (초)
        '''
        self.n_mfcc = n_mfcc
        self.n_fft = n_fft
        self.segment_length = segment_length

    def extract(self, audio):
        '''
        Func: 
            MFCC 특징 추출 메소드
        Parameters:
            audio : 오디오 신호
        Returns:
            각 Segment 별로 추출한 MFCC 리스트
        Description
            audio를 Segment 단위로 분리 후 MFCC 추출하여 리스트로 반환
            MFCC 추출에는 librosa 라이브러리 사용
            MFCC 추출에 사용되는 파라미터는 생성자를 통해 결정
            Segment 분리 시 남는 부분은 제거
        '''
        segment_samples = int(self.segment_length * Define.SAMPLING_RATE)
        mfcc_list = []
        for start in range(0, len(audio), segment_samples):
            end = start + segment_samples
            if end > len(audio):
                continue
            segment = audio[start:end]
            if len(segment) < self.n_fft:
                continue
            mfcc = librosa.feature.mfcc(y=segment, sr=Define.SAMPLING_RATE, n_mfcc=self.n_mfcc, hop_length=int(self.n_fft / 4), n_fft=self.n_fft)
            mfcc_list.append(mfcc.T)
            
            '''
            # show mfcc
            plt.figure(figsize=(10, 4))
            librosa.display.specshow(mfcc, x_axis='time', sr=Define.SAMPLING_RATE, hop_length=int(self.n_fft / 4))
            plt.colorbar()
            plt.title('MFCC')
            plt.tight_layout()
            plt.show()
            '''
        return mfcc_list

class OSC:
    def __init__(self, window_length=1024, overlap=512, alpha=0.2):
        '''
        OSC 클래스 초기화
        Parameters:
            window_length : STFT 윈도우 길이 (기본값: 1024)
            overlap : STFT 오버랩 길이 (기본값: 512)
            alpha : Peak, Valley 계산에 사용되는 비율 (기본값: 0.2)
        '''
        self.window_length = window_length
        self.overlap = overlap
        self.alpha = alpha

    def extract(self, data):
        '''
        Func: 
            OSC 특징 추출 메소드
        Parameters:
            audio : 오디오 신호
        Returns:
            음원 내 주파수 밴드 별 Peak, Valley의 대비 리스트
        '''
        Segment_size = self.window_length * 256  # Define the segment size as 256 times the window length if not specified
        step_size = self.window_length - self.overlap
        num_segments = int(np.ceil((len(data) - self.overlap) / Segment_size))  # Calculate number of segments based on the Segment_size
        window = signal.windows.hann(self.window_length, sym=False)
        frequencies = np.fft.fftfreq(self.window_length, 1 / Define.SAMPLING_RATE)[:self.window_length // 2]
        bands = [(0, 200), (200, 400), (400, 800), (800, 1600), (1600, 3200), (3200, 6400)]
        spectral_data_list = []  # List to store spectral data for each segment
        for i in range(num_segments):
            start = i * Segment_size  # Use Segment_size to define the start of each segment
            end = start + Segment_size  # Define the end of each segment using Segment_size
            if end > len(data):
                segment = np.zeros(Segment_size)  # If the end extends beyond the data, pad with zeros
                segment[:len(data) - start] = data[start:len(data)]
            else:
                segment = data[start:end]
            # Process segment using multiple windows if Segment_size > window_length
            segment_spectral_data = []
            for j in range(0, Segment_size - self.window_length + 1, step_size):
                windowed_segment = segment[j:j + self.window_length] * window
                Zxx = np.fft.fft(windowed_segment, n=self.window_length)[:self.window_length // 2]
                abs_Zxx = np.abs(Zxx)
                band_data = []
                for low, high in bands:
                    band_mask = (frequencies >= low) & (frequencies < high)
                    if np.any(band_mask):
                        band_data.append(np.mean(abs_Zxx[band_mask]))
                segment_spectral_data.append(band_data)
            # Optionally, average the spectral data from all windows within the segment
            averaged_band_data = np.mean(segment_spectral_data, axis=0)
            spectral_data_list.append(averaged_band_data.tolist())

        return spectral_data_list, bands
    
    def calculate_peak_valley(self, spectral_data):
        '''
        Func: 
            Peak, Valley 계산 메소드 (Class 내부에서만 사용)
        Parameters:
            spectral_data : STFT 데이터
            alpha : Peak, Valley 계산에 사용되는 비율 (기본값: 0.2)
        Returns:
            주파수 밴드 별 Peak, Valley 리스트
        '''
        # Determine the number of points in each band (assuming uniform distribution)
        N_b = spectral_data.shape[1]
        alpha_N_b = int(self.alpha * N_b)  # Number of points to average over
        peaks = []
        valleys = []
        for band_data in spectral_data:
            # Sort the band data in descending order
            sorted_band_data = np.sort(band_data)[::-1]  # This sorts the array in ascending order first, then reverses it
            # Calculate peak: average of the first alpha_N_b points
            peak_avg = np.mean(sorted_band_data[:alpha_N_b])
            peak_dB = np.log(peak_avg)  # Convert to dB using natural logarithm
            # Calculate valley: average of the last alpha_N_b points
            valley_avg = np.mean(sorted_band_data[-alpha_N_b:])
            valley_dB = np.log(valley_avg)  # Convert to dB using natural logarithm
            peaks.append(peak_dB)
            valleys.append(valley_dB)
        return np.array(peaks), np.array(valleys)
    
    def calculate_spectral_contrast(self, peaks, valleys):
        '''
        Func: 
            Spectral Contrast 계산 메소드 (Class 내부에서만 사용)
        Parameters:
            peaks : Peak 리스트
            valleys : Valley 리스트
        Returns:
            Spectral Contrast 리스트
        '''
        return peaks - valleys