import numpy as np
import matplotlib.pyplot as plt


def pol2cart(rho, theta):
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return x, y


def rotate_curve(x, y, time, x_rot, y_rot, t_background):
    omega = 2 * np.pi / t_background
    qx = x_rot + np.cos(omega * time) * (x - x_rot) - np.sin(omega * time) * (y - y_rot)
    qy = y_rot + np.sin(omega * time) * (x - x_rot) + np.cos(omega * time) * (y - y_rot)
    return qx, qy


def translate_curve(x, y, time, v_x, v_y):
    qx = x + v_x * time
    qy = y + v_y * time
    return qx, qy


def timeline(t_max: int, dt: float, t_min: int = 0):
    return np.arange(t_min, t_max, dt)


def plot_drawing(x, y, save_path=None, bc="w", lc="k", lw=1.0):
    fig = plt.figure(figsize=(20, 20))
    if bc != "w":
        fig.patch.set_facecolor(bc)

    plt.plot(x, y, color=lc, linewidth=lw)
    plt.axis('off')
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
