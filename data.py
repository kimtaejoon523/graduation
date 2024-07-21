import smbus2
import time

# I2C 버스 초기화
bus = smbus2.SMBus(1)
address = 0x48  # ADC I2C 주소 (예: ADS1115)

# ADS1115 레지스터 주소
CONFIG_REGISTER = 0x01
CONVERSION_REGISTER = 0x00

# CONFIG_REGISTER 설정 값 (예: 채널 0, ±4.096V 범위, 860 SPS)
config = 0x8483  # 채널 0, ±4.096V 범위, 860 SPS

# CONFIG_REGISTER에 설정 값 쓰기
config_high = (config >> 8) & 0xFF
config_low = config & 0xFF
bus.write_i2c_block_data(address, CONFIG_REGISTER, [config_high, config_low])

# 데이터 읽기 함수
def read_adc():
    # CONVERSION_REGISTER에서 2바이트 데이터 읽기
    data = bus.read_i2c_block_data(address, CONVERSION_REGISTER, 2)
    # 읽은 데이터를 16비트 값으로 변환
    value = data[0] * 256 + data[1]
    # 음수 값을 처리
    if value > 32767:
        value -= 65536
    # ADC 값을 실제 전압으로 변환
    voltage = value * 4.096 / 32768.0  # ±4.096V 범위
    return voltage

# 샘플 데이터 수집
sampling_rate = 1000  # Hz
duration = 3.0  # seconds
num_samples = int(sampling_rate * duration)
data = []

start_time = time.time()
for _ in range(num_samples):
    adc_value = read_adc()  # 데이터 읽기
    # 2V에서 5V 사이의 값을 측정하기 위해 필터링
    if 2.0 <= adc_value <= 5.0:
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
import time
import os

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
plt.savefig('~/termP/train/0/0.png')  # 파일 이름과 확장자를 원하는 대로 변경 가능
plt.show()

# 2초 대기 후 프로그램 종료
time.sleep(2)
os._exit(0)
