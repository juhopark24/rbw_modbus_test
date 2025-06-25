import sys, os, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.modbus_client import create_modbus_client
from devices.kemppi.watchdog_task import start_watchdog_loop
from devices.kemppi.simulation_mode import enable_simulation_mode
from devices.kemppi.tast_reader import read_tast_value

if __name__ == "__main__":
    client = create_modbus_client()

    print("[TEST] Watchdog 루프 시작")
    start_watchdog_loop(client)
    time.sleep(1)

    print("[TEST] NoArc 시뮬레이션 모드 진입")
    enable_simulation_mode(client)
    time.sleep(0.5)

    print("[TEST] TAST 값 읽기")
    try:
        tast = read_tast_value(client)
        print(f"[TAST] 수신된 값: {tast}")
    except Exception as e:
        print(f"[TAST] 오류: {e}")
    finally:
        client.close()