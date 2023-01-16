from typing import Union
import numpy as np
from .Curve_abs import Curve


class Lissajous(Curve):
    def __init__(self, time, x_period: Union[float, int], y_period: Union[float, int],
                 phase: float = 0):
        super().__init__()
        self.t = time
        self.phi = phase
        self.T_x = x_period
        self.T_y = y_period
        self.x = np.cos(2 * np.pi / self.T_x * self.t + self.phi)
        self.y = np.sin(2 * np.pi / self.T_y * self.t + self.phi)
