from typing import Union
import utils
import numpy as np
from datetime import datetime
from pathlib import Path


class Liss:
    def __init__(self, t_max: int, dt: float, t_x: Union[float, int], t_y: Union[float, int], phase: float):
        self.time = utils.timeline(t_max=t_max, dt=dt)
        self.x = np.cos(2 * np.pi / t_x * self.time)
        self.y = np.sin(2 * np.pi / t_y * self.time)
        self.x_rot = None  # TODO
        self.y_rot = None  # TODO
        self.name = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')

    def plot(self, save: bool = False, background: str = "w", linecolor: str = "k", linewidth: float = 1.0):
        if save:
            save = Path("images") / Path(datetime.now().date().strftime("%d-%m-%y")) / (datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + ".png")  #TODO tutto da rifareeeee
        utils.plot_drawing(self.x, self.y, save, bc=background, lc=linecolor, lw=linewidth)

    def rotate(self, x_rot, y_rot, t_background):
        self.x, self.y = utils.rotate_curve(self.x, self.y, self.time, x_rot=x_rot, y_rot=y_rot, t_background=t_background)
        # TODO should this return something? this should overwrite the original coords or crete new one?

    def translate(self, v_x, v_y):
        self.x, self.y = utils.translate_curve(self.x, self.y, self.time, v_x=v_x, v_y=v_y)