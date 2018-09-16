t0 = 0.1

p0 = np.random.uniform(0, 1., 2)
e = eval_boulders(*p0)

best = p0
best_e = e
parcours = []

evals = []
best_evals = []

for i in range(10000):

    t0 *= 0.97
    delta = np.random.uniform(-0.1, 0.1, 2)
    next_ = p0 + delta

    while next_.min() < 0 or next_.max() > 1:
        delta = np.random.uniform(-0.15, 0.15, 2)
        next_ = p0 + delta

    e_next = eval_boulders(*next_)

    if e_next > e:
        if np.exp((e - e_next)/t0) < np.random.uniform(0., 1.):
            continue

    if e_next < best_e:
        best = p0
        best_e = e_next

    best_evals.append(best_e)
    evals.append(e_next)

    e = e_next
    p0 = next_
    parcours.append(np.r_[p0, best])


plt.plot(evals)
plt.plot(best_evals)
