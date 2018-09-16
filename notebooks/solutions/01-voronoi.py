"""Simulated annealing on Voronoi diagrams."""

import random
import colorsys
import numpy as np

from vispy import app
from stochastic.voronoi import Voronoi

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


class SimulatedAnnealing(Voronoi):

    def __init__(self, nb_points, nb_colors, t_i, t_rate):
        Voronoi.__init__(self, nb_points=nb_points, nb_colors=nb_colors)
        self.temp = t_i
        self.prec_eval = self.eval()

        # just for the plot!
        self.i = 0
        self.iter = []
        self.evals = []
        self.best_evals = []
        self.probs = []
        self.best_colors = []

        fig = plt.figure()
        self.ax = fig.gca()
        self.a, = self.ax.semilogy(self.iter, self.evals, '-', color="#aaaaaa")
        self.b, = self.ax.semilogy(self.iter, self.best_evals, '-',
                                   color="red")
        self.ax.set_ylim([1e-7, 1])

        divider = make_axes_locatable(self.ax)
        self.col = divider.append_axes("top", 1.2, pad=0.1, sharex=self.ax)
        self.col.set_ylim([0, 1])

        # make some labels invisible
        plt.setp(self.col.get_xticklabels(), visible=False)

        colors = {int(360*colorsys.rgb_to_hsv(*col)[0]): col
                  for col in self.rgb[0]}

        for i, c in enumerate(self.paired_cm):
            col = colors[int(360*c)]
            col = "#{:02x}{:02x}{:02x}".format(*[int(255*c) for c in col])
            self.best_colors.append(self.col.plot(self.iter, [], color=col)[0])

        plt.show(False)

    def on_timer(self, event):

        old = np.array(self.points)
        new = np.array(old)

        # Basic movement
        for i in random.sample(range(self.nb_points), self.nb_points // 2):
            x = new[i, :] + np.random.uniform(-0.1, 0.1, size=(1, 2))
            if (x.min() < 0 or x.max() > 1):  # Tant pis...
                continue
            new[i, :] = x

        self.points = new
        new_eval = self.eval()

        # just for the plot!
        self.i += 1
        self.iter.append(self.i)
        self.evals.append(new_eval)

        # Simulated annealing
        self.temp = 0.95 * self.temp
        if new_eval > self.prec_eval:
            energy = np.exp((self.prec_eval - new_eval) / self.temp)
            if energy < random.uniform(0, 1):
                self.points = old
                self.best_evals.append(self.prec_eval)
                self.probs.append(self.probs[-1])
                return

        print("\r{:.3g} {:.3g}     ".format(self.temp, new_eval), end="")

        self.prec_eval = new_eval
        self.best_evals.append(self.prec_eval)
        self.probs.append(self.p)

        # just for the plot!
        self.a.set_data(self.iter, self.evals)
        self.b.set_data(self.iter, self.best_evals)
        for i, _ in enumerate(self.p):
            self.best_colors[i].set_data(self.iter, [p[i] for p in self.probs])

        self.ax.set_xlim([0, self.i])
        plt.draw()


if __name__ == "__main__":
    import sys
    try:
        nb_points = int(sys.argv[1])
        nb_colors = int(sys.argv[2])
    except:
        msg = "Usage: python voronoi_recuit.py nb_points nb_colors"
        raise RuntimeError(msg)

    t_i = 0.05
    t_rate = 0.97
    try:
        t_i = float(sys.argv[3])
        t_rate = float(sys.argv[4])
    except:
        pass

    c = SimulatedAnnealing(nb_points, nb_colors, t_i, t_rate)
    app.run()
