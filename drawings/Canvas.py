from utils import plot_drawing


class DrawingCanvas:
    """
    Create drawing canvas to then show everything
    """

    def __init__(self):
        self.curve_list = []

    def add(self, curve):
        if isinstance(curve, list):
            for c in curve:
                self.curve_list.append(c)
        else:
            self.curve_list.append(curve)
        return self

    def plot(self, save: bool = False, background: str = "w", linecolor: str = "k", linewidth: float = 1.0):
        plot_drawing(self.curve_list, save, bc=background, lc=linecolor, lw=linewidth)






