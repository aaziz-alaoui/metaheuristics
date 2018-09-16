
import numpy as np

from matplotlib.animation import FuncAnimation

def sa_animation(fig, ax, coords):

    coords = np.array(coords)
    C = [(0,0,0,.9)]

    scat = ax.scatter(coords[:1,0], coords[:1,1], facecolor=C, edgecolor=C)

    ax.set_xlim(0,1), ax.set_xticks([])
    ax.set_ylim(0,1), ax.set_yticks([])

    line, = ax.plot([], [], 'o', linestyle='-', color="#cb4154")
    xbest, ybest, l = [], [], -1

    i = 0

    def update(frame):
        nonlocal coords, xbest, ybest, l
        if frame == 0:
            xbest, ybest, l = [], [], -1
        if frame > 50:
            C = np.ones((50, 4))*(0,0,0,.9)
            C[:,3]= np.linspace(0,1,50)
            scat.set_offsets(coords[frame-50:frame, :2])
        else:
            C = np.ones((frame, 4))*(0, 0, 0, .9)
            C[:,3] = np.linspace(0, 1, frame)
            scat.set_offsets(coords[:frame, :2])
        scat.set_facecolor(C)
        scat.set_edgecolor(C)
        if frame <= 2000:
            if l < 0 or xbest[l] != coords[frame, 2] or ybest[l] != coords[frame, 3]:
                l += 1
                xbest.append(coords[frame, 2])
                ybest.append(coords[frame, 3])
                line.set_data(xbest, ybest)
        return scat

    return FuncAnimation(fig, update, coords.shape[0], interval=100,
                         repeat=False)
