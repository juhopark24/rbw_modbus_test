import threading
import time
from core.config import UNIT_ID

WATCHDOG_REGISTER = 8
INTERVAL_SEC = 0.5

def _toggle_watchdog(client):
    toggle = 1
    while True:
        try:
            result = client.write_register(address=WATCHDOG_REGISTER, value=toggle, unit=UNIT_ID)
            if result.isError():
                print(f"[Watchdog] Modbus write error: {result}")
            else:
                print(f"[Watchdog] Sent value: {toggle}")
        except Exception as e:
            print(f"[Watchdog] Exception: {e}")
        toggle = 1 - toggle
        time.sleep(INTERVAL_SEC)

def start_watchdog_loop(client):
    thread = threading.Thread(target=_toggle_watchdog, args=(client,), daemon=True)
    thread.start()
    return thread