"""Computing a Voronoi diagram on the GPU.  """

import random
import numpy as np

from vispy import app
from vispy import gloo

from matplotlib.cm import Paired
from itertools import product
import colorsys


# Voronoi shaders.
VS_voronoi = """
attribute vec2 a_position;

void main() {
    gl_Position = vec4(a_position, 0., 1.);
}
"""

FS_voronoi = """
uniform vec2 u_seeds[nb_points];
uniform vec3 u_colors[nb_points];
uniform vec2 u_screen;

void main() {
    float dist = distance(u_screen * u_seeds[0], gl_FragCoord.xy);
    vec3 color = u_colors[0];
    for (int i = 1; i < nb_points; i++) {
        float current = distance(u_screen * u_seeds[i], gl_FragCoord.xy);
        if (current < dist) {
            color = u_colors[i];
            dist = current;
        }
    }
    gl_FragColor = vec4(color, 1.0);
}
"""

# Seed point shaders.
VS_seeds = """
attribute vec2 a_position;
uniform float u_ps;

void main() {
    gl_Position = vec4(2. * a_position - 1., 0., 1.);
    gl_PointSize = 5. * u_ps;
}
"""

FS_seeds = """
varying vec3 v_color;
void main() {
    gl_FragColor = vec4(1., 1., 1., 1.);
}
"""


class immutable_array(np.ndarray):

    def __setitem__(self, *args, **kwargs):
        import sys
        msg = """
        YOU WILL ENCOUNTER WEIRD BEHAVIOURS!!

        Make a copy of the array before anything:
        >>> p = np.array(self.points)

        then use the proper setter:
        >>> self.points = p
        """
        print(msg)
        sys.exit(2)


class Voronoi(app.Canvas):

    def __init__(self, nb_points, nb_colors):

        app.Canvas.__init__(self, size=(250, 250), title='Voronoi diagram',
                            keys='interactive')

        self.nb_points = nb_points
        self.ps = self.pixel_scale

        self.seeds = np.random.uniform(0, 1.0 * self.ps,
                                       size=(nb_points, 2)).astype(np.float32)

        self.rgb = Paired(np.linspace(0, 1, nb_colors))[np.newaxis, :, :3]

        self.colors = np.array([random.choice(self.rgb[0])
                                for i in range(nb_points)]).astype(np.float32)

        self.paired_cm = [colorsys.rgb_to_hsv(*self.colors[i])[0]
                          for i in range(nb_points)]
        self.paired_cm = np.array(list(set(self.paired_cm)))

        self.nb_colors = len(self.paired_cm)
        print("{} colors".format(self.nb_colors))

        # Set Voronoi program.
        self.program_v = gloo.Program(
            VS_voronoi, FS_voronoi.replace('nb_points', str(nb_points)))
        self.program_v['a_position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
        # HACK: work-around a bug related to uniform arrays until
        # issue #345 is solved.
        for i in range(nb_points):
            self.program_v['u_seeds[%d]' % i] = self.seeds[i, :]
            self.program_v['u_colors[%d]' % i] = self.colors[i, :]

        # Set seed points program.
        self.program_s = gloo.Program(VS_seeds, FS_seeds)
        self.program_s['a_position'] = self.seeds
        self.program_s['u_ps'] = self.ps

        self._timer = app.Timer('auto', connect=self.on_timer, start=True)

        self.activate_zoom()
        self.show()

    def eval(self):
        maps = self.render()
        maps_hue = np.array([colorsys.rgb_to_hsv(*maps[i, j][:3])[0]
                             for i, j in product(range(maps.shape[0]),
                                                 range(maps.shape[1]))])
        counts = [np.sum(np.abs(maps_hue - current_color) < 1e-6)
                  for current_color in self.paired_cm]
        counts = np.array(counts)
        self.p = counts / counts.sum()
        return np.exp((self.p * np.log(self.p)).sum()) - 1 / self.nb_colors

    @property
    def points(self):
        return self.seeds.view(immutable_array)

    @points.setter
    def points(self, points):
        self.seeds = points
        self.program_s['a_position'] = self.seeds
        for i in range(self.nb_points):
            self.program_v['u_seeds[%d]' % i] = self.seeds[i, :]
        self.update()

    def on_timer(self, event):
        pass

    def on_draw(self, event):
        gloo.clear()
        self.program_v.draw('triangle_strip')
        self.program_s.draw('points')

    def on_resize(self, event):
        self.activate_zoom()

    def activate_zoom(self):
        self.width, self.height = self.size
        gloo.set_viewport(0, 0, *self.physical_size)
        self.program_v['u_screen'] = self.physical_size


if __name__ == "__main__":
    c = Voronoi()
    app.run()
