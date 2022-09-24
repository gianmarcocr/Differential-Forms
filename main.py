import seaborn as sns
import matplotlib
from pathlib import Path
from datetime import date, datetime
import numpy as np
from drawings.Lissajous import Liss
import os

matplotlib.use('TkAgg')
np.set_printoptions(suppress=True)
sns.set_theme()

draw_path = Path("images")
draw_path.mkdir(exist_ok=True)

today_path = draw_path / date.today().strftime("%d-%m-%y")
today_path.mkdir(exist_ok=True)
os.environ["today_path"] = str(today_path)

if __name__ == "__main__":
    curve = Liss(50, 0.025, np.pi, 2, 1)
    curve.rotate(x_rot=1, y_rot=1, t_background=2).rotate(x_rot=1, y_rot=1, t_background=2)
    curve.plot(save=True, background="black", linecolor="r", linewidth=2)
