import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib
from pathlib import Path
from typing import Union

matplotlib.use('TkAgg')
np.set_printoptions(suppress=True)
sns.set_theme()

draw_path = Path("./drawings")
draw_path.mkdir(exist_ok=True)


def pol2cart(rho, theta) -> tuple:
    """
    convert from polar to cartesian coordinates
    :param rho:
    :param theta:
    :return:
    """
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return x, y


def rotate(x, y, time, x_rot, y_rot, Tfoglio, save=False, bc="w", axe='off', cc=np.random.rand(3, ), lw=0.8):
    """
    :param x:
    :param y:
    :param time:
    :param x_rot:
    :param y_rot:
    :param Tfoglio:
    :param save:
    :param bc:
    :param axe:
    :param cc:
    :param lw:
    :return:
    """


def timeline(t_max, dt, t_min=0):
    return np.arange(t_min, t_max, dt)


def plot_drawing(x, y, save):
    plt.figure()
    plt.plot(x, y)
    plt.axis('off')
    if save:
        plt.savefig(draw_path / "prova.jpg", dpi=300)


class Liss:
    def __init__(self, t_max: int, dt: float, t_x: Union[float, int], t_y: Union[float, int], phase: float):
        self.time = timeline(t_max=t_max, dt=dt)
        self.x = np.cos(2 * np.pi / t_x * self.time)
        self.y = np.sin(2 * np.pi / t_y * self.time)

    def plot(self, save=False):
        plot_drawing(self.x, self.y, save)


if __name__ == "__main__":
    prova = Liss(50, 0.025, np.pi, 2, 1)
    prova.plot(save=True)
