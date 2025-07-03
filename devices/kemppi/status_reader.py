# devices/kemppi/status_reader.py

from core.config import UNIT_ID

#  상태값 주소 (Input Register)
TAST_REGISTER       = 1   # Word 1
VOLT_REGISTER       = 3   # Word 3
CURR_REGISTER       = 4   # Word 4
ARC_VOLT_REGISTER   = 8   # Word 8: WeldingArcVoltage (set voltage)
WATCHDOG_REGISTER   = 9   # Word 9: WatchdogTimeoutValue
PROCESS_REGISTER    = 10  # Word 10: WeldingProcess
TRAVELSPD_REGISTER  = 11  # Word 11: TravelSpeed

def read_status_values(client):
    rr = client.read_input_registers(address=TAST_REGISTER, count=11, unit=UNIT_ID)
    if rr.isError():
        raise Exception(rr)
    regs = rr.registers
    return {
        "TAST":    regs[0],           # Word 1
        "Voltage": regs[2],           # Word 3 (measured)
        "Current": regs[3],           # Word 4
        "ArcVoltage": regs[7],        # Word 8 (set/arc voltage)
        "Watchdog": regs[8],          # Word 9
        "Process":  regs[9],          # Word 10
        "TravelSpd": regs[10],        # Word 11
    }