import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, datetime
from pathlib import Path
import os
import utils
from tqdm import tqdm

from drawings.Phasor import Phasor, Pintograph

matplotlib.use('TkAgg')

draw_path = Path("images")
draw_path.mkdir(exist_ok=True)

today_path = draw_path / date.today().strftime("%d-%m-%y")
today_path.mkdir(exist_ok=True)
os.environ["today_path"] = str(today_path)

tmax = 200
dt = 0.1
tim = utils.timeline(t_max=tmax, dt=dt)

r1 = 1.5 + np.sin(2 * np.pi / 20 * tim)
r2 = 1
x_rot, y_rot = -3, 5

curve1 = Phasor(t_max=tmax, dt=dt, x_cent=0, y_cent=0, radius=r1, period=10, phase=0)
curve2 = Phasor(t_max=tmax, dt=dt, x_cent=4, y_cent=0, radius=r2, period=5, phase=np.pi / 2)
pinto = Pintograph(phasor1=curve1, phasor2=curve2, arm1=5, arm2=5, extension=0)
pinto2 = Pintograph(phasor1=curve1, phasor2=curve2, arm1=5, arm2=5, extension=0)
pinto2.rotate(-3, 5, tmax)

dist = max(np.sqrt((pinto.x - x_rot) ** 2 + (pinto.y - y_rot) ** 2))

fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, aspect="equal")
# max_x, min_x = max(curve1.x.max(), curve2.x.max(), pinto2.x.max()), min(curve1.x.min(), curve2.x.min(), pinto2.x.min())
# max_y, min_y = max(curve1.y.max(), curve2.y.max(), pinto2.y.max()), min(curve1.y.min(), curve2.y.min(), pinto2.y.min())
max_x, min_x = x_rot + dist, x_rot - dist
max_y, min_y = y_rot + dist, y_rot - dist
ax.set(xlim=(min_x - 0.1, max_x + 0.1), ylim=(min_y - 0.1, max_y + 0.1))
ax.axis('off')

c1, = ax.plot(curve1.x, curve1.y, c="k", lw=0.5)
c2, = ax.plot(curve2.x, curve2.y, c="k", lw=0.5)
fasore1, = ax.plot(curve1.x[0], curve1.y[0], marker="o")
fasore2, = ax.plot(curve2.x[0], curve2.y[0], marker="o")
pint1, = ax.plot(pinto.x[0], pinto.y[0])
pint2, = ax.plot(pinto.x[0], pinto.y[0])
arm1, = ax.plot([curve1.x[0], pinto.x[0]], [curve1.y[0], pinto.y[0]])
arm2, = ax.plot([curve2.x[0], pinto.x[0]], [curve2.y[0], pinto.y[0]])


def animate(i):
    c1.set_data(curve1.x[:i], curve1.y[:i])
    c2.set_data(curve2.x[:i], curve2.y[:i])

    # c1.set_alpha(max(1-i/(tmax/2),0))
    # c2.set_alpha(max(1-i/(tmax/2),0))
    fasore1.set_data(curve1.x[i], curve1.y[i])  # update the data.
    fasore1.set_color("k")  # np.random.rand(3,)
    fasore2.set_data(curve2.x[i], curve2.y[i])
    fasore2.set_color("k")
    pint1.set_data(pinto.x[:i], pinto.y[:i])
    omega = -2 * np.pi / tmax
    qx = []
    qy = []
    for j in range(i):
        qx.append(x_rot + np.cos(omega * dt * (i - j)) * (pinto.x[j] - x_rot) - np.sin(omega * dt * (i - j)) * (
                pinto.y[j] - y_rot))
        qy.append(y_rot + np.sin(omega * dt * (i - j)) * (pinto.x[j] - x_rot) + np.cos(omega * dt * (i - j)) * (
                pinto.y[j] - y_rot))
    pint2.set_data(qx, qy)
    arm1.set_data([curve1.x[i], pinto.x[i]], [curve1.y[i], pinto.y[i]])
    arm2.set_data([curve2.x[i], pinto.x[i]], [curve2.y[i], pinto.y[i]])

    pint1.set_alpha(0)

    return c1, c2, fasore1, fasore2, pint1, arm1, arm2, pint2  # the comma is needed here


ani = animation.FuncAnimation(fig, animate, interval=0, blit=False, frames=tqdm(range(len(curve1.x))))
#ani.save('test.gif', fps=60)

# To save the animation, use e.g.
#
# ani.save("movie.mp4")
#
# or
#
# writer = animation.FFMpegWriter(
#     fps=30, metadata=dict(artist='Me'), bitrate=100)
# ani.save("movie.mp4", writer=writer)

plt.show()
