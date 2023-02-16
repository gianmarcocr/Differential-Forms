import matplotlib
import numpy as np
import seaborn as sns

# from differentialforms.Lissajous import Lissajous
from differentialforms.Canvas import DrawingCanvas
from differentialforms.Phasor import Phasor, Pintograph
from utils import timeline

matplotlib.use('TkAgg')
np.set_printoptions(suppress=True)
sns.set_theme()

# test

if __name__ == "__main__":
    tmax = 100  # to include last tmax as last value
    dt = 0.01

    pi = np.pi
    tim = timeline(t_max=tmax, dt=dt)
    u = tim / tmax

    r1 = 1.3 + np.sin(2 * pi * u * 1)
    r2 = 1. + np.sin(2 * pi * u)

    curve = Phasor(time=tim, x_cent=0, y_cent=0, radius=r1, period=1, phase=0)
    curve2 = Phasor(time=tim, x_cent=8, y_cent=0, radius=r2, period=1, phase=0)
    pinto = Pintograph(curve1=curve, curve2=curve2, arm1=6.2, arm2=6.2, extension=0).rotate(4.5, 2.5, tmax, 0)
    # pinto1 = Pintograph(curve1=pinto, curve2=curve2, arm1=6.2, arm2=6.2, extension=0).rotate(4.5, 2.5, tmax, 0.3)
    # pinto2 = Pintograph(curve1=curve, curve2=curve2, arm1=6.2, arm2=6.2, extension=0).rotate(4.5, 2.5, tmax, 0.6)
    canv = DrawingCanvas().add([pinto])#, pinto1, pinto2])
    lw = u * 5
    canv.plot(linecolor=["k"], save=True, logo=True, show=False)
