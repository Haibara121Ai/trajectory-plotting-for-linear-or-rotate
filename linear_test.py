import matplotlib.pyplot as plt
import re
import numpy as np


def file_name(file_num, linear_way):
    if linear_way == "forward":
        log_files = [("".join(["linear_trial",f"/{file_num}_trial","forward.md"]), "forward")]
    elif linear_way == "back":
        log_files = [("".join(["linear_trial",f"/{file_num}_trial","back.md"]), "back")]
    return log_files

file_num_0 = 1
linear_way = "forward"

log_files = file_name(file_num_0)

pose_pattern = re.compile(
    r"t:\s*(-?\d+\.?\d*),\s*current_theta:\s*(-?\d+\.?\d*),\s*current_x:\s*(-?\d+\.?\d*),\s*current_y\s*=\s*(-?\d+\.?\d*)"
)
vel_pattern = re.compile(
    r"t\s*=\s*(-?\d+\.?\d*).*?"
    r"left_actual_velocity\s*=\s*(-?\d+\.?\d*).*?"
    r"right_actual_velocity\s*=\s*(-?\d+\.?\d*)"
)
all_t = []
all_x = []
all_y = []
all_theta = []
labels = []

all_lefts = []
all_rights = []
all_sums = []


all_linear = []
all_angular = []

sim_left_val = []
sim_right_val = []

t_val = []

for file_index,(path, label) in enumerate(log_files):
    with open(path, "r") as f:
        lines = f.readlines()



    x_vals = []
    y_vals = []
    theta_vals = []
    abs_left_vels = []
    abs_right_vels = []

    left_vels = []
    right_vels = []
    sum_vels = []
    linear_vels = []
    angular_vels = []
    for i in range(0, len(lines) - 1, 2):
        pose_line = lines[i]
        vel_line = lines[i + 1]

        pose_match = pose_pattern.search(pose_line)
        vel_match = vel_pattern.search(vel_line)

        if pose_match and vel_match:
            t = float(pose_match.group(1))
            theta = float(pose_match.group(2))
            x = float(pose_match.group(3)) - 105000
            y = float(pose_match.group(4)) - 103000

            timing = float(vel_match.group(1))
            left = float(vel_match.group(2))
            right = float(vel_match.group(3))

            all_t.append(t)
            t_val.append(timing)
            x_vals.append(x)
            y_vals.append(y)
            theta_vals.append(theta)

            abs_left_vels.append(abs(left))
            abs_right_vels.append(abs(right))

            linear_vels.append((left + right)/2)
            angular_vels.append((right - left)/485)

            left_vels.append(left)
            right_vels.append(right)

            sim_left_val.append(left)
            sim_right_val.append(right)

    all_x.append(x_vals)
    all_y.append(y_vals)
    all_theta.append(theta_vals)
    labels.append(label)

    all_lefts.append(abs_left_vels)
    all_rights.append(abs_right_vels)

    all_linear.append(linear_vels)
    all_angular.append(angular_vels)

    all_sums.append(sum_vels)

if __name__ == '__main__':

    plt.figure(figsize=(8, 8))
    for i in range(len(log_files)):
        plt.plot(all_x[i], all_y[i], label=labels[i])
        skip = max(len(all_x[i]) // 20, 1)
        print(f"len(allx[i]):{len(all_x[i])}")
        for j in range(0, len(all_x[i]), skip):
            plt.text(all_x[i][j], all_y[i][j], all_t[j], alpha = 0.3)
            # plt.arrow(all_x[i][j], all_y[i][j], dx, dy, head_width=0.05, color='r', alpha=0.5)

    plt.tight_layout()
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("ant's pose")
    # plt.axis("equal")
    plt.grid(True)
    plt.legend()
    plt.show()

    n = len(log_files)
    fig, axes = plt.subplots(n, 1, figsize=(10, 4 * n), sharex=False)

    if n == 1:
        axes = [axes]

    for i in range(n):
        ax = axes[i]

        # v_ant = all_linear[i]   # 线速度
        # w_ant = all_angular[i]  # 角速度

    

        # 左轴：线速度
        ax.plot(all_lefts[i], label = 'Left Velocity', color='tab:blue')
        ax.plot(all_rights[i], label = 'Right Velocity', color = 'tab:red')
        ax.set_ylabel("Velocity (mm/s)")
        # ax.tick_params(axis='y', labelcolor='tab:blue')

        # # 右轴：角速度
        # ax2 = ax.twinx()
        # ax2.plot(all_rights[i], label='Angular Velocity', color='tab:red')
        # ax2.set_ylabel("Angular Velocity (rad/s)", color='tab:red')
        # ax2.tick_params(axis='y', labelcolor='tab:red')
        ax.legend()
        ax.set_title(f"Velocity_diff - {labels[i]}")
        ax.set_xlabel("t(/ms)")
        ax.grid(True)



    plt.tight_layout()
    plt.show()
