import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, datetime
from pathlib import Path
import os
import utils
from tqdm import tqdm
from drawings.Phasor import Phasor, Pintograph, Pendulum

matplotlib.use('TkAgg')
draw_path = Path("images")
draw_path.mkdir(exist_ok=True)
today_path = draw_path / date.today().strftime("%d-%m-%y")
today_path.mkdir(exist_ok=True)
os.environ["today_path"] = str(today_path)

k = 0.7  # scale factor

tmax = 300
dt = 0.2
x_rot, y_rot = 2, 2
T_foglio = 100

tim = utils.timeline(t_max=tmax, dt=dt)
u = tim / tmax           # normalized time

r1 = 5 + np.sin(2*np.pi/tmax * u)
r2 = 1.3 * np.sin(np.pi * u) ** 2

# TEST
P = Phasor(tim, x_cent=0, y_cent=0, radius=1, period=tmax, phase=0)
A = Pendulum(tim, x_cent=P.x, y_cent=P.y, radius=r1, max_angle=np.pi/6, period=tmax/3,  phase=-1)
B = Pendulum(tim, x_cent=A.x, y_cent=A.y, radius=3, max_angle=np.pi/4, period=tmax/9,  phase=2)

# pintograph = Pintograph(phasor1=phasor1, phasor2=phasor2, arm1=5, arm2=5, extension=0)

#  CACCA
curva = B
scia = utils.rotate_live(curva, x_rot, y_rot, T=T_foglio)
dist = max(np.sqrt((curva.x - x_rot) ** 2 + (curva.y - y_rot) ** 2))



class Anim:
    def __init__(self):
        fig = plt.figure(figsize=(k * 10.8, k * 10.8))
        ax = fig.add_subplot(111, aspect="equal")
        max_x, min_x = x_rot + dist, x_rot - dist
        max_y, min_y = y_rot + dist, y_rot - dist
        ax.set(xlim=(min_x - 0.1, max_x + 0.1), ylim=(min_y - 0.1, max_y + 0.1))
        ax.axis('off')
        self.pivot = ax.plot(x_rot,y_rot, c="k", marker=".")   # pivot for rotation

        # cerchio1 = utils.Circle(A.x_c, A.y_c, A.r[0])
        # self.disc1, = ax.plot(cerchio1[0][:], cerchio1[1][:],"--")

        # self.point1, = ax.plot(A.x[0], A.y[0], c="k", lw=0.3)  # first point
        self.point2, = ax.plot(B.x[0], B.y[0], c="k", lw=0.3, ls="--")  # second point

        self.marker1, = ax.plot(A.x[0], A.y[0], c="k", marker="o", ms=2, alpha=1)  # first marker
        self.marker2, = ax.plot(B.x[0], B.y[0], c="k", marker="o", ms=2, alpha=1)  # second marker

        scia_in = scia[0]
        self.scia, = ax.plot([scia_in.x, scia_in.y], lw=0.8)

        self.arm0, = ax.plot( [P.x_c, P.x[0]], [P.y_c, P.y[0]], c="k", lw=0.5)
        self.arm1, = ax.plot( [A.x_c[0], A.x[0]], [A.y_c[0], A.y[0]], c="k", lw=0.7)  # first arm
        self.arm2, = ax.plot([B.x_c[0], B.x[0]], [B.y_c[0], B.y[0]], c="k", lw=0.7)  # second arm

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
        # cerchio = utils.Circle(A.x_c, A.y_c, A.r[i])
        # # self.disc1.set_data(cerchio[0][:], cerchio[1][:])
        # self.disc1, = ax.plot(cerchio[0][:], cerchio[1][:], "--")

        # Update points

        # self.point1.set_data(A.x[:i], A.y[:i])
        self.point2.set_data(B.x[:i], B.y[:i])
        # self.point2.set_alpha(max(1-i/(tmax), 0.2))
        # self.point1.set_color("k")  # np.random.rand(3,)
        self.point2.set_color("k")  # np.random.rand(3,)

        self.marker1.set_data(A.x[i], A.y[i])
        # self.marker1.set_color("k")

        self.marker2.set_data(B.x[i], B.y[i])
        self.marker2.set_color("k")
        # self.marker2.set_alpha(max(1-i/(tmax), 0.2))

        self.arm0.set_data([P.x_c, P.x[i]], [P.y_c, P.y[i]])
        self.arm1.set_data([A.x_c[i], A.x[i]], [A.y_c[i], A.y[i]])  # first arm
        self.arm2.set_data([B.x_c[i], B.x[i]], [B.y_c[i], B.y[i]])  # second arm

        scia_i = scia[i]
        self.scia.set_data(scia_i.x[:i], scia_i.y[:i])
        self.scia.set_color("r")

        # alpha = utils.sigmoid(i, a=.7, b= 100 * 3 / 5)
        alpha = max(1 - u[i], 0.5)
        # self.point1.set_alpha(alpha)
        # self.point2.set_alpha(alpha)
        self.arm1.set_alpha(alpha)
        # self.arm2.set_alpha(alpha)
        self.marker1.set_alpha(alpha)
        # self.marker2.set_alpha(alpha)

        return self.marker1, self.arm0, self.arm1, self.scia,  self.point2, self.arm2, self.marker2,  #self.point1 self.disc1,  # the comma is needed here

    def toggle_pause(self, *args, **kwargs):
        if self.paused:
            self.ani.resume()
        else:
            self.ani.pause()
        self.paused = not self.paused


pa = Anim()
plt.show()
