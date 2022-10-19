import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from typing import Union
import os
from datetime import datetime



def pol2cart(rho, theta):
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return x, y


def rotate_curve(x, y, time, x_rot, y_rot, t_background):
    omega = 2 * np.pi / t_background
    qx = x_rot + np.cos(omega * time) * (x - x_rot) - np.sin(omega * time) * (y - y_rot)
    qy = y_rot + np.sin(omega * time) * (x - x_rot) + np.cos(omega * time) * (y - y_rot)
    return qx, qy


def translate_curve(x, y, time, v_x, v_y):
    qx = x + v_x * time
    qy = y + v_y * time
    return qx, qy


def timeline(t_max: int, dt: float, t_min: int = 0) -> object:
    return np.arange(t_min, t_max+1, dt)


def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img


def plot_drawing(draw: Union[object, list], save: bool = False, bc="w", lc="k", lw=1.0):
    """
    plot single or multiple curves
    Args:
        draw:
        save:
        bc:
        lc:
        lw:

    Returns:

    """
    # metadata = draw.get_metadata()

    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(bc)  # remove this to remove background

    if isinstance(draw, list):
        for c in draw:
            ax.plot(c.x, c.y, color=lc, linewidth=lw)
    elif hasattr(draw, "x") and hasattr(draw, "y"):
        ax.plot(draw.x, draw.y, color=lc, linewidth=lw)
    else:
        raise "The curve is neither a list nor has x and y attributes"

    ax.axis('off')
    plt.tight_layout()
    plt.show()
    if save:
        save_path = os.environ["today_path"] + f"/{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.png"
        fig.savefig(save_path, facecolor=fig.get_facecolor(), dpi=300)
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



