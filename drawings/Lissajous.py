from typing import Union
import utils
import numpy as np

class Lissajous:
    def __init__(self, t_max: int, dt: float, x_period: Union[float, int], y_period: Union[float, int],
                 phase: float = 0):
        self.t = utils.timeline(t_max=t_max, dt=dt)
        self.phi = phase
        self.T_x = x_period
        self.T_y = y_period
        self.x = np.cos(2 * np.pi / self.T_x * self.t + self.phi)
        self.y = np.sin(2 * np.pi / self.T_y * self.t + self.phi) # TODO fix all this path situation

    def get_metadata(self):
        liss_meta = self.__dict__.copy()
        return str(liss_meta)

    def plot(self, save: bool = False, background: str = "w", linecolor: str = "k", linewidth: float = 1.0):
        utils.plot_drawing(self, save, bc=background, lc=linecolor, lw=linewidth)

    def rotate(self, x_rot, y_rot, t_background):
        self.x, self.y = utils.rotate_curve(self.x, self.y, self.t, x_rot=x_rot, y_rot=y_rot,
                                            t_background=t_background)
        return self

    def translate(self, v_x, v_y):
        self.x, self.y = utils.translate_curve(self.x, self.y, self.t, v_x=v_x, v_y=v_y)
        return self

    def __getitem__(self, item):
        return self.x[item], self.y[item]

