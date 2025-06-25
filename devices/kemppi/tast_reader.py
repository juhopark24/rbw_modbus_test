from core.config import UNIT_ID

TAST_REGISTER = 1  # Word 1번이 TAST로 문서에 명시됨

def read_tast_value(client):
    result = client.read_holding_registers(address=TAST_REGISTER, count=1, unit=UNIT_ID)
    if result.isError():
        raise Exception(f"Modbus read error: {result}")
    return result.registers[0]

# # devices/kemppi/tast_reader.py

# from core.modbus_client import create_modbus_client
# from core.config import UNIT_ID, LOG_PATH
# from devices.kemppi.modbus_map import TAST_REGISTER
# from datetime import datetime

# def read_tast_value(client):
#     client = create_modbus_client()
#     try:
#         result = client.read_holding_registers(address=TAST_REGISTER, count=1, unit=UNIT_ID)
#         if result.isError():
#             raise Exception(f"Modbus Error: {result}")
#         tast = result.registers[0]
#         return tast
#     finally:
#         client.close()

# def log_tast_value():
#     tast_value = read_tast_value()
#     now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     with open(LOG_PATH, "a") as f:
#         f.write(f"{now}, TAST={tast_value}\n")
#     print(f"[{now}] TAST: {tast_value}")
