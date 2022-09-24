import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib
from pathlib import Path
from typing import Union
from datetime import date

matplotlib.use('TkAgg')
np.set_printoptions(suppress=True)
sns.set_theme()

draw_path = Path("./drawings")
draw_path.mkdir(exist_ok=True)
today_path = draw_path / date.today().strftime("%d-%m-%y")
today_path.mkdir(exist_ok=True)


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


def plot_drawing(x, y, save, bc="w", lc="k", lw=1.0):
    fig = plt.figure()
    if bc != "w":
        fig.patch.set_facecolor(bc)

    plt.plot(x, y, color=lc, linewidth=lw)
    plt.axis('off')
    plt.tight_layout()
    if save:
        fig.savefig(today_path / "prova.jpg", dpi=300)


class Liss:
    def __init__(self, t_max: int, dt: float, t_x: Union[float, int], t_y: Union[float, int], phase: float):
        self.time = timeline(t_max=t_max, dt=dt)
        self.x = np.cos(2 * np.pi / t_x * self.time)
        self.y = np.sin(2 * np.pi / t_y * self.time)
        self.x_rot = None
        self.y_rot = None

    def plot(self, save: bool = False, background: str = "w", linecolor: str = "k", linewidth: float = 1.0):
        plot_drawing(self.x, self.y, save, bc=background, lc=linecolor, lw=linewidth)

    def rotate(self, x_rot, y_rot, t_background):
        self.x, self.y = rotate_curve(self.x, self.y, self.time, x_rot=x_rot, y_rot=y_rot, t_background=t_background)
        # TODO should this return something? this should overwrite the original coords or crete new one?

    def translate(self, v_x, v_y):
        self.x, self.y = translate_curve(self.x, self.y, self.time, v_x=v_x, v_y=v_y)


if __name__ == "__main__":
    prova = Liss(50, 0.025, np.pi, 2, 1)
    prova.rotate(1, 1, 2)
    prova.plot(save=False, background="black", linecolor="r", linewidth=2)
