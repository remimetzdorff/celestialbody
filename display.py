##########################################################################
# display.py offers some examples to use celestialbody
# Copyright (C) 2021 Rémi Metzdorff (remi.metzdorff@orange.fr)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
##########################################################################

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import datetime
from celestialbody import CelestialBody

def prepare_data(names, ref=None, start=None, stop=None, step=None):
    Xs, Ys, Zs, dates = [], [], [], []
    for name in names:
        body = CelestialBody(name)
        X, Y, Z, _ = body.trajectory(start=start, stop=stop, step=step)
        dates.append(body.data("date",start=start, stop=stop, step=step))
        Xs.append(X)
        Ys.append(Y)
        Zs.append(Z)
    X_sun, Y_sun, Z_sun = np.zeros(len(X)), np.zeros(len(X)), np.zeros(len(X))
    Xs.append(X_sun)
    Ys.append(Y_sun)
    Zs.append(Z_sun)
    names.append("Sun")
    if ref not in names:
        print("ref must be in names!")
        return
    else:
        for i, name in enumerate(names):
            if name == ref:
                Xs.append(Xs[i])
                Ys.append(Ys[i])
                Zs.append(Zs[i])
        names.append(ref)

    Xs_ref, Ys_ref, Zs_ref = [], [], []
    for X, Y, Z in zip(Xs, Ys, Zs):
        Xs_ref.append(X - Xs[-1])
        Ys_ref.append(Y - Ys[-1])
        Zs_ref.append(Z - Zs[-1])

    coord_sun = [Xs, Ys, Zs]
    coord_ref = [Xs_ref, Ys_ref, Zs_ref]
    return names, coord_sun, coord_ref, dates


def frame_of_reference(names, ref=None, start=None, stop=None, step=None):
    """
    Affiche deux graphes contenant les trajectoires des objets contenus dans la liste names :
        - le premier dans le référentiel écliptique héliocentrique
        - le deuxième dans le référentiel écliptique lié à l'objet nommé ref
    """
    names, coord_sun, coord_ref, dates = prepare_data(names, ref=ref, start = start, stop = stop, step = step)

    fig = plt.figure(figsize=(16, 8))
    sps = (1, 2)
    ax1 = plt.subplot2grid(sps, (0, 0))
    ax2 = plt.subplot2grid(sps, (0, 1))

    for coord, ax in zip([coord_sun, coord_ref], [ax1, ax2]):
        Xs, Ys, Zs = coord
        i = 0
        for name, X, Y, Z in zip(names[:-1], Xs[:-1], Ys[:-1], Zs[:-1]):
            if name == "Sun":
                color = "gold"
            else:
                color = "C"+str(i)
            position,   = ax.plot(X[0], Y[0], "o", color=color, label=name)
            trajectory, = ax.plot(X, Y, "-", color=color, linewidth=.5)
            i += 1

        ax.set_title(dates[0][0].date())
        ax.set_xlabel("X (au)")
        ax.set_ylabel("Y (au)")
        ax.set_aspect("equal")
        ax.legend()
    ax1.set_xlim(ax2.get_xlim())
    ax1.set_ylim(ax2.get_ylim())
    return fig


def plot_bodies(names, date=datetime.datetime.today()):

    fig = plt.figure(figsize=(16, 8))
    sps = (1, 2)
    ax1 = plt.subplot2grid(sps, (0, 0))
    ax2 = plt.subplot2grid(sps, (0, 1), projection='3d')

    ax1.scatter(0, 0, marker="o", color="gold")
    ax1.annotate("Soleil", (0, 0), color="gold", textcoords="offset points", xytext=(2, 2),
                 fontsize="medium", horizontalalignment='left', verticalalignment='bottom', alpha=1)
    ax2.scatter(0, 0, 0, marker="o", color="gold")
    ax2.text(0, 0, 0, "Soleil", fontsize="medium", color="gold", horizontalalignment='left', verticalalignment='bottom')

    for i, name in enumerate(names):
        body = CelestialBody(name)
        body.date = date

        x, y, z = body.position
        X, Y, Z = body.orbit

        color = "C" + str(i)

        ax1.scatter(x, y, marker="o", color=color)
        ax1.plot(X, Y, color=color, linewidth=.5)
        ax1.annotate(body.name, (x, y), color=color, textcoords="offset points", xytext=(2, 2),
                     fontsize="medium", horizontalalignment='left', verticalalignment='bottom', alpha=1)

        ax2.scatter(x, y, z, marker="o", color=color)
        ax2.plot(X, Y, Z, color=color, linewidth=.5)
        ax2.text(x, y, z, body.name, fontsize="medium", color=color, horizontalalignment='left',
                 verticalalignment='bottom')

    # Gestion des limites, etc.
    ax1.set_aspect("equal")

    ax2.set_zlim(ax2.get_xlim())
    plt.tight_layout()

    for ax in [ax1, ax2]:
        ax.set_xlabel("X (au)")
        ax.set_ylabel("Y (au)")
        ax.set_title(date.date())
    ax2.set_zlabel("Z (au)")

    return fig


