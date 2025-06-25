# devices/kemppi/status_reader.py

from core.config import UNIT_ID

# 상태값 주소 정의
TAST_REGISTER = 1
VOLTAGE_REGISTER = 3
CURRENT_REGISTER = 4

def read_status_values(client):
    """TAST, 전압, 전류를 한 번에 읽어서 반환 (dict)."""
    result = client.read_holding_registers(address=TAST_REGISTER, count=5, unit=UNIT_ID)
    if result.isError():
        raise Exception(f"Modbus read error: {result}")
    regs = result.registers
    return {
        "TAST": regs[0],
        "Voltage": regs[2],  # addr=3
        "Current": regs[3],  # addr=4
    }
