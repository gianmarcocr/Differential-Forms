from typing import Union

import matplotlib.pyplot as plt
import numpy as np

from differentialforms.drawings.curve import Curve
from differentialforms.utils import Timeline, compute_length, line_from_points


class Phasor(Curve):
    def __init__(
        self,
        time: Timeline,
        x_cent: Union[float, int] = 0,
        y_cent: Union[float, int] = 0,
        radius: Union[float, int] = 1,
        period: Union[float, int] = 10,
        phase: Union[float, int] = 0,
    ):
        super().__init__(name="phasor")
        self.x_c = x_cent
        self.y_c = y_cent
        self.radius = radius
        self.time = time.time
        self.T = period
        self.phi = phase
        self.x = self.x_c + self.radius * np.cos(
            (2 * np.pi / self.T) * self.time + self.phi
        )
        self.y = self.y_c + self.radius * np.sin(
            (2 * np.pi / self.T) * self.time + self.phi
        )
        self.length = compute_length(self.x, self.y)


class Pintograph(Curve):
    def __init__(
        self,
        curve1,
        curve2,
        arm1: float,
        arm2: float,
        extension: int = 0,
        choice: str = "up",
    ):
        super().__init__(name="Pintograph")
        self.p1 = curve1
        self.p2 = curve2
        assert (
            curve1.time.all() == curve2.time.all()
        ), "curve1 and curve2 have different timelines"
        self.time = curve1.time
        self.l1 = arm1
        self.l2 = arm2
        self.u = extension
        self.choice = choice
        self.x, self.y = self._solution()
        self.length = compute_length(self.x, self.y)

    def get_metadata(self):
        pinto_meta = self.__dict__.copy()
        pinto_meta.pop("p1")
        pinto_meta.pop("p2")
        p1_meta = self.p1.__dict__
        p2_meta = self.p2.__dict__
        meta = (
            "Pintograph:\n"
            + str(pinto_meta)
            + "\nPhasor1:\n"
            + str(p1_meta)
            + "\nPhasor2:\n"
            + str(p2_meta)
        )
        return meta

    def _solution(self):
        assert len(self.p1.time) == len(
            self.p2.time
        ), f"Phasor 1 and 2 time vectors have different lengths: {self.p1.time} != {self.p2.time}"

        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y

        d = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        x, y = np.nan * np.ones_like(d), np.nan * np.ones_like(d)

        valid_points = d <= self.l1 + self.l2
        assert np.all(valid_points), (
            f"Warning: some points are unreachable with these arms (l1={self.l1}, l2={self.l2}). "
            f"Go back and increase those"
        )

        a = (self.l1**2 - self.l2**2 + d**2) / (2 * d)
        h = np.sqrt(self.l1**2 - a**2)

        x2_x1_d = (x2 - x1) / d
        y2_y1_d = (y2 - y1) / d
        x3 = x1 + a * x2_x1_d
        y3 = y1 + a * y2_y1_d
        x4 = x3 + h * y2_y1_d
        y4 = y3 - h * x2_x1_d
        x5 = x3 - h * y2_y1_d
        y5 = y3 + h * x2_x1_d

        if self.choice == "up":
            x[valid_points] = np.where(y4 >= y5, x4, x5)[valid_points]
            y[valid_points] = np.where(y4 >= y5, y4, y5)[valid_points]
        elif self.choice == "down":
            x[valid_points] = np.where(y4 <= y5, x4, x5)[valid_points]
            y[valid_points] = np.where(y4 <= y5, y4, y5)[valid_points]

        if self.u > 0:
            m, q = line_from_points([x1, y1], [x, y])
            alpha = np.arctan(m)
            x += np.where(alpha > 0, self.u * np.cos(alpha), -self.u * np.cos(alpha))
            y += np.where(alpha > 0, self.u * np.sin(alpha), -self.u * np.sin(alpha))

        return x, y

    def display(self):
        fig, ax = plt.subplots(figsize=(10, 10))
        alpha = 0.5
        ax.set_facecolor("white")
        ax.axis("equal")

        r1_label = (
            self.p1.radius
            if isinstance(self.p1.radius, int) or isinstance(self.p1.radius, float)
            else [self.p1.radius[i] for i in range(3)] + ["..."]
        )
        p1 = ax.plot(
            self.p1.x, self.p1.y, label=f"Phasor 1: r={r1_label} ", alpha=alpha
        )
        ax.plot(self.p1.x_c, self.p1.y_c, c=p1[0].get_color(), marker="o", alpha=alpha)
        ax.plot(
            [self.p1.x[0], self.x[0]],
            [self.p1.y[0], self.y[0]],
            "k",
            label=f"Arm 1: l={self.l1}",
            alpha=alpha,
            zorder=2,
        )

        r2_label = (
            self.p2.radius
            if isinstance(self.p2.radius, int) or isinstance(self.p2.radius, float)
            else [self.p2.radius[i] for i in range(3)] + ["..."]
        )
        p2 = ax.plot(self.p2.x, self.p2.y, label=f"Phasor 2: r={r2_label}", alpha=alpha)
        ax.plot(self.p2.x_c, self.p2.y_c, c=p2[0].get_color(), marker="o", alpha=alpha)
        ax.plot(
            [self.p2.x[0], self.x[0]],
            [self.p2.y[0], self.y[0]],
            "k",
            label=f"Arm 2: l={self.l2}",
            alpha=alpha,
            zorder=2,
        )
        ax.plot(self.x, self.y, label="Pintograph", alpha=1, c="k", lw=2, zorder=1)

        start_x, end_x = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(int(start_x), int(end_x), 0.5))
        start_y, end_y = ax.get_ylim()
        ax.yaxis.set_ticks(np.arange(int(start_y), int(end_y), 0.5))
        ax.grid(visible=True, which="both", color="k", linestyle="-", alpha=alpha)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Pintograph")
        ax.legend()


def extend(Sx, Sy, Cx, Cy, r, choice):
    def linecircle(x, y, r, m, q, choice=2):
        a = -2 * x
        b = -2 * y
        c = a**2 / 4 + b**2 / 4 - r**2
        a1 = 1 + m**2
        b1 = 2 * m * q + a + b * m
        c1 = q**2 + b * q + c
        delta = b1**2 - 4 * a1 * c1
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
