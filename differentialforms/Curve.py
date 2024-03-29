from abc import ABC, abstractmethod

import numpy as np

import utils


class Curve(ABC):
    @abstractmethod
    def __init__(self, x: np.array = 0, y: np.array = 0, t= 0):
        self.x = x
        self.y = y
        self.t = t

    def get_metadata(self):
        curve_meta = self.__dict__.copy()
        return str(curve_meta)

    def plot(self, save: bool = False, background: str = "w", linecolor: str = "k", linewidth: float = 1.0, **kwargs):
        utils.plot_drawing(self, save, bc=background, lc=linecolor, lw=linewidth, **kwargs)

    def rotate(self, x_rot, y_rot, t_background, phase=0):
        self.x, self.y = utils.rotate_curve(self.x,
                                            self.y,
                                            self.t,
                                            x_rot=x_rot,
                                            y_rot=y_rot,
                                            t_background=t_background, phi=phase)
        return self

    def translate(self, v_x, v_y):
        self.x, self.y = utils.translate_curve(self.x,
                                               self.y,
                                               self.t,
                                               v_x=v_x,
                                               v_y=v_y)
        return self

    def __getitem__(self, item):
        return self.x[item], self.y[item]
