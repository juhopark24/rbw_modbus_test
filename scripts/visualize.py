import matplotlib.pyplot as plt

# 시계열 데이터 (t, TAST, Voltage, Current)
data = [
    (0.0, 0, 0, 0),
    (0.2, 0, 0, 0),
    (0.4, 1606, 80, 62),
    (0.6, 1620, 80, 62),
    (0.8, 2196, 244, 110),
    (1.0, 3277, 227, 138),
    (1.2, 1766, 278, 134),
    (1.4, 3729, 233, 65),
    (1.7, 3457, 233, 65),
    (1.9, 3520, 148, 97),
    (2.1, 3728, 194, 52),
    (2.3, 3606, 151, 90),
    (2.5, 3858, 178, 65),
    (2.7, 3654, 145, 94),
    (2.9, 3504, 176, 66),
    (3.1, 3879, 150, 93),
]

# 리스트 언팩
xs, tast, volt, curr = zip(*data)

plt.figure(figsize=(8, 4))
plt.plot(xs, tast, label="TAST")
plt.plot(xs, volt, label="Voltage (0.1V)")
plt.plot(xs, curr, label="Current (0.1A)")

plt.xlabel("Time (s)")
plt.ylabel("Raw value")
plt.title("Kemppi sample status data")
plt.legend()
plt.tight_layout()
plt.show()
