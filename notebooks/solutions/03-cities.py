def func(*x):
    """ Compute the function to minimise.

    Vector reshaped for more readability.
    """
    res = 0
    x = np.array(x)
    x = x.reshape((n, 2))
    for i in range(n):
        for j in range(i+1, n):
            (x1, y1), (x2, y2) = x[i, :], x[j, :]
            delta = (x2 - x1)**2 + (y2 - y1)**2 - distances[i, j]**2
            res += delta**2
    return res

# Ça va servir pour résoudre en BFGS

def func_der(*x):
    """ Derivative of the preceding function.

    Note: (f \circ g)' = g' \times f' \circ g
    Vector reshaped for more readability.
    """
    res = np.zeros((n, 2))
    x = np.array(x)
    x = x.reshape((n, 2))
    for i in range(n):
        for j in range(i+1, n):
            (x1, y1), (x2, y2) = x[i, :], x[j, :]
            delta = (x2 - x1)**2 + (y2 - y1)**2 - distances[i, j]**2
            res[i, 0] += 4 * (x1 - x2) * delta
            res[i, 1] += 4 * (y1 - y2) * delta
            res[j, 0] += 4 * (x2 - x1) * delta
            res[j, 1] += 4 * (y2 - y1) * delta
    return np.ravel(res)

# on tire au hasard une solution initiale
x0 = np.random.normal(size=(n, 2))

# On normalise la solution initiale pour une animation plus lisible (pas obligé)
l1, l2 = np.meshgrid(x0[:,0], x0[:,0])
r1, r2 = np.meshgrid(x0[:,1], x0[:,1])

x0 /= np.linalg.norm(np.sqrt((l1 - l2)**2 + (r1 - r2)**2))
