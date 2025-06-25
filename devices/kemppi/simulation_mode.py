from core.config import UNIT_ID
import time

ROBOT_CONTROL_MODE_COIL = 7
ROBOT_READY_TO_WELD_COIL = 1
SIMULATION_ON_COIL = 6

def enable_simulation_mode(client):
    try:
        print("[NoArc] RobotControlMode → ON")
        client.write_coil(ROBOT_CONTROL_MODE_COIL, True, unit=UNIT_ID)
        time.sleep(0.1)

        print("[NoArc] RobotReadyToWeld → ON")
        client.write_coil(ROBOT_READY_TO_WELD_COIL, True, unit=UNIT_ID)
        time.sleep(0.1)

        print("[NoArc] SimulationOn → ON")
        client.write_coil(SIMULATION_ON_COIL, True, unit=UNIT_ID)
        time.sleep(0.1)

        print("[NoArc] 시뮬레이션 모드 정상 진입 완료")
    except Exception as e:
        print(f"[NoArc] 오류 발생: {e}")