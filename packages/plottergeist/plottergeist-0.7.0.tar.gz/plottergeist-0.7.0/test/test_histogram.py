import numpy as np
import plottergeist

pulls = []

for i in range(100):
    x = np.random.normal(0, 1, 1000000)
    y = np.random.normal(0, 1, 1000000)
    bins = 10

    h_ptg = plottergeist.make_hist(x, bins=bins)
    h_np = np.histogram(y, bins=h_ptg.edges)[0]

    p = plottergeist.compute_pulls(ref_counts=h_np, counts=h_ptg.counts, counts_l=h_ptg.yerr[0], counts_h=h_ptg.yerr[1])

    pulls.append(np.sum(p))

print(max(abs(np.array(pulls))))
