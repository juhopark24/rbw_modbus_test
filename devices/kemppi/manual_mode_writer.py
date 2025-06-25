# devices/kemppi/manual_mode_writer.py

from core.modbus_client import create_modbus_client
from core.config import UNIT_ID
import time

# Manual Mode용 주소 정의
FEED_SPEED_REGISTER = 2     # 와이어 송급 속도
VOLTAGE_REGISTER = 3        # 전압
START_REGISTER = 5          # start 명령 주소 (WSL 분석 기반)
START_COMMAND = 1159        # WSL에서 사용된 weld_on 상수
STOP_COMMAND = 0            # weld_off는 대부분 0으로 종료 의미

def send_manual_weld_parameters(feed_speed: int, voltage: int, duration_sec: float = 3.0):
    """
    Manual Mode에서 설정값 전송 후 용접 시작 → 유지 → 종료
    :param feed_speed: 와이어 속도 (정수, 단위 보정 포함)
    :param voltage: 전압 (정수, 단위 보정 포함)
    :param duration_sec: 유지 시간 (초)
    """
    client = create_modbus_client()
    try:
        print(f"[Manual] Feed Speed → {feed_speed}")
        client.write_register(FEED_SPEED_REGISTER, feed_speed, unit=UNIT_ID)
        time.sleep(0.1)

        print(f"[Manual] Voltage → {voltage}")
        client.write_register(VOLTAGE_REGISTER, voltage, unit=UNIT_ID)
        time.sleep(0.1)

        print(f"[Manual] Start command → {START_COMMAND} (address={START_REGISTER})")
        client.write_register(START_REGISTER, START_COMMAND, unit=UNIT_ID)
        time.sleep(duration_sec)

        print("[Manual] Stop command → 0")
        client.write_register(START_REGISTER, STOP_COMMAND, unit=UNIT_ID)
    except Exception as e:
        print(f"[Manual] 오류 발생: {e}")
    finally:
        client.close()