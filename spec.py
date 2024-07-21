import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram

# 파일에서 데이터 읽기
data = []
with open('adc_data.txt', 'r') as f:
    for line in f:
        data.append(int(line.strip()))

# 데이터를 numpy 배열로 변환
digital_signal = np.array(data)

# 샘플링 속도 설정
sampling_rate = 1000  # Hz

# 단시간 푸리에 변환(STFT) 수행
frequencies, times, Sxx = spectrogram(digital_signal, fs=sampling_rate)

# 시간-주파수 영역 신호 시각화 및 저장
plt.figure(figsize=(12, 8))
plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='gouraud')
plt.title("Spectrogram of the Digitized Signal")
plt.xlabel("Time [s]")
plt.ylabel("Frequency [Hz]")
plt.colorbar(label='Intensity [dB]')

plt.ylim(0, 500)  # 필요한 경우 주파수 범위 조정

# 스펙트로그램을 이미지 파일로 저장
plt.savefig('spectrogram.png')  # 파일 이름과 확장자를 원하는 대로 변경 가능
plt.show()
