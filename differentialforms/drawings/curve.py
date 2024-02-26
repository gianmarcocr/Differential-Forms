from abc import ABC
from typing import Union

from differentialforms.utils import (
    rotate_curve,
    translate_curve,
    plot_drawing,
    rotate_curve_w_matrix,
)


class Curve(ABC):
    # @abstractmethod
    def __init__(self, name):
        self.type = name
        self.x = None
        self.y = None
        self.time = None

    def get_metadata(self):
        curve_meta = self.__dict__.copy()
        return str(curve_meta)

    def plot(
        self,
        save: bool = False,
        background: str = "w",
        linecolor: str = "k",
        linewidth: float = 1.0,
        **kwargs
    ):
        plot_drawing(
            self, save=save, bc=background, lc=linecolor, lw=linewidth, **kwargs
        )

    def rotate(
        self,
        x_rot: Union[float, int],
        y_rot: Union[float, int],
        t_background: Union[float, int],
        phase: Union[float, int] = 0,
    ):
        self.x, self.y = rotate_curve(
            self.x,
            self.y,
            self.time,
            x_rot=x_rot,
            y_rot=y_rot,
            t_background=t_background,
            phi=phase,
        )
        return self

    def rotate_w_m(
        self,
        x_rot: Union[float, int],
        y_rot: Union[float, int],
        t_background: Union[float, int],
        phase: Union[float, int] = 0,
    ):
        self.x, self.y = rotate_curve_w_matrix(
            self.x,
            self.y,
            self.time,
            x_rot=x_rot,
            y_rot=y_rot,
            t_background=t_background,
            phi=phase,
        )
        return self

    def translate(self, v_x, v_y):
        self.x, self.y = translate_curve(self.x, self.y, self.time, v_x=v_x, v_y=v_y)
        return self

    def __getitem__(self, item):
        return self.x[item], self.y[item]
