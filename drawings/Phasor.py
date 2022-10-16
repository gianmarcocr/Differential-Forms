import numpy as np
import utils
import os
from datetime import datetime
import warnings
import matplotlib.pyplot as plt


class Phasor:
    def __init__(self, t_max, dt=0.1, x_cent=0, y_cent=0, radius=1, period=10, phase=0):  # TODO typing
        self.x_c = x_cent
        self.y_c = y_cent
        self.r = radius
        self.t = utils.timeline(t_min=0,t_max=t_max, dt=dt)
        self.T = period
        self.phi = phase
        self.x = self.x_c + self.r * np.cos((2 * np.pi / self.T) * self.t + self.phi)
        self.y = self.y_c + self.r * np.sin((2 * np.pi / self.T) * self.t + self.phi)
        self.save_path = os.environ["today_path"]
        if not os.path.exists(self.save_path): os.makedirs(self.save_path)  # TODO fix all this path situation

    # def __make_coord(self):
    #
    #     return np.column_stack((x, y))

    def get_metadata(self):
        phasor_meta = self.__dict__.copy()
        return str(phasor_meta)

    def __getitem__(self, item):
        return self.x[item], self.y[item]

    def plot(self, save: bool = False, background: str = "w", linecolor: str = "k", linewidth: float = 1.0):
        if save:
            save = self.save_path + f"/{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.png"
        utils.plot_drawing(self, save, bc=background, lc=linecolor, lw=linewidth)


def line_from_points(p, q):
    a = q[1] - p[1]
    b = q[0] - p[0]
    m = a / b
    q = (q[0] * p[1] - p[0] * q[1]) / b
    return m, q


def linecircle(x, y, r, m, q, choice):
    a = -2 * x
    b = -2 * y
    c = a ** 2 / 4 + b ** 2 / 4 - r ** 2
    a1 = 1 + m ** 2
    b1 = 2 * m * q + a + b * m
    c1 = q ** 2 + b * q + c
    delta = b1 ** 2 - 4 * a1 * c1
    if delta > 0:
        if choice == "1":
            x1 = (-b1 + np.sqrt(delta)) / (2 * a1)
        elif choice == "2":
            x1 = (-b1 - np.sqrt(delta)) / (2 * a1)

    if delta <= 0:
        print("non va dio can")
    return x1, m * x1 + q


def prolunga(Sx, Sy, Cx, Cy, r, choice="2"):
    sol = []
    for i in range(len(Sx)):
        m, q = line_from_points([Sx[i], Sy[i]], [Cx[i], Cy[i]])
        sol.append(linecircle(Cx[i], Cy[i], r, m, q, choice))
    return np.asarray(sol)


