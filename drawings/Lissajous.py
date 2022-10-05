from typing import Union
import utils
import numpy as np
from datetime import datetime
import os


class Lissajous:
    def __init__(self, t_max: int, dt: float, x_period: Union[float, int], y_period: Union[float, int],
                 phase: float = 0):
        self.t = utils.timeline(t_max=t_max, dt=dt)
        self.phi = phase
        self.T_x = x_period
        self.T_y = y_period
        self.x = np.cos(2 * np.pi / self.T_x * self.t + self.phi)
        self.y = np.sin(2 * np.pi / self.T_y * self.t + self.phi)
        self.save_path = os.environ["today_path"] + "/Lissajous/"
        if not os.path.exists(self.save_path): os.makedirs(self.save_path)  # TODO fix all this path situation

    # def __make_coord(self):
    #
    #     return np.column_stack((x, y))

    def plot(self, save: bool = False, background: str = "w", linecolor: str = "k", linewidth: float = 1.0):
        if save:
            save = self.save_path + f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.png"
        utils.plot_drawing(self.x, self.y, save, bc=background, lc=linecolor, lw=linewidth)

    def rotate(self, x_rot, y_rot, t_background):
        self.x, self.y = utils.rotate_curve(self.x, self.y, self.t, x_rot=x_rot, y_rot=y_rot,
                                            t_background=t_background)
        return self  # TODO should this return something? this should overwrite the original coords or crete new one?

    def translate(self, v_x, v_y):
        self.x, self.y = utils.translate_curve(self.x, self.y, self.time, v_x=v_x, v_y=v_y)
        return self

    def __getitem__(self, item):
        return self.x[item], self.y[item]

