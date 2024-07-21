import smbus2
import time

bus = smbus2.SMBus(1)
address = 0x48  # ADC I2C 주소 (예: ADS1115)


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
    data = bus.read_i2c_block_data(address, CONVERSION_REGISTER, 2)
    value = data[0] * 256 + data[1]
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