def animate_bodies(names, ref=None, start=None, stop=None, step=None, show_speed=False):

    names, coord_sun, coord_ref, dates = prepare_data(names, ref=ref, start=start, stop=stop, step=step)

    fig = plt.figure(figsize=(8, 8))
    ax = plt.subplot2grid((1,1), (0, 0))

    Xs, Ys, Zs = coord_ref

    for X, Y in zip(Xs, Ys):
        ax.plot(X,Y)
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    ax.clear()

    positions, trajectories, speeds = [], [], []
    for i, name in enumerate(names[:-1]):
        if name == "Sun":
            color = "gold"
        else:
            color = "C"+str(i)
        position,   = ax.plot([], [], "o", color=color, label=name)
        trajectory, = ax.plot([], [], "-", color=color, linewidth=.5)
        speed       = ax.quiver(0, 0, 0, 0, color=color, alpha=.5, width=.005, angles='xy', scale_units='xy', scale=1)
        positions.append(position)
        trajectories.append(trajectory)
        speeds.append(speed)

    def init():
        for position, trajectory in zip(positions, trajectories):
            position.set_data([], [])
            trajectory.set_data([], [])
        return

    def animate(i):
        for X, Y, position, trajectory, speed in zip(Xs, Ys, positions, trajectories, speeds):
            ax.set_title(dates[0][i].date())
            position.set_data(X[i], Y[i])
            trajectory.set_data(X[:i], Y[:i])
            if i < len(X) - 1 and show_speed:
                scale = 10
                u, v = scale * (X[i + 1] - X[i]) / step, scale * (Y[i + 1] - Y[i]) / step
                speed.set_UVC(u, v)
                speed.set_offsets((X[i], Y[i]))
        return

    ax.legend(loc="upper left")
    ax.set_aspect("equal")
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel("X (au)")
    ax.set_ylabel("Y (au)")

    anim = animation.FuncAnimation(fig, animate, frames=len(Xs[0]) - 1, interval=1e3 / 25, init_func=init)
    return anim


def animate_swept_area(name, start=None, stop=None, swept_days=None, category=None, speed="normal"):
    body = CelestialBody(name, category=category)
    if start is None:
        if body.e > .25:
            start = body.perihelion_passage_date - datetime.timedelta(days=body.period/10)
        else:
            start = datetime.datetime.today()
    if stop is None:
        stop = start + 5 * datetime.timedelta(days=body.period)
    if swept_days is None:
        swept_days = body.period / 20
    if speed == "fast":
        step = swept_days / (2 ** 4)
    elif speed == "normal":
        step = swept_days / (2 ** 5)
    elif speed == "slow":
        step = swept_days / (2 ** 6)
    data = body.data("position", start=start, stop=stop, step=step)
    dates = body.data("date", start=start, stop=stop, step=step)
    orbit = body.orbit
    X = data[:, 0]
    Y = data[:, 1]

    n = int(swept_days / step)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal")
    sun       = ax.scatter(0,0, color="gold")
    orbit,    = ax.plot(orbit[0], orbit[1], "C0", lw=1)
    position, = ax.plot(0, 0, "oC0")
    radius,   = ax.plot(0, 0, "C0")
    fill,     = ax.fill(np.zeros(n + 1), np.zeros(n + 1), alpha=.25, color="C0")
    ax.set_xlabel("X (au)")
    ax.set_ylabel("Y (au)")

    def animate(j):
        i = n+j
        ax.set_title(dates[i].date())
        position.set_data(X[i], Y[i])
        radius.set_data([0, X[i]], [0, Y[i]])
        # Some dark magic happens here
        # https://brushingupscience.com/2019/08/01/elaborate-matplotlib-animations/
        path = fill.get_path()
        verts = fill.get_path().vertices
        verts[1:n + 1, 0] = X[i - n + 2:i + 2]
        verts[1:n + 1, 1] = Y[i - n + 2:i + 2]

    fps = 25
    anim = animation.FuncAnimation(fig, animate, interval=1000/fps, frames=len(X)-n, repeat=True)

    return anim