class Pintograph:
    def __init__(self, phasor1, phasor2, arm1, arm2, extension, choice="up"):
        self.p1 = phasor1
        self.p2 = phasor2
        self.l1 = arm1
        self.l2 = arm2
        self.u = extension
        self.choice = choice
        self.x, self.y = self.solution
        self.save_path = os.environ["today_path"]
        if not os.path.exists(self.save_path): os.makedirs(self.save_path)

    def get_metadata(self):
        pinto_meta = self.__dict__.copy()
        pinto_meta.pop("p1")
        pinto_meta.pop("p2")
        p1_meta = self.p1.__dict__
        p2_meta = self.p2.__dict__
        meta = "Pintograph:\n" + str(pinto_meta) + "\nPhasor1:\n" + str(p1_meta) + "\nPhasor2:\n" + str(p2_meta)
        return meta

    @property
    def solution(self):
        assert len(self.p1.t) == len(self.p2.t), print(f"Phasor 1 and 2 time vectors have different lengths: {self.p1.t} != {self.p2.t}")
        sol_x = []
        sol_y = []
        for i in range(len(self.p1.x)):
            x, y = self.intersection(self.p1.x[i], self.p1.y[i], self.l1, self.p2.x[i], self.p2.y[i], self.l2,
                                     self.choice)
            sol_x.append(x)
            sol_y.append(y)
            if self.u > 0:
                m, q = line_from_points([self.p1.x[i], self.p1.y[i]], [sol_x[i], sol_y[i]])
                alpha = np.arctan(m)
                if alpha > 0:
                    sol_x[i] += self.u * np.cos(alpha)
                    sol_y[i] += self.u * np.sin(alpha)
                else:
                    sol_x[i] -= self.u * np.cos(alpha)
                    sol_y[i] -= self.u * np.sin(alpha)
        return np.asarray(sol_x), np.asarray(sol_y)

    @staticmethod
    def intersection(x1, y1, r1, x2, y2, r2, choice):
        """
        source: https://stackoverflow.com/questions/55816902/finding-the-intersection-of-two-circles
        Args:
            x1:
            y1:
            r1:
            x2:
            y2:
            r2:
            choice:

        Returns:

        """
        d = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        x, y = np.nan, np.nan
        # non intersecting
        if d > r1 + r2:
            warnings.warn(f"Distance between phasors > sum of arms length: {d}>{r1}+{r2}")
            return x, y
        # One circle within other
        elif d < abs(r1 - r2):
            warnings.warn(f"Inscribed circles: {d}<|{r1}-{r2}|")
            return x, y
        # coincident circles
        elif d == 0 and r1 == r2:
            warnings.warn(f"Coincident circles or arms length==0: d={d}, arm1={r1} arm2={r2}")
            return x, y
        else:
            a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
            h = np.sqrt(r1 ** 2 - a ** 2)
            x3 = x1 + a * (x2 - x1) / d
            y3 = y1 + a * (y2 - y1) / d

            x4 = x3 + h * (y2 - y1) / d
            y4 = y3 - h * (x2 - x1) / d
            x5 = x3 - h * (y2 - y1) / d
            y5 = y3 + h * (x2 - x1) / d

            if choice == "up":
                if y4 >= y5:  # select upper or lower intersection
                    x, y = x4, y4
                else:
                    x, y = x5, y5
            elif choice == "down":
                if y4 <= y5:  # selezione soluzione
                    x, y = x4, y4
                else:
                    x, y = x5, y5

            return x, y

    def plot(self, save: bool = False, background: str = "w", linecolor: str = "k", linewidth: float = 1.0):
        if save:
            save = self.save_path + f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.png"
        utils.plot_drawing(self, save, bc=background, lc=linecolor, lw=linewidth)

    def display(self):
        fig, ax = plt.subplots(figsize=(15, 15))
        alpha = 0.5
        ax.set_facecolor("white")
        ax.axis('equal')
        p1 = ax.plot(self.p1.x, self.p1.y, label=f'Phasor 1: r={self.p1.r} ', alpha=alpha)
        ax.plot(self.p1.x_c, self.p1.y_c, c=p1[0].get_color(), marker="o", alpha=alpha)
        ax.plot([self.p1.x[0], self.x[0]], [self.p1.y[0], self.y[0]], 'k', label=f"Arm 1: l={self.l1}", alpha=alpha,
                zorder=2)
        p2 = ax.plot(self.p2.x, self.p2.y, label=f'Phasor 2: r={self.p2.r}', alpha=alpha)
        ax.plot(self.p2.x_c, self.p2.y_c, c=p2[0].get_color(), marker="o", alpha=alpha)
        ax.plot([self.p2.x[0], self.x[0]], [self.p2.y[0], self.y[0]], 'k', label=f"Arm 2: l={self.l2}", alpha=alpha,
                zorder=2)
        ax.plot(self.x, self.y, label='Pintograph', alpha=1, c="k", lw=2, zorder=1)
        start_x, end_x = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(int(start_x), int(end_x), 0.5))
        start_y, end_y = ax.get_ylim()
        ax.yaxis.set_ticks(np.arange(int(start_y), int(end_y), 0.5))
        ax.grid(b=True, which='both', color='k', linestyle='-', alpha=alpha)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Pintograph")
        ax.legend()

    def rotate(self, x_rot, y_rot, t_background):
        self.x, self.y = utils.rotate_curve(self.x, self.y, self.p1.t, x_rot=x_rot, y_rot=y_rot,
                                            t_background=t_background)
        return self

    def translate(self, v_x, v_y):
        self.x, self.y = utils.translate_curve(self.x, self.y, self.p1.t, v_x=v_x, v_y=v_y)
        return self

    def __getitem__(self, item):
        return self.x[item], self.y[item]

