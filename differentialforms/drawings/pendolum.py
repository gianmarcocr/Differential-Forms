from .Curve_abs import Curve
from .. import utils


class Pendulum(Curve):
    """
    Builds a "pendulum".

    Args:
        x_cent, y_cent: center coordinates
        radius: pendulum radius
        max_angle: half of the maximum aperture of the pendulum (rad)
        period: period of oscillation
        phase: direction of equilibrium (rad)

        x(t) = x_c + r * cos(alpha + phase)
        y(t) = y_c + r * sin(max_angle*alpha + phase)
        alpha(t) = 2pi/T * t

    Returns:

    """

    def __init__(
        self,
        time,
        x_cent: float = 0,
        y_cent: float = 0,
        radius: float = 1,
        max_angle: float = np.pi / 6,
        period: float = 10,
        phase: float = 0,
    ):
        self.x_c = x_cent
        self.y_c = y_cent
        self.r = radius
        self.t = time
        self.T = period
        self.max_angle = max_angle
        self.phi = phase

        self.omega = 2 * np.pi / self.T
        self.alpha = self.max_angle * np.sin(self.omega * self.t)
        self.x = self.x_c + self.r * np.cos(self.alpha + self.phi)
        self.y = self.y_c + self.r * np.sin(self.alpha + self.phi)

    def get_metadata(self):
        phasor_meta = self.__dict__.copy()
        return str(phasor_meta)

    def plot(
        self,
        save: bool = False,
        background: str = "w",
        linecolor: str = "k",
        linewidth: float = 1.0,
    ):
        utils.plot_drawing(self, save, bc=background, lc=linecolor, lw=linewidth)

    def rotate(self, x_rot, y_rot, t_background):
        self.x, self.y = utils.rotate_curve(
            self.x, self.y, self.t, x_rot=x_rot, y_rot=y_rot, t_background=t_background
        )
        return self

    def translate(self, v_x, v_y):
        self.x, self.y = utils.translate_curve(self.x, self.y, self.t, v_x=v_x, v_y=v_y)
        return self

    def __getitem__(self, item):
        return self.x[item], self.y[item]
