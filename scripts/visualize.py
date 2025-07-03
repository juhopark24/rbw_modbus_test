# 최근파일 python scripts/visualize.py
# 특정파일 python scripts/visualize.py logs/20250703_1040_18.txt


import os
import re
import sys
import matplotlib.pyplot as plt
from pathlib import Path

def parse_log_file(filepath):
    """Parse log file and extract TAST, Voltage, Current data"""
    data = []
    time_offset = None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            # [MON] t=1.2s | TAST=1766 | V=278 | I=134
            match = re.search(r't=([\d.]+)s.*TAST=(\d+).*V=(\d+).*I=(\d+)', line)
            if match:
                t = float(match.group(1))
                tast = int(match.group(2))
                volt = int(match.group(3))
                curr = int(match.group(4))
                
                if time_offset is None:
                    time_offset = t
                
                # Normalize time to start from 0
                normalized_t = t - time_offset
                data.append((normalized_t, tast, volt, curr))
    
    return data

def plot_data(data, title=None):
    """Plot TAST, Voltage, and Current data"""
    if not data:
        print("No data to plot")
        return
    
    # Unpack data
    times, tast, volt, curr = zip(*data)
    
    # Create figure and axis
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    
    # Plot TAST
    ax1.plot(times, tast, 'b-', label="TAST")
    ax1.set_ylabel('TAST')
    ax1.grid(True)
    ax1.legend()
    
    # Plot Voltage
    ax2.plot(times, volt, 'r-', label="Voltage (0.1V)")
    ax2.set_ylabel('Voltage (0.1V)')
    ax2.grid(True)
    ax2.legend()
    
    # Plot Current
    ax3.plot(times, curr, 'g-', label="Current (0.1A)")
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Current (0.1A)')
    ax3.grid(True)
    ax3.legend()
    
    if title:
        plt.suptitle(title, y=1.02)
    
    plt.tight_layout()
    plt.show()

def main():
    # Get log file path from command line or use default
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    else:
        # Find the most recent log file if none specified
        log_dir = Path(__file__).parent.parent / 'logs'
        log_files = sorted(log_dir.glob('*.txt'), key=os.path.getmtime, reverse=True)
        if not log_files:
            print("No log files found in logs directory")
            return
        log_file = log_files[0]
    
    # Check if file exists
    if not os.path.exists(log_file):
        print(f"File not found: {log_file}")
        return
    
    print(f"Processing file: {log_file}")
    
    # Parse and plot data
    data = parse_log_file(log_file)
    if data:
        plot_data(data, title=f"Welding Data - {os.path.basename(log_file)}")
    else:
        print("No valid data found in the log file")

if __name__ == "__main__":
    main()


# import matplotlib.pyplot as plt

# # 시계열 데이터 (t, TAST, Voltage, Current)
# data = [
#     (0.0, 0, 0, 0),
#     (0.2, 0, 0, 0),
#     (0.4, 1606, 80, 62),
#     (0.6, 1620, 80, 62),
#     (0.8, 2196, 244, 110),
#     (1.0, 3277, 227, 138),
#     (1.2, 1766, 278, 134),
#     (1.4, 3729, 233, 65),
#     (1.7, 3457, 233, 65),
#     (1.9, 3520, 148, 97),
#     (2.1, 3728, 194, 52),
#     (2.3, 3606, 151, 90),
#     (2.5, 3858, 178, 65),
#     (2.7, 3654, 145, 94),
#     (2.9, 3504, 176, 66),
#     (3.1, 3879, 150, 93),
# ]

# # 리스트 언팩
# xs, tast, volt, curr = zip(*data)

# plt.figure(figsize=(8, 4))
# plt.plot(xs, tast, label="TAST")
# plt.plot(xs, volt, label="Voltage (0.1V)")
# plt.plot(xs, curr, label="Current (0.1A)")

# plt.xlabel("Time (s)")
# plt.ylabel("Raw value")
# plt.title("Kemppi sample status data")
# plt.legend()
# plt.tight_layout()
# plt.show()
