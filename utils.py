from datetime import datetime
# from PIL.PngImagePlugin import PngInfo
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from tqdm import tqdm
from pathlib import Path
from datetime import date
import os
from matplotlib.collections import LineCollection


# from differentialforms.Curve import Curve  # TODO FIX


def ensure_folder_struct():
    Path("images").mkdir(exist_ok=True)
    today_path = Path("images") / date.today().strftime("%d-%m-%y")
    today_path.mkdir(exist_ok=True)
    os.environ["today_path"] = str(today_path)


def compute_length(curve):
    l = 0
    for i in range(len(curve.t) - 1):
        l += ((curve.x[i + 1] - curve.x[i]) ** 2 + (curve.y[i + 1] - curve.y[i]) ** 2) ** 0.5
    return l


def pol2cart(rho, theta):
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return x, y


def rotate_curve(x, y, time, x_rot, y_rot, t_background: float = 0, phi: float = 0):
    omega = 0 if t_background == 0 else 2 * np.pi / t_background
    qx = x_rot + np.cos(omega * time + phi) * (x - x_rot) - np.sin(omega * time + phi) * (y - y_rot)
    qy = y_rot + np.sin(omega * time + phi) * (x - x_rot) + np.cos(omega * time + phi) * (y - y_rot)
    return qx, qy


def translate_curve(x, y, time, v_x: float = 0, v_y: float = 0):
    qx = x + v_x * time
    qy = y + v_y * time
    return qx, qy


def timeline(t_max: int, dt: float, t_min: int = 0) -> object:
    return np.arange(t_min, t_max + dt, dt)


def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img


def plot_drawing(draw: Union[object, list],
                 save: bool = False,
                 bc: str = "w",
                 lc: Union[str, list] = "k",
                 lw: float = 1.0,
                 show: bool = True,
                 logo: bool = False,
                 legend: bool = False):
    # metadata = draw.get_metadata()

    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111, aspect="equal")
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
            # points = np.array([d.x, d.y]).T.reshape(-1, 1, 2)
            # segments = np.concatenate([points[:-1], points[1:]], axis=1)
            # norm = plt.Normalize(d.t[0], d.t[-1])
            # ls = LineCollection(segments, cmap="magma", norm=norm)
            # ls.set_array(d.t)
            # ax.add_collection(ls)
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
            # if bc == "k":
            #     im = 255 - im
            imagebox = OffsetImage(im, zoom=0.1, cmap="gray")
            ab = AnnotationBbox(imagebox, (max_x, min_y), frameon=False)
            ax.add_artist(ab)
        fig.savefig(save_path + ".png", facecolor=fig.get_facecolor(), dpi=300)
        plt.close()

        # img = fig2img(fig)  # TODO fix file extension
        # meta = PngInfo()
        # meta.add_text(draw.__class__.__name__, metadata)  # TODO fix metadata
        # img.save(save_path, pnginfo=meta)


def parse_metadata(data):
    # result = result or dict()
    if isinstance(data, dict):
        for key, item in data.items():
            if isinstance(item, dict):
                parse_metadata(item)
            elif isinstance(data, (list, int, float)):
                meta.add_text(data, str(item))
    return


def rotate_live(curve, x_rot: float, y_rot: float, T: float):
    """
    Compute rotated curve for each timestamp
    Args:
        curve:
        x_rot:
        y_rot:
        T:

    Returns:

    """
    assert hasattr(curve, "x") & hasattr(curve, "y") & hasattr(curve, "t"), print(
        "Curve doesn't have the correct attributes")

    curve_rotated = []
    dt = curve.t[1]
    omega = 0 if T == 0 else -2 * np.pi / T

    for i in tqdm(range(0, len(curve.t)), desc="Computing rotated curve"):
        rot_x_i = []
        rot_y_i = []
        for j in range(i + 1):
            x = x_rot + np.cos(omega * dt * (i - j)) * (curve.x[j] - x_rot) - np.sin(omega * dt * (i - j)) * (
                    curve.y[j] - y_rot)
            y = y_rot + np.sin(omega * dt * (i - j)) * (curve.x[j] - x_rot) + np.cos(omega * dt * (i - j)) * (
                    curve.y[j] - y_rot)
            rot_x_i.append(x)
            rot_y_i.append(y)
        curve_rotated.append(Curve(time=curve.t[:i], x=rot_x_i, y=rot_y_i))

    return curve_rotated


def sigmoid(x, a: float = 1, b: float = 0):
    """
    Args:
        x: point where to compute sigmoid
        a: increase steepness
        b: translate sigmoid left or right

    Returns: 1/(1+e^(-ax+b)

    """
    return 1 / (1 + np.exp(-a * x + b))

# def rot(i,j):
#     rot_matrix = np.array([[np.cos(omega * dt * (i-j)), -np.sin(omega * dt * (i-j))],
#                             [np.sin(omega * dt * (i-j)), np.cos(omega * dt * (i-j))]])
#     return rot_matrix
#
# for i in tqdm(range(tim.shape[0])):
#     rot_i = []
#     for j in range(i):
#         r = [x_rot, y_rot] + np.dot(rot(i,j), [pinto.x[j] - x_rot, pinto.x[j] - x_rot])
#         rot_i.append(r)
#     rotated_curve_new.append(rot_i)


# def piecewise(time: timeline, steps: list):
#     v = np.zeros_like(time)
#     start = 0
#     c = steps[0][1]
#     d = []
#     for i in range(len(steps)):
#         v[start:steps[i][0]] =




















