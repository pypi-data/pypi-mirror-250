import plottergeist
import numpy as np

fig, ax = plottergeist.make_plot(ndim=1)


for i in range(10):
    x = [i for _ in range(1000)]
    y = np.linspace(0, 1, 1000)
    ax.plot(x, y, linewidth=2)

fig.savefig('colors.pdf')
