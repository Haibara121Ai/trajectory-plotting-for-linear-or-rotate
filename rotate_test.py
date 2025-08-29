import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

x_data = []
y_data = []
theta_data = []

log_files = [
    ("1_trial/clw_to_240.txt", "To 120°"),
    ("1_trial/clw_to_120.txt", "To 240°"),
    ("1_trial/clw_to_0.txt", "To 360°")
]

pattern = re.compile(
    r"current_theta:\s*(-?\d+\.?\d*),\s*current_x:\s*(-?\d+\.?\d*),\s*current_y\s*=\s*(-?\d+\.?\d*)"
)


plt.figure(figsize=(10, 10))

for path, label in log_files:
    with open(path, "r") as f:
        lines = f.readlines()

    data = []
    lines_combined = []
    current_x = current_y = current_theta = None

    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            combined_line = lines[i].strip() + lines[i + 1].strip()
            lines_combined.append(combined_line)
        else:
            lines_combined.append(lines[i].strip())

    for line in lines_combined:
        match = pattern.search(line)
        if match:
            current_theta = float(match.group(1))
            current_x = float(match.group(2))
            current_y = float(match.group(3))

        if current_x is not None and current_y is not None and current_theta is not None:
            current_x = round(current_x, 3)
            current_y = round(current_y, 3)
            x_data.append(current_x - 101000)
            y_data.append(current_y - 101000)
            theta_data.append(current_theta)
            data.append((current_x-101000, current_y-101000, current_theta))
            current_x = current_y = current_theta = None

    df = pd.DataFrame(data, columns=["x", "y", "theta"])

    # 画轨迹线
    plt.plot(df["x"], df["y"], marker='.', linestyle='-', markersize = 2, label=label)

    # 添加方向箭头（每隔几个点画一个）
    skip = max(len(df) // 20, 1)
    for i in range(0, len(df), skip):
        dx = 1 * np.cos(df["theta"][i]*np.pi/180.00)
        dy = 1 * np.sin(df["theta"][i]*np.pi/180.00)
        print(f"theta:{df["theta"][i]}")
        plt.arrow(df["x"][i], df["y"][i], dx, dy, head_width=0.1, color='r', alpha=0.6)

# plt.axis('equal')
# plt.xlim(0, 30)
# plt.ylim(-10, 30)

# plt.xticks(np.arange(-30, 31, 5))
# plt.yticks(np.arange(-30, 31, 5))
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.title("Clockwise Rotation Test")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
