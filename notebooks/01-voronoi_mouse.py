# Squelette d'un fichier .py indépendant

import numpy as np
from vispy import app

from stochastic.voronoi import Voronoi

class Discover(Voronoi):

    def __init__(self, nb_points, nb_colors):
        Voronoi.__init__(self, nb_points=nb_points, nb_colors=nb_colors)
        self.current = 0

    def on_mouse_move(self, event):
        x, y = event.pos
        x, y = x / float(self.width), 1 - y / float(self.height)

        # Ne pas écrire self.points[self.current, :] = ...
        # (sinon le programme quitte proprement!)
        new = np.array(self.points)
        new[self.current, :] = x * self.ps, y * self.ps
        self.points = new

    def on_mouse_press(self, event):
        self.current = (self.current + 1) % self.nb_points

c = Discover(10, 30)
app.run()
