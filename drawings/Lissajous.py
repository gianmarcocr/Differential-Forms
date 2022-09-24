from typing import Union
import utils
import numpy as np
from datetime import datetime
import os


class Liss:
    def __init__(self, t_max: int, dt: float, t_x: Union[float, int], t_y: Union[float, int], phase: float = 0):
        self.time = utils.timeline(t_max=t_max, dt=dt)
        self.x = np.cos(2 * np.pi / t_x * self.time + phase)
        self.y = np.sin(2 * np.pi / t_y * self.time + phase)

    def plot(self, save: bool = False, background: str = "w", linecolor: str = "k", linewidth: float = 1.0):
        if save:
            save = os.environ["today_path"] + f"/Lissajous/{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.png"
        utils.plot_drawing(self.x, self.y, save, bc=background, lc=linecolor, lw=linewidth)

    def rotate(self, x_rot, y_rot, t_background):
        self.x, self.y = utils.rotate_curve(self.x, self.y, self.time, x_rot=x_rot, y_rot=y_rot, t_background=t_background)
        return self
        # TODO should this return something? this should overwrite the original coords or crete new one?

    def translate(self, v_x, v_y):
        self.x, self.y = utils.translate_curve(self.x, self.y, self.time, v_x=v_x, v_y=v_y)
        return self
