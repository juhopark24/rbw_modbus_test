# devices/kemppi/memory_mode.py

from core.modbus_client import create_modbus_client
from core.config import UNIT_ID
import time
from typing import Optional, Callable

# Coil 주소 정의
COIL_CONTROL_MODE = 7        # RobotControlMode
COIL_READY = 1               # RobotReadyToWeld
COIL_START_WELDING = 0       # StartWelding

# Register 주소 정의
REG_COMMAND = 0              # 명령 전송용 (weld_on, weld_off)
REG_MEMORY_CHANNEL = 1       # Memory 채널 선택
REG_FEED_SPEED = 2           # FeedSpeed (10x 스케일)
REG_VOLTAGE = 3              # Voltage (10x 스케일)

# 명령어 값 정의
MEMORY_CHANNEL = 1           # 사용 채널 (기본값 1)
FEED_SPEED = 150             # 15.0 m/min → x10 = 150
VOLTAGE = 1                  # 0.1 V → x10 = 1
WELD_ON = 1159               # 용접 시작 명령
WELD_OFF = 130               # 용접 종료 명령

def send_memory_mode_welding(
    memory_channel: int = 1,
    weld_duration_sec: float = 1.0,
    feed_speed: Optional[int] = None,
    voltage: Optional[int] = None,
    monitor: bool = False,
    monitor_interval: float = 0.2,
    monitor_callback: Optional[Callable[[float, float, float, float], None]] = None,
):
    """Memory 채널 기반 용접 실행

    Parameters
    ----------
    memory_channel : int
        사용할 Kemppi Memory 채널 (1~99)
    weld_duration_sec : float
        용접 유지 시간(sec). 0 이하면 수동 종료 필요.
    feed_speed : int | None
        10x 스케일 송급속도 값. None 이면 레지스터를 건드리지 않음(메모리 채널값 사용).
    voltage : int | None
        10x 스케일 전압 fine-tune 값. None 이면 건드리지 않음.
    monitor : bool
        True 시 용접 동안 TAST/Voltage/Current 값을 주기적으로 출력.
    monitor_interval : float
        모니터링 간격(sec).
    monitor_callback : callable | None
        모니터링 데이터를 처리할 콜백 함수. 
        콜백 함수의 파라미터는 (time, TAST, Voltage, Current) 순서로 전달됨.
    """
    client = create_modbus_client()
    try:
        # 1) 제어권 & Ready
        client.write_coil(COIL_CONTROL_MODE, True, unit=UNIT_ID)
        time.sleep(0.1)
        client.write_coil(COIL_READY, True, unit=UNIT_ID)
        time.sleep(0.1)

        # 2) Memory 채널 선택
        client.write_register(REG_MEMORY_CHANNEL, memory_channel, unit=UNIT_ID)
        time.sleep(0.05)

        # 3) 선택적 파라미터 Override
        if feed_speed is not None:
            client.write_register(REG_FEED_SPEED, feed_speed, unit=UNIT_ID)
            time.sleep(0.05)
        if voltage is not None:
            client.write_register(REG_VOLTAGE, voltage, unit=UNIT_ID)
            time.sleep(0.05)

        # 4) Weld ON
        client.write_register(REG_COMMAND, WELD_ON, unit=UNIT_ID)

        # 5) 유지 & 모니터링 (동일 세션 사용 — Kemppi는 동시 1세션 제한)

        start_time = time.time()
        while True:
            if monitor:
                from devices.kemppi.status_reader import read_status_values
                try:
                    data = read_status_values(client)
                    current_time = time.time() - start_time
                    if monitor_callback:
                        monitor_callback(current_time, data['TAST'], data['Voltage'], data['Current'])
                    else:
                        print(f"[MON] t={current_time:.1f}s | TAST={data['TAST']} | V={data['Voltage']} | I={data['Current']}")
                except Exception as e:
                    print(f"[MON] read error: {e}")
                time.sleep(monitor_interval)
            if weld_duration_sec > 0 and (time.time() - start_time) >= weld_duration_sec:
                break
            time.sleep(monitor_interval if monitor else 0.05)

        # 6) Weld OFF
        client.write_register(REG_COMMAND, WELD_OFF, unit=UNIT_ID)

    finally:
        client.close()

# 기존 호환 함수명 유지
def send_memory_mode_welding_strict(weld_duration_sec: float = 2.0):
    """Backward-compat wrapper (strict = fixed channel/params)"""
    send_memory_mode_welding(
        memory_channel=MEMORY_CHANNEL,
        weld_duration_sec=weld_duration_sec,
        feed_speed=FEED_SPEED,
        voltage=VOLTAGE,
    )