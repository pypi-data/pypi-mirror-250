import plottergeist
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

plt.rcParams.update({

    "axes.xmargin": 0.01,
    "axes.ymargin": 0.03,
    "font.size": 15

    })

np.random.seed(42)

ndim = 3
ntoys = 10000
bins = 30

mu, sigma = 5.367, 17.0/1000.0

def pdf(x):
    arg = (x - mu) / sigma
    return np.exp(-arg**2/2.0)

fig, ax, leg, axpull = plottergeist.make_plot(ndim=ndim, pull=True)

def compute_pdfpulls(x_pdf:np.ndarray, y_pdf:np.ndarray, x_hist:np.ndarray,
                     y_hist:np.ndarray, y_l:np.ndarray, y_h:np.ndarray)->np.ndarray:
  """
  This function compares one histogram with a pdf. The pdf is given with two
  arrays x_pdf and y_pdf, these are interpolated (and extrapolated if needed),
  contructing a cubic spline. The histogram takes x_hist (bins), y_hist(counts),
  y_l (counts's lower limit) and y_h (counts' upper limit). The result is a
  pull array between the histogram and the pdf.
  (the pdf is expected to be correctly normalized)
  """
  s = interp1d(x_pdf, y_pdf, kind='cubic', fill_value='extrapolate')
  residuals = y_hist - s(x_hist);
  pulls = np.where(residuals>0, residuals/y_l, residuals/y_h)
  return pulls

for i in range(ndim):
    x = np.random.normal(mu, sigma, ntoys)

    hx = plottergeist.make_hist(x, bins=30)

    px = np.linspace(hx.edges[0], hx.edges[-1], 1000)
    py = pdf(px)

    scale_factor = hx.norm / np.trapz(x=px, y=py)
    py *= scale_factor

    ax[i].errorbar(hx.bins, hx.counts, xerr=hx.xerr, yerr=hx.yerr, fmt=".", color='black', label="Histogram of data")
    ax[i].plot(px, py, linewidth=2, label="Probability density function")
    binwidth = hx.bins[1] - hx.bins[0]
    ax[i].set_ylabel("Candidates / {:.3f}".format(binwidth) + r" GeV/c$^2$")

    axpull[i].set_xlabel(r"$m(K^+ \pi^- K^- \pi^+)$" + r" [GeV/c$^2$]")

    xmin, xmax = axpull[i].get_xlim()

    axpull[i].hlines(y=3.0, xmin=xmin, xmax=xmax, linewidth=1.0, color="lightsteelblue", linestyle="dotted")
    axpull[i].hlines(y=-3.0, xmin=xmin, xmax=xmax, linewidth=1.0, color="lightsteelblue",linestyle="dotted")
    axpull[i].hlines(y=5.0, xmin=xmin, xmax=xmax, linewidth=1.0, color="lightsteelblue", linestyle="dashed")
    axpull[i].hlines(y=-5.0, xmin=xmin, xmax=xmax, linewidth=1.0, color="lightsteelblue", linestyle="dashed")

    hpull = compute_pdfpulls(x_pdf=px, y_pdf=py, x_hist=hx.bins, y_hist=hx.counts, y_l=hx.yerr[0], y_h=hx.yerr[1])
    axpull[i].fill_between(hx.bins, hpull, 0, facecolor="dodgerblue", alpha=1.0)



handles, labels = ax[0].get_legend_handles_labels()

leg.axis("off")
leg.legend(handles, labels, loc='center')

fig.savefig('plot3D.pdf')
