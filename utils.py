import os
from datetime import date, datetime
from pathlib import Path
from typing import Union, Literal

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from tqdm import tqdm

from differentialforms.Curve import Curve


class Timeline:
    def __init__(self, t_max: int = 100, dt: float = 0.01, t_min: int = 0):
        self.t_max = t_max
        self.t_min = t_min
        self.dt = dt
        self.time = np.arange(t_min, t_max + dt, dt)


def line_from_points(p: list, q: list) -> (float, float):
    """
    get slope and intersect of line trough 2  points
    :param p: first point
    :param q: second point
    :return: slope, intersect
    """
    a = q[1] - p[1]
    b = q[0] - p[0]
    m = a / b
    q = (q[0] * p[1] - p[0] * q[1]) / b
    return m, q


def ensure_folder_struct():
    """
    ensure needed folders exist
    """
    Path("images").mkdir(exist_ok=True)
    today_path = Path("images") / date.today().strftime("%d-%m-%y")
    today_path.mkdir(exist_ok=True)
    os.environ["today_path"] = str(today_path)
    return


def compute_length(curve: Curve) -> float:
    """

    :param curve:
    :return: lenght of curve
    """
    l = 0
    for i in range(len(curve.t) - 1):
        l += ((curve.x[i + 1] - curve.x[i]) ** 2 + (curve.y[i + 1] - curve.y[i]) ** 2) ** 0.5
    return l


def pol2cart(rho: float, theta: float) -> (float, float):
    """
    Convert polar coord to cartesian
    :param rho:
    :param theta:
    :return:
    """
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return x, y


def rotate_curve(x: np.array, y: np.array, time: Timeline, x_rot: float, y_rot: float, t_background: float = 0,
                 phi: float = 0) -> (np.array, np.array):
    """
    Rotate a curve give a point of rotation and period
    :param x: x of original curve
    :param y: y of original curve
    :param time: vector of timesteps
    :param x_rot: x coord of rotation
    :param y_rot: y coord of rotation
    :param t_background: background period
    :param phi: phase
    :return: rotated x, rotated y
    """
    omega = 0 if t_background == 0 else 2 * np.pi / t_background
    qx = x_rot + np.cos(omega * time + phi) * (x - x_rot) - np.sin(omega * time + phi) * (y - y_rot)
    qy = y_rot + np.sin(omega * time + phi) * (x - x_rot) + np.cos(omega * time + phi) * (y - y_rot)
    return qx, qy


def translate_curve(x: np.array, y: np.array, time: Timeline, v_x: float = 0, v_y: float = 0) -> (np.array, np.array):
    """
    Translate a curve given x and y velocity
    :param x: x of original curve
    :param y: y of original curve
    :param time: vector of timesteps
    :param v_x: x velocity
    :param v_y: y velocity
    :return: translated x, translated y
    """
    qx = x + v_x * time
    qy = y + v_y * time
    return qx, qy


def fig2img(fig: plt.figure) -> Image:
    """
    Convert a Matplotlib figure to a PIL Image and return it
    :param fig:
    :return:
    """
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img


