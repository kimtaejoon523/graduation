import smbus2
import time

# I2C 버스 초기화
bus = smbus2.SMBus(1)
address = 0x48  # ADC I2C 주소 (예: ADS1115)

# 데이터 읽기 함수
def read_adc(channel):
    # I2C를 통해 ADC에서 데이터 읽기 (예시)
    bus.write_byte(address, channel)
    time.sleep(0.1)
    data = bus.read_i2c_block_data(address, 0, 2)
    value = data[0] * 256 + data[1]
    if value > 32767:
        value -= 65536
    return value

# 샘플 데이터 수집
sampling_rate = 1000  # Hz
duration = 3.0  # seconds
num_samples = int(sampling_rate * duration)
data = []

start_time = time.time()
for _ in range(num_samples):
    adc_value = read_adc(0)  # 채널 0에서 데이터 읽기
    data.append(adc_value)
    while time.time() - start_time < _ / sampling_rate:
        pass  # 샘플링 속도에 맞추기 위해 대기

# 데이터를 파일에 저장 (원하는 경우)
with open('adc_data.txt', 'w') as f:
    for value in data:
        f.write(f"{value}\n")

print("Data collection complete.")

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
