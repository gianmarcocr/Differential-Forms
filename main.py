import os
from datetime import date
from pathlib import Path

import matplotlib
import numpy as np
import seaborn as sns

from drawings.Phasor import Phasor, Pintograph
from drawings.Lissajous import Lissajous
from drawings.Canvas import DrawingCanvas
from utils import timeline

matplotlib.use('TkAgg')
np.set_printoptions(suppress=True)
sns.set_theme()

draw_path = Path("images")
draw_path.mkdir(exist_ok=True)

today_path = Path("images") / date.today().strftime("%d-%m-%y")
today_path.mkdir(exist_ok=True)
os.environ["today_path"] = str(today_path)

if __name__ == "__main__":
    t = timeline(t_max=100, dt=0.1)
    # curve = Lissajous(50, 0.025, np.pi, 2, 1)
    # curve.rotate(x_rot=1, y_rot=1, t_background=2).rotate(x_rot=1, y_rot=1, t_background=2)
    # curve.plot(save=True, background="black", linecolor="r", linewidth=2)
    curve = Phasor(time=t, x_cent=0, y_cent=0, radius=3, period=100, phase=0)
    curve2 = Phasor(time=t, x_cent=2, y_cent=0, radius=3, period=50, phase=np.pi/2)
    pinto = Pintograph(phasor1=curve, phasor2=curve2, arm1=2, arm2=1.5, extension=0)
    # pinto.display()
    # pinto.plot(save=False)
    canv = DrawingCanvas().add([curve, curve2])
    canv.add(pinto)
    canv.plot()