def plot_drawing(draw: Union[Curve, list[Curve]],
                 aspect: Literal["auto", "equal"] = "equal",
                 save: bool = False,
                 bc: str = "w",
                 lc: Union[str, list[str]] = "k",
                 lw: float = 1.0,
                 show: bool = True,
                 logo: bool = False,
                 legend: bool = False):
    """
    Plot drawing
    :param draw: curve(s) to be drawn
    :param aspect: force image to be square
    :param save: if you want to save
    :param bc: background color
    :param lc: line color
    :param lw: line width
    :param show: if you want to show the drawing before saving
    :param logo: if you want to add watermark
    :param legend: if you want to show legend
    """

    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111, aspect=aspect)
    fig.patch.set_facecolor(bc)  # remove this to remove background

    if isinstance(draw, list):
        max_x, min_x, max_y, min_y = -np.inf, np.inf, -np.inf, np.inf

        if not isinstance(lc, list):
            lc = [lc for i in range(len(draw))]

        if len(lc) != len(draw):
            for i in range(len(draw) - len(lc)):
                lc.append("k")

        for i, d in enumerate(draw):
            assert hasattr(d, "x") and hasattr(d, "y"), print(f"Curve {d} doesn't have the correct attributes")
            ax.plot(d.x, d.y, color=lc[i], linewidth=lw, label=i)
            if max(d.x) > max_x:
                max_x = max(d.x)
            if min(d.x) < min_x:
                min_x = min(d.x)
            if max(d.y) > max_y:
                max_y = max(d.y)
            if min(d.y) < min_y:
                min_y = min(d.y)

    elif hasattr(draw, "x") and hasattr(draw, "y"):  # TODO fix if else assert
        ax.plot(draw.x, draw.y, color=lc, linewidth=lw, label="curve")
        max_x, min_x, max_y, min_y = max(draw.x), min(draw.x), max(draw.y), min(draw.y)

    else:
        raise "The curve is neither a list nor has x and y attributes"

    ax.set_xlim(max_x + 0.1, min_x - 0.1)
    ax.set_ylim(max_y + 0.1, min_y - 0.1)
    ax.invert_xaxis()
    ax.invert_yaxis()
    plt.tight_layout()

    if show:
        if legend:
            ax.legend()
        plt.show()

    if save:
        ensure_folder_struct()
        if legend:
            ax.get_legend().remove()
        ax.axis('off')
        save_path = os.environ["today_path"] + f"/{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}"
        fig.savefig(save_path + ".svg", facecolor=fig.get_facecolor(), dpi=300)
        if logo:
            from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
            im = np.array(Image.open(r"logo/logo_DF-PNG.png"))
            imagebox = OffsetImage(im, zoom=0.1, cmap="gray")
            ab = AnnotationBbox(imagebox, (max_x, min_y), frameon=False)
            ax.add_artist(ab)
        fig.savefig(save_path + ".png", facecolor=fig.get_facecolor(), dpi=300)
        plt.close()
    return


def parse_metadata(data):
    # result = result or dict()
    if isinstance(data, dict):
        for key, item in data.items():
            if isinstance(item, dict):
                parse_metadata(item)
            elif isinstance(data, (list, int, float)):
                meta.add_text(data, str(item))
    return


# def rotate_live(curve: Curve, x_rot: float, y_rot: float, t: float):
#     """
#
#     :param curve:
#     :param x_rot:
#     :param y_rot:
#     :param t:
#     :return:
#     """
#     assert hasattr(curve, "x") & hasattr(curve, "y") & hasattr(curve, "t"), print(
#         "Curve doesn't have the correct attributes")
#
#     curve_rotated = []
#     dt = curve.t[1]
#     omega = 0 if t == 0 else -2 * np.pi / t
#
#     for i in tqdm(range(0, len(curve.t)), desc="Computing rotated curve"):
#         rot_x_i = []
#         rot_y_i = []
#         for j in range(i + 1):
#             x = x_rot + np.cos(omega * dt * (i - j)) * (curve.x[j] - x_rot) - np.sin(omega * dt * (i - j)) * (
#                     curve.y[j] - y_rot)
#             y = y_rot + np.sin(omega * dt * (i - j)) * (curve.x[j] - x_rot) + np.cos(omega * dt * (i - j)) * (
#                     curve.y[j] - y_rot)
#             rot_x_i.append(x)
#             rot_y_i.append(y)
#         curve_rotated.append(Curve(x=rot_x_i, y=rot_y_i, t=curve.t[:i]))
#
#     return curve_rotated


def sigmoid(x, a: float = 1, b: float = 0):
    """
    Compute sigmoid
    :param x: point where to compute sigmoid
    :param a: increase steepness
    :param b: translate sigmoid left or right
    :return: 1/(1+e^(-ax+b)
    """
    return 1 / (1 + np.exp(-a * x + b))

def gcode(curve, filename):
    f = open("filename.nc", "a")
    f.write("G1"," X", curve.x[0]," Y",curve.y[0], " Z", -1)

    for i in range(1,len(curve.x)):                 #loop su curva
        f.write(" X", curve.x[0]," Y",curve.y[0])

    f.write("Z", 20) #penup
    f.write("G28") #return home
    f.close()
    return

