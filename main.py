import seaborn as sns
import matplotlib
from pathlib import Path
from datetime import date, datetime
import numpy as np
from drawings.Lissajous import Liss

matplotlib.use('TkAgg')
np.set_printoptions(suppress=True)
sns.set_theme()

draw_path = Path("images")
draw_path.mkdir(exist_ok=True)
today_path = draw_path / date.today().strftime("%d-%m-%y")
today_path.mkdir(exist_ok=True)

if __name__ == "__main__":
    prova = Liss(50, 0.025, np.pi, 2, 1)
    prova.rotate(1, 1, 2)
    prova.plot(save=True, background="black", linecolor="r", linewidth=2)
