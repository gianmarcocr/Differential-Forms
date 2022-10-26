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

tmax = 100
dt = 1
tim = utils.timeline(t_max=tmax, dt=dt)
u=tim/tmax

r1 = 1.5 + np.sin(2 * np.pi / 20 * tim)
r2 = 1
x_rot, y_rot = -3, 5

phasor1 = curve1 = Phasor(tim, x_cent=0, y_cent=0, radius=r1, period=50, phase=0)
phasor2 =  Phasor(tim, x_cent=curve1.x, y_cent=curve1.y, radius=r2, period=-5-20*u, phase=0*np.pi*tim/100)
# pintograph = Pintograph(phasor1=phasor1, phasor2=phasor2, arm1=5, arm2=5, extension=0)

curva = phasor2

scia = utils.rotate_live(curva, x_rot, y_rot)
dist = max(np.sqrt((curva.x - x_rot) ** 2 + (curva.y - y_rot) ** 2))


class Anim:
    def __init__(self):
        fig = plt.figure(figsize=(10.8, 10.8))
        ax = fig.add_subplot(111, aspect="equal")
        max_x, min_x = x_rot + dist, x_rot - dist
        max_y, min_y = y_rot + dist, y_rot - dist
        ax.set(xlim=(min_x - 0.1, max_x + 0.1), ylim=(min_y - 0.1, max_y + 0.1))
        ax.axis('off')

        self.circle1, = ax.plot(phasor1.x, phasor1.y, c="k", lw=0.5)  # first circle
        self.circle2, = ax.plot(phasor2.x, phasor2.y, c="k", lw=0.5)  # second circle
        self.fasore1, = ax.plot(phasor1.x[0], phasor1.y[0], marker="o")  # first phasor
        self.fasore2, = ax.plot(phasor2.x[0], phasor2.y[0], marker="o")  # second phasor

        self.scia, = ax.plot(curva.x[0], curva.y[0])  # second phasor
        # self.pint, = ax.plot(pintograph.x[0], pintograph.y[0])  # pintograph
        # self.arm1, = ax.plot([phasor1.x[0], pintograph.x[0]], [phasor1.y[0], pintograph.y[0]])  # first arm
        # self.arm2, = ax.plot([phasor2.x[0], pintograph.x[0]], [phasor2.y[0], pintograph.y[0]])  # second arm

        self.ani = animation.FuncAnimation(fig, self.animate, interval=0, blit=True,
                                           frames=tqdm(range(len(phasor1.x)), desc="Plotting animation"),
                                           repeat_delay=5000,
                                           )
        self.paused = False

        # self.ani.save(os.environ["today_path"] + f"/{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.mov",
        #               fps=60,
        #               dpi=200)
        fig.canvas.mpl_connect('button_press_event', self.toggle_pause)

    def animate(self, i):
        self.circle1.set_data(phasor1.x[:i], phasor1.y[:i])
        # self.circle1.set_alpha(max(1-i/(tmax/2),0))

        self.circle2.set_data(phasor2.x[:i], phasor2.y[:i])
        # self.circle2.set_alpha(max(1-i/(tmax/2),0))

        self.fasore1.set_data(phasor1.x[i], phasor1.y[i])  # update the data.
        self.fasore1.set_color("k")  # np.random.rand(3,)

        self.fasore2.set_data(phasor2.x[i], phasor2.y[i])
        self.fasore2.set_color("k")

        # self.scia.set_data(scia.x[i], scia.y[i])
        # self.scia.set_color("r")
        # self.arm1.set_data([phasor1.x[i], pintograph.x[i]], [phasor1.y[i], pintograph.y[i]])
        # self.arm2.set_data([phasor2.x[i], pintograph.x[i]], [phasor2.y[i], pintograph.y[i]])

        self.scia.set_data(scia[i][:, 0], scia[i][:, 1])
        self.scia.set_color("r")

        if i == tim.shape[0]-1 :
            self.circle1.set_alpha(0)
            self.circle2.set_alpha(0)
            # self.arm1.set_alpha(0)
            # self.arm2.set_alpha(0)
            self.fasore1.set_alpha(0)
            self.fasore2.set_alpha(0)

        return self.circle1, self.circle2, self.fasore1, self.fasore2, self.scia # self.pint, self.arm1, self.arm2,  # the comma is needed here

    def toggle_pause(self, *args, **kwargs):
        if self.paused:
            self.ani.resume()
        else:
            self.ani.pause()
        self.paused = not self.paused


# ani.save('test.gif', fps=60)

# To save the animation, use e.g.
#
# ani.save("movie.mp4")
#
# or
#

pa = Anim()
plt.show()
