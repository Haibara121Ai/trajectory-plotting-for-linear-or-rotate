import numpy as np
import matplotlib.pyplot as plt

t_val = [x*0.01 for x in range(200)]

left_v = [x * 10 for x in range(100)] + [(1000 - x * 10) for x in range(100)]
right_v = [ -x * 1.01 for x in left_v]

t = np.diff(t_val)
L = 440
[x, y, theta] = [0, 0, 0]




# print(left_v)
# print(right_v)

x_list = [x]
y_list = [y]
theta_list = [theta]

for vl, vr, dt in zip(left_v, right_v, t):
    v = (vl + vr) / 2
    w = (vr - vl) / L
    x += v * np.cos(theta) * dt
    y += v * np.sin(theta) * dt
    theta += w * dt

    x_list.append(x)
    y_list.append(y)
    theta_list.append(theta)

final_position = (x, y)
total_displacement = np.sqrt(x**2 + y**2)
print(f"最终位置：x = {x:.2f} mm, y = {y:.2f} mm")
print(f"总位移：{total_displacement:.2f} mm")

plt.figure(figsize=(6, 6))
plt.plot(x_list, y_list, label="Trajectory")
# for i in range(0, len(x_list), 10):  # 每 10 步画一个朝向箭头
#     dx = 50 * np.cos(theta_list[i])  # 箭头长度 (mm)
#     dy = 50 * np.sin(theta_list[i])
#     plt.arrow(x_list[i], y_list[i], dx, dy, head_width=15, color='k', alpha=0.5)

plt.xlabel("X Position (mm)")
plt.ylabel("Y Position (mm)")
plt.title("Differential Drive Robot Trajectory")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
