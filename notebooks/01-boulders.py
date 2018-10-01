import numpy as np

n_boulders = 150
boulders = np.random.uniform(0., 1., (n_boulders, 3))
boulders[:, 2] = 1 / (3 ** np.random.choice(range(2, 4), (n_boulders)))


def eval_boulders(x, y, boulders=boulders):
    res = 0
    for i in range(boulders.shape[0]):
        eval_ = (
            (x - boulders[i, 0]) ** 2
            + (y - boulders[i, 1]) ** 2
            - boulders[i, 2] ** 2
        )
        if eval_ < 0:
            res += eval_
    return res


X, Y = np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100))
Z = np.zeros(X.shape)

for i in range(n_boulders):
    eval_ = (
        (X - boulders[i, 0]) ** 2
        + (Y - boulders[i, 1]) ** 2
        - boulders[i, 2] ** 2
    )
    Z[eval_ < 0] += eval_[eval_ < 0]
