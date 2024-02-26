from typing import List, Union

from differentialforms.drawings.curve import Curve
from differentialforms.utils import plot_drawing


class DrawingCanvas:
    """
    Create drawing canvas to then show everything
    """

    def __init__(self):
        self.curve_list = []

    def add(self, curve: Union[List, Curve]):
        if isinstance(curve, list):
            self.curve_list.extend(curve)
        else:
            self.curve_list.append(curve)
        return self

    def plot(
        self,
        save: bool = False,
        background: str = "w",
        linecolor: str = "k",
        linewidth: float = 1.0,
        show=True,
        **kwargs
    ):
        plot_drawing(
            self.curve_list,
            save=save,
            bc=background,
            lc=linecolor,
            lw=linewidth,
            show=show,
            **kwargs,
        )
