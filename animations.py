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

k = 1  # scale factor

tmax = 300
dt = 1
tim = utils.timeline(t_max=tmax, dt=dt)
u = tim / tmax

r1 = 5 * np.sqrt(u)
r2 = 0 + np.sin(np.pi * u) ** 2
x_rot, y_rot = -6, 5

# FASORE SU FASORE - B sopra ad A
A = Phasor(tim, x_cent=0, y_cent=0, radius=r1, period=300, phase=0)
B = Phasor(tim, x_cent=A.x, y_cent=A.y, radius=r2, period=-4, phase=0)
# pintograph = Pintograph(phasor1=phasor1, phasor2=phasor2, arm1=5, arm2=5, extension=0)


curva = B
scia = utils.rotate_live(curva, x_rot, y_rot, T=2 / 3 * tmax)
dist = max(np.sqrt((curva.x - x_rot) ** 2 + (curva.y - y_rot) ** 2))



class Anim:
    def __init__(self):
        fig = plt.figure(figsize=(k * 10.8, k * 10.8))
        ax = fig.add_subplot(111, aspect="equal")
        max_x, min_x = x_rot + dist, x_rot - dist
        max_y, min_y = y_rot + dist, y_rot - dist
        ax.set(xlim=(min_x - 0.1, max_x + 0.1), ylim=(min_y - 0.1, max_y + 0.1))
        ax.axis('off')

        self.point1, = ax.plot(A.x[0], A.y[0], c="k", lw=0.3)  # first point
        self.point2, = ax.plot(B.x[0], B.y[0], c="k", lw=0.3)  # second point

        self.marker1, = ax.plot(A.x[0], A.y[0], c="k", marker="o", ms=2, alpha=1)  # first marker
        self.marker2, = ax.plot(B.x[0], B.y[0], c="k", marker="o", ms=2, alpha=1)  # second marker

        scia_in = scia[0]
        self.scia, = ax.plot([scia_in.x, scia_in.y], lw=0.5)

        self.arm1, = ax.plot([A.x_c, A.x[0]], [A.y_c, A.y[0]], c="k", lw=0.5)  # first arm
        self.arm2, = ax.plot([A.y[0], B.x[0]], [A.y[1], B.y[0]], c="k", lw=0.5)  # second arm

        self.ani = animation.FuncAnimation(fig, self.animate, interval=0, blit=True,
                                           frames=tqdm(range(len(A.x)), desc="Plotting animation"),
                                           repeat_delay=3000,
                                           )
        self.paused = False

        if False:
            path = os.environ["today_path"] + f"/{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.mov"
            self.ani.save(path,
                          fps=60,
                          dpi=200)
            utils.plot_drawing(scia[-1], True, show=True)

        fig.canvas.mpl_connect('button_press_event', self.toggle_pause)

    def animate(self, i):
        self.point1.set_data(A.x[:i], A.y[:i])
        self.point2.set_data(B.x[:i], B.y[:i])
        # self.point2.set_alpha(max(1-i/(tmax), 0.2))
        # self.point1.set_color("k")  # np.random.rand(3,)
        # self.point2.set_color("k")  # np.random.rand(3,)

        self.marker1.set_data(A.x[i], A.y[i])
        # self.marker1.set_color("k")

        self.marker2.set_data(B.x[i], B.y[i])
        # self.marker2.set_color("k")
        # self.marker2.set_alpha(max(1-i/(tmax), 0.2))

        self.arm1.set_data([A.x_c, A.x[i]], [A.y_c, A.y[i]])  # first arm
        self.arm2.set_data([B.x_c[i], B.x[i]], [B.y_c[i], B.y[i]])  # second arm

        scia_i = scia[i]
        self.scia.set_data(scia_i.x[:i], scia_i.y[:i])
        # self.scia.set_color("r")

        alpha = utils.sigmoid(i, a=.7, b=-tmax * 3 / 5)
        self.point1.set_alpha(alpha)
        self.point2.set_alpha(alpha)
        self.arm1.set_alpha(alpha)
        self.arm2.set_alpha(alpha)
        self.marker1.set_alpha(alpha)
        self.marker2.set_alpha(alpha)

        return self.point1, self.point2, self.marker1, self.marker2, self.scia, self.arm1, self.arm2,  # self.pint, self.arm1, self.arm2,  # the comma is needed here

    def toggle_pause(self, *args, **kwargs):
        if self.paused:
            self.ani.resume()
        else:
            self.ani.pause()
        self.paused = not self.paused


pa = Anim()
plt.show()
