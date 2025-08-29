import pandas as pd
import matplotlib.pyplot as plt
import re

# 初始化统计变量
diff_sum = 0
left_sum = 0
right_sum = 0

log_files = [
    ("first_trial/velocity_diff_3.txt", "Clw To 240°"),
    ("first_trial/velocity_diff_4.txt", "Clw To 120°"),
    ("first_trial/velocity_diff_5.txt", "Clw To 0°"),
]

pattern = re.compile(
    r"left_actual_velocity\s*=\s*(-?\d+\.?\d*),\s*right_actual_velocity\s*=\s*(-?\d+\.?\d*)"
)


n_files = len(log_files)
fig, axes = plt.subplots(n_files, 1, figsize=(12, 4 * n_files), sharex=False)

if n_files == 1:
    axes = [axes]

for idx, (path, label) in enumerate(log_files):
    with open(path, "r") as f:
        lines = f.readlines()

    lines_combined = []
    left_vals = []
    right_vals = []
    sum_vals = []
    v_ant = []
    w_ant = []
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            combined_line = lines[i].strip() + lines[i + 1].strip()
        else:
            combined_line = lines[i].strip()
        lines_combined.append(combined_line)

    for line in lines_combined:
        match = pattern.search(line)
        if match:
            left = float(match.group(1))
            right = float(match.group(2))
            left_vals.append(abs(left))
            right_vals.append(abs(right))
            sum_vals.append(left + right)
            v_ant.append((left+right)/2)
            w_ant.append((right-left)/480)  #逆时针转为正
            diff_sum += left + right
            left_sum += left
            right_sum += right


    ax = axes[idx]
    ax.plot(v_ant, label='Linear Velocity(mm/s)')
    # ax.plot(sum_vals, label='Diff (L+R)')
    ax_right = ax.twinx()
    ax_right.plot(w_ant, label='Angular Velocity(rad/s)', color='tab:red')
    ax_right.set_ylabel("angularvelocity", color='tab:red')
    ax_right.tick_params(axis='y', labelcolor='tab:red')
    ax.set_title(f"Linear and Angular Velocity - {label}")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Velocity")
    ax.grid(True)
    ax.legend()
    # info_text = f"diff_sum: {diff_sum:.2f}\nleft_sum: {left_sum:.2f}\nright_sum: {right_sum:.2f}"
    # ax.text(
    #     0.95, 0.95,
    #     info_text,
    #     ha='right',
    #     va='top',
    #     fontsize=10,
    #     bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", edgecolor="gray")
    # )

    diff_sum = 0
    left_sum = 0
    right_sum = 0




plt.tight_layout(rect=[0, 0, 0.9, 1])
plt.show()
