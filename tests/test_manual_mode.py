# tests/test_manual_mode.py

import sys, os, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.modbus_client import create_modbus_client
from devices.kemppi.watchdog_task import start_watchdog_loop
from devices.kemppi.simulation_mode import enable_simulation_mode
from devices.kemppi.manual_mode_writer import send_manual_weld_parameters
from devices.kemppi.status_reader import read_status_values

if __name__ == "__main__":
    client = create_modbus_client()

    print("[TEST] Watchdog 루프 시작")
    start_watchdog_loop(client)
    time.sleep(1)

    print("[TEST] NoArc 시뮬레이션 모드 진입")
    enable_simulation_mode(client)
    time.sleep(0.5)

    print("[TEST] Manual 모드로 용접 시작 → 유지 → 종료")
    send_manual_weld_parameters(feed_speed=70, voltage=80, duration_sec=3)

    print("[TEST] 용접 직후 상태값 읽기")
    try:
        data = read_status_values(client)
        print(f"[STATUS] TAST={data['TAST']}, Voltage={data['Voltage']}, Current={data['Current']}")
    except Exception as e:
        print(f"[STATUS] 오류: {e}")
    finally:
        client.close()