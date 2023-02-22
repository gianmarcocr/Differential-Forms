import warnings

import matplotlib.pyplot as plt
import numpy as np

from utils import compute_length, line_from_points, Timeline
from .Curve import Curve


class Phasor(Curve):
    def __init__(self, time: Timeline, x_cent: float = 0, y_cent: float = 0, radius: float = 1, period: float = 10,
                 phase: float = 0):
        super().__init__()
        self.x_c = x_cent
        self.y_c = y_cent
        self.r = radius
        self.t = time.time
        self.T = period
        self.phi = phase
        self.x = self.x_c + self.r * np.cos((2 * np.pi / self.T) * self.t + self.phi)
        self.y = self.y_c + self.r * np.sin((2 * np.pi / self.T) * self.t + self.phi)
        self.length = compute_length(self)


class Pintograph(Curve):
    def __init__(self, curve1, curve2, arm1: float, arm2: float, extension: int = 0, choice: str = "up"):
        super().__init__()
        self.p1 = curve1
        self.p2 = curve2
        assert curve1.t.all() == curve2.t.all(), "curve1 and curve2 have different timelines"
        self.t = curve1.t
        self.l1 = arm1
        self.l2 = arm2
        self.u = extension
        self.choice = choice
        self.x, self.y = self._solution
        self.length = compute_length(self)

    def get_metadata(self):
        pinto_meta = self.__dict__.copy()
        pinto_meta.pop("p1")
        pinto_meta.pop("p2")
        p1_meta = self.p1.__dict__
        p2_meta = self.p2.__dict__
        meta = "Pintograph:\n" + str(pinto_meta) + "\nPhasor1:\n" + str(p1_meta) + "\nPhasor2:\n" + str(p2_meta)
        return meta

    @property
    def _solution(self):
        assert len(self.p1.t) == len(self.p2.t), print(
            f"Phasor 1 and 2 time vectors have different lengths: {self.p1.t} != {self.p2.t}")
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

    def display(self):
        fig, ax = plt.subplots(figsize=(10, 10))
        alpha = 0.5
        ax.set_facecolor("white")
        ax.axis('equal')

        r1_label = self.p1.r if isinstance(self.p1.r, int) or isinstance(self.p1.r, float) else [self.p1.r[i] for i in
                                                                                                 range(3)] + ["..."]
        p1 = ax.plot(self.p1.x, self.p1.y, label=f'Phasor 1: r={r1_label} ', alpha=alpha)
        ax.plot(self.p1.x_c, self.p1.y_c, c=p1[0].get_color(), marker="o", alpha=alpha)
        ax.plot([self.p1.x[0], self.x[0]], [self.p1.y[0], self.y[0]], 'k', label=f"Arm 1: l={self.l1}", alpha=alpha,
                zorder=2)

        r2_label = self.p2.r if isinstance(self.p2.r, int) or isinstance(self.p2.r, float) else [self.p2.r[i] for i in
                                                                                                 range(3)] + ["..."]
        p2 = ax.plot(self.p2.x, self.p2.y, label=f'Phasor 2: r={r2_label}', alpha=alpha)
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


def extend(Sx, Sy, Cx, Cy, r, choice):
    def linecircle(x, y, r, m, q, choice=2):
        a = -2 * x
        b = -2 * y
        c = a ** 2 / 4 + b ** 2 / 4 - r ** 2
        a1 = 1 + m ** 2
        b1 = 2 * m * q + a + b * m
        c1 = q ** 2 + b * q + c
        delta = b1 ** 2 - 4 * a1 * c1
        if delta > 0:
            if choice == 1:
                x1 = (-b1 + np.sqrt(delta)) / (2 * a1)
            elif choice == 2:
                x1 = (-b1 - np.sqrt(delta)) / (2 * a1)
            else:
                raise "Wrong choice. Can be only 1 o 2"
        if delta <= 0:
            print("delta <=0")
        return x1, m * x1 + q

    sol = []
    for i in range(len(Sx)):
        m, q = line_from_points([Sx[i], Sy[i]], [Cx[i], Cy[i]])
        sol.append(linecircle(Cx[i], Cy[i], r, m, q, choice))
    return np.asarray(sol)
