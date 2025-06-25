from pymodbus.client import ModbusTcpClient
from core.config import WELDER_IP, WELDER_PORT

def create_modbus_client():
    return ModbusTcpClient(
        host=WELDER_IP,
        port=WELDER_PORT,
        source_address=("192.168.0.110", 0),  # 반드시 LAN IP로 설정
        timeout=3
    )