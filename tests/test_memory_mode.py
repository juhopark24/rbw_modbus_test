import sys
import os
import time
import logging
from datetime import datetime

# 로그 디렉토리 생성
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)

# 로그 파일명 설정 (월_일_시_분_초.txt)
timestamp = datetime.now().strftime('%Y%m%d_%H%M_%S')
log_filename = f"{timestamp}.txt"
log_path = os.path.join(log_dir, log_filename)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler(log_path, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def print_and_log(message):
    """콘솔 출력과 로그 파일에 동시에 기록"""
    logger.info(message)

# 프로젝트 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from devices.kemppi.memory_mode import send_memory_mode_welding
from devices.kemppi.status_reader import read_status_values
from core.modbus_client import create_modbus_client

def monitor_callback(timestamp, tast, voltage, current):
    """모니터링 콜백 함수"""
    message = f"[MON] t={timestamp:.1f}s | TAST={tast} | V={voltage} | I={current}"
    print_and_log(message)

if __name__ == "__main__":
    try:
        print_and_log(f"[TEST] 로그 파일: {os.path.abspath(log_path)}")
        print_and_log(f"[TEST] Memory 모드 (채널: {memory_channel})")
        
        # 모니터링 콜백 함수 전달
        send_memory_mode_welding(
            memory_channel=11, 
            weld_duration_sec=6.0, 
            monitor=True,
            monitor_interval=0.005,
            monitor_callback=monitor_callback
        )

        print_and_log("[TEST] 용접 직후 상태값 읽기")
        client = create_modbus_client()
        try:
            data = read_status_values(client)
            print_and_log(f"[STATUS] TAST={data['TAST']}, Voltage={data['Voltage']}, Current={data['Current']}")
        except Exception as e:
            print_and_log(f"[STATUS] 오류: {e}")
        finally:
            client.close()
            
    except Exception as e:
        print_and_log(f"[ERROR] 테스트 중 오류 발생: {e}")
    
    print_and_log("[TEST] 테스트 완료")