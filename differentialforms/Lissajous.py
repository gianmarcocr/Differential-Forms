from typing import Union

from numpy import cos, sin, pi

from utils import compute_length
from .Curve import Curve


class Lissajous(Curve):
    def __init__(self, time, x_period: Union[float, int], y_period: Union[float, int],
                 phase: float = 0):
        super().__init__()
        self.t = time
        self.phi = phase
        self.T_x = x_period
        self.T_y = y_period
        self.x = cos(2 * pi / self.T_x * self.t + self.phi)
        self.y = sin(2 * pi / self.T_y * self.t + self.phi)
        self.length = compute_length(self)
