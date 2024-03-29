import matplotlib
import numpy as np
import seaborn as sns

from differentialforms.Canvas import DrawingCanvas
from differentialforms.Phasor import Phasor, Pintograph
from utils import Timeline

matplotlib.use('TkAgg')
np.set_printoptions(suppress=True)
sns.set_theme()

if __name__ == "__main__":
    """
    Demo script, just play this!
    """

    tmax = 100
    dt = 0.01

    pi = np.pi
    tim = Timeline(t_max=tmax, dt=dt)
    u = tim.time / tmax

    r1 = 1.3 + np.sin(2 * pi * u * 1)
    r2 = 1. + np.sin(2 * pi * u)

    curve = Phasor(time=tim, x_cent=0, y_cent=0, radius=r1, period=1, phase=0)
    curve2 = Phasor(time=tim, x_cent=8, y_cent=0, radius=r2, period=1, phase=0)
    pinto = Pintograph(curve1=curve, curve2=curve2, arm1=6.2, arm2=6.2, extension=0).rotate(4.5, 2.5, tmax, 0)
    canv = DrawingCanvas().add([pinto])
    canv.plot(linecolor=["k"], save=False, logo=True, show=True)
