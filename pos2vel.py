import numpy as np
import matplotlib.pyplot as plt
from vel_pos import *

all_x = [x for sublist in all_x for x in sublist]
all_y = [x for sublist in all_y for x in sublist]
all_theta = [x for sublist in all_theta for x in sublist]
x_vals = np.array(all_x) 
y_vals = np.array(all_y)
theta_vals = np.array(all_theta)
t_vals = np.array([t*0.01 for t in range(len(all_x))])
L = 485.0

dt = np.diff(t_vals)
dx = np.diff(x_vals)
dy = np.diff(y_vals)
dtheta = np.diff(theta_vals)

theta_rad = np.radians(theta_vals)
omega = np.diff(np.unwrap(theta_rad)) / dt

v = np.sqrt(dx**2 + dy**2) / dt

v = v[1:]
omega = omega[1:]
valid_t = t_vals[2:] 

v_r = v + (L / 2) * omega
v_l = v - (L / 2) * omega

print("右轮速度 v_r:", v_r)
print("左轮速度 v_l:", v_l)


fig, ax = plt.subplots(1, 1, figsize=(10, 3), sharex=False)
# plt.plot(valid_t, (v_l + v_r)/2, label="Left Wheel Velocity (mm/s)")
ax.plot(valid_t, (v_l + v_r)/2, label="linear velocity(mm/s)", color = "tab:red")
ax.set_ylabel("linear Velocity", color = "tab:red")
ax_right = ax.twinx()
# plt.plot(valid_t, (v_r - v_l)/L, label="Right Wheel Velocity (mm/s)")
ax_right.plot(valid_t, (v_r - v_l)/L, label="angular velocity (rad/s)", color = "tab:blue")
ax_right.set_ylabel("angular velocity", color = "tab:blue")
plt.xlabel("Time (s)")
# plt.ylabel("Velocity (mm/s)")
# plt.title("Estimated Left/Right Wheel Velocities")
ax.legend()
ax_right.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
