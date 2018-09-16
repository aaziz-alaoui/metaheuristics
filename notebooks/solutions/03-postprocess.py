res = solution[0].reshape((n, 2))

# rotate it so that Copenhagen is above Rome
south, north = cities.index("Rome"), cities.index("Copenhagen")
d = res[north, :] - res[south, :]
rotate = np.arctan2(d[1], d[0]) - np.pi/2
mat_rotate = np.array([[np.cos(rotate), -np.sin(rotate)],
                       [np.sin(rotate), np.cos(rotate)]])
res = res @ mat_rotate  # matrix product, from Python 3.5

# mirror so that Reykjavik is west of Moscow
west, east = cities.index("Reykjavik"), cities.index("Moscow")
mirror = False
if res[west, 0] > res[east, 0]:
    mirror = True
    res[:, 0] *= -1

# apply the transformation to the full track
track = [p.reshape((n, 2)) @ mat_rotate for p in solution[1]]
if mirror == True:
    track = [p * np.array([-1, 1]) for p in track]
