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
ticc = 2  # thickness factor

tmax = 300
dt = 0.05  # 0.05
video_lenght = 30  # in sec
x_rot, y_rot = -0.7, -0.5
T_foglio = -3000

tim = utils.timeline(t_max=tmax, dt=dt)
u = tim / tmax  # normalized time

r1 = 4 * np.sqrt(u + 0.3)
r2 = 1.3 * np.sin(np.pi * u) ** 2

# FASORE SU FASORE - B sopra ad A
A = Phasor(tim, x_cent=0, y_cent=0, radius=r1, period=170, phase=0)
B = Phasor(tim, x_cent=A.x, y_cent=A.y, radius=r2, period=3, phase=0)
# C = B.rotate(x_rot, y_rot, t=T_foglio)
# pintograph = Pintograph(phasor1=phasor1, phasor2=phasor2, arm1=5, arm2=5, extension=0)


curva = B
scia = utils.rotate_live(curva, x_rot, y_rot, T=T_foglio)
dist = max(np.sqrt((curva.x - x_rot) ** 2 + (curva.y - y_rot) ** 2))


class Anim:
    def __init__(self):
        fig = plt.figure(figsize=(k * 10.8, k * 10.8))
        self.ax = fig.add_subplot(111, aspect="equal")
        self.max_x, self.min_x = x_rot + dist, x_rot - dist
        self.max_y, self.min_y = y_rot + dist, y_rot - dist
        self.ax.set(xlim=(self.min_x - 0.1, self.max_x + 0.1), ylim=(self.min_y - 0.1, self.max_y + 0.1))
        self.ax.axis('off')
        plt.tight_layout()

        # self.pivot = ax.plot(x_rot,y_rot, c="k", marker="x")   # pivot for rotation

        self.point1, = self.ax.plot(A.x[0], A.y[0], c="b", lw=ticc * 0.3)  # first point
        self.point2, = self.ax.plot(B.x[0], B.y[0], c="k", lw=ticc * 0.3)  # second point

        self.marker1, = self.ax.plot(A.x[0], A.y[0], c="k", marker="o", ms=2, alpha=1)  # first marker
        self.marker2, = self.ax.plot(B.x[0], B.y[0], c="k", marker="o", ms=2, alpha=1)  # second marker

        scia_in = scia[0]
        self.scia, = self.ax.plot([scia_in.x, scia_in.y], c="k", lw=ticc * 1)

        self.arm1, = self.ax.plot([A.x_c, A.x[0]], [A.y_c, A.y[0]], c="k", lw=ticc * 0.5)  # first arm
        self.arm2, = self.ax.plot([A.x[0], B.x[0]], [A.y[1], B.y[0]], c="k", lw=ticc * 0.5)  # second arm

        self.ani = animation.FuncAnimation(fig, self.animate, interval=0, blit=False,
                                           frames=tqdm(range(len(A.x)), desc="Plotting animation"),
                                           repeat_delay=3000,
                                           )
        self.paused = False

        if True:
            path = os.environ["today_path"] + f"/{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.mov"
            self.ani.save(path,
                          fps=(tmax // (dt * video_lenght)),
                          dpi=100)
            utils.plot_drawing(scia[-1], True, show=False)

        fig.canvas.mpl_connect('button_press_event', self.toggle_pause)

    def animate(self, i):

        self.point1.set_data(A.x[:i], A.y[:i])
        # self.point2.set_data(B.x[:i], B.y[:i])
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
        self.scia.set_data(scia_i.x, scia_i.y)
        # self.ax.set(xlim=(A.x[i] -1 , A.x[i] + 1), ylim=(A.y[i] - 1, A.y[i] + 1))

        # self.scia.set_color("r")

        alpha = utils.sigmoid(i, a=.7, b=- (tmax / dt) * 3 / 5)
        self.point1.set_alpha(alpha)
        self.point2.set_alpha(alpha)
        self.arm1.set_alpha(alpha)
        self.arm2.set_alpha(alpha)
        self.marker1.set_alpha(alpha)
        self.marker2.set_alpha(alpha)

        return self.point1, self.point2, self.marker1, self.marker2, self.scia, self.arm1, self.arm2, self.ax,  # self.pint, self.arm1, self.arm2,  # the comma is needed here

    def toggle_pause(self, *args, **kwargs):
        if self.paused:
            self.ani.resume()
        else:
            self.ani.pause()
        self.paused = not self.paused


pa = Anim()
plt.show()
