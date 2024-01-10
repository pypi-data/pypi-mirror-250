import plottergeist
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

np.random.seed(42)

ndim = 1
bins = 30

ntoys_sig = 10000
ntoys_bkg = 6000
ntoys_comb = 3000

ll = 5.165
ul = 5.5

mu_sig, sigma_sig = 5.367, 17.0/1000.0
mu_bkg, sigma_bkg = 5.270, 21.0/1000.0
tau_comb = 0.06

def pdf_gauss(x, mu, sigma):
    arg = (x - mu) / sigma
    return np.exp(-arg**2/2.0)

def pdf_expo(x, tau):
    return np.exp(-x/tau)

def generate_expo(tau, ll, ul, size):
    u = np.random.uniform(0.0, 1.0, size=size)
    return -tau*np.log(np.exp(-ll/tau) +u*(np.exp(-ul/tau) - np.exp(-ll/tau)))

# plottergeist.fig_creator.FIGSIZE = (10,8)

fig, ax, axpull = plottergeist.make_plot(ndim=ndim, pull=True)

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

x_sig = np.random.normal(mu_sig, sigma_sig, ntoys_sig)
x_bkg = np.random.normal(mu_bkg, sigma_bkg, ntoys_bkg)
x_comb = generate_expo(tau_comb, ll, ul, ntoys_comb)

x_sig = x_sig[np.logical_and(x_sig>ll, x_sig<ul)]
x_bkg = x_bkg[np.logical_and(x_bkg>ll, x_bkg<ul)]
x_comb = x_comb[np.logical_and(x_comb>ll, x_comb<ul)]

print("Size sig: ", len(x_sig))
print("Size bkg: ", len(x_bkg))
print("Size comb: ", len(x_comb))

ntot = len(x_sig) + len(x_bkg) + len(x_comb)
f_sig = len(x_sig) / ntot
f_bkg = len(x_bkg) / ntot
f_comb = 1.0 - f_sig - f_bkg

x = np.concatenate([x_sig, x_bkg, x_comb])


hx = plottergeist.make_hist(x, bins=30)

px = np.linspace(hx.edges[0], hx.edges[-1], 1000)

py_sig = pdf_gauss(px, mu_sig, sigma_sig)
py_sig /= np.trapz(x=px, y=py_sig)

py_bkg = pdf_gauss(px, mu_bkg, sigma_bkg)
py_bkg /= np.trapz(x=px, y=py_bkg)

py_comb = pdf_expo(px, tau_comb)
py_comb /= np.trapz(x=px, y=py_comb)

py = f_sig*py_sig + f_bkg*py_bkg + f_comb*py_comb

scale_factor = hx.norm / np.trapz(x=px, y=py)
py *= scale_factor

py_sig *= scale_factor * f_sig
py_bkg *= scale_factor * f_bkg
py_comb *= scale_factor * f_comb

ax.plot(px, py, linewidth=2, label="Total probability density function")
ax.plot(px, py_sig, linewidth=1, linestyle='--', label="Signal")
ax.plot(px, py_bkg, linewidth=1, linestyle='--', label="Background")
ax.plot(px, py_comb, linewidth=1, linestyle='--', label="Combinatorial")
ax.errorbar(hx.bins, hx.counts, xerr=hx.xerr, yerr=hx.yerr, fmt=".", color='black', label="Histogram of data")
binwidth = hx.bins[1] - hx.bins[0]
ax.set_ylabel("Candidates / {:.3f}".format(binwidth) + r" GeV/c$^2$")
ax.set_title(r"a$a$ b$b$ c$c$ d$d$ e$e$")

axpull.set_xlabel(r"$m(K^+ \pi^- K^- \pi^+)$" + r" [GeV/c$^2$]")

# xmin, xmax = axpull.get_xlim()
xmin, xmax = hx.edges[0], hx.edges[-1]
axpull.hlines(y=3.0, xmin=xmin, xmax=xmax, linewidth=1.0, color="lightsteelblue", linestyle="dotted")
axpull.hlines(y=-3.0, xmin=xmin, xmax=xmax, linewidth=1.0, color="lightsteelblue",linestyle="dotted")
axpull.hlines(y=5.0, xmin=xmin, xmax=xmax, linewidth=1.0, color="lightsteelblue", linestyle="dashed")
axpull.hlines(y=-5.0, xmin=xmin, xmax=xmax, linewidth=1.0, color="lightsteelblue", linestyle="dashed")

hpull = compute_pdfpulls(x_pdf=px, y_pdf=py, x_hist=hx.bins, y_hist=hx.counts, y_l=hx.yerr[0], y_h=hx.yerr[1])
axpull.fill_between(hx.bins, hpull, 0, facecolor="dodgerblue", alpha=1.0)




ax.legend(loc='best')

fig.savefig('plot1D.pdf')
