"""Generate the Ashraf-Galor figure the project is missing.

AG's headline is a HUMP-SHAPED (quadratic) IV effect of genetic diversity on
log population density in 1500 CE. A forest plot would misrepresent it, so we
draw the fitted hump from the replicated quadratic-2SLS coefficients
(adiv = +285.19, adiv_sqr = -206.576), mark the optimal-diversity turning
point (0.690), and rug the 21 in-sample countries' diversity values.

The linear-PLIV extension is a different, non-comparable quantity (a single
average slope), so it is NOT drawn here.

Writes forest_plot.png/.pdf into the AG project's paper/figures/ so the page
generator copies it like every other paper.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]   # recast_fable/
AG = ROOT / "phase2" / "projects" / "ashraf_galor_2013"
OUT = AG / "paper" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

B1, B2 = 285.19, -206.576          # replicated quadratic-2SLS coefficients
TP = -B1 / (2 * B2)                # optimal diversity = 0.690

# in-sample diversity values (N=21 limited HGDP-CEPH sample)
df = pd.read_stata(AG / "raw_data" / "country.dta")
adiv = df.query("cleanlim == 1")["adiv"].dropna().to_numpy()
lo, hi = float(adiv.min()), float(adiv.max())

x = np.linspace(lo, hi, 400)
# diversity contribution to log pop density, recentred to its in-range minimum
g = B1 * x + B2 * x**2
g = g - g.min()

fig, ax = plt.subplots(figsize=(7.2, 4.4))
ax.plot(x, g, color="#2c5f8a", lw=2.4, label="Fitted quadratic-2SLS effect")
ax.axvline(TP, color="#b5462f", ls="--", lw=1.4)
ax.annotate(f"optimal diversity ≈ {TP:.3f}",
            xy=(TP, g.max()), xytext=(TP + 0.01, g.max() * 0.62),
            color="#b5462f", fontsize=10)
# rug of the 21 in-sample countries
ax.plot(adiv, np.full_like(adiv, -g.max() * 0.03), "|", color="#6c757d",
        ms=10, mew=1.2, label="21 countries (in-sample)")
ax.set_xlabel("Predicted genetic diversity (adiv)")
ax.set_ylabel("Contribution to log population density, 1500 CE")
ax.set_title("Ashraf–Galor (2013): the hump-shaped IV effect of genetic diversity")
ax.legend(loc="lower center", fontsize=9, frameon=False)
ax.margins(x=0.02)
fig.tight_layout()
for ext in ("png", "pdf"):
    fig.savefig(OUT / f"forest_plot.{ext}", dpi=150, bbox_inches="tight")
print(f"AG figure written to {OUT} (turning point {TP:.3f}, adiv in [{lo:.3f}, {hi:.3f}], n={len(adiv)})")
