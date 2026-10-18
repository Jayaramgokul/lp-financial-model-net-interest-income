"""03. How the policy variables move the optimum (paper section 5, Figures 5-9).

For each setting of a policy variable the LP is re-solved, as the paper did with
Excel's Solver:
  * collection fractions, in 5% steps, with one of the three fixed at 0
    (the 2-months-after fraction is always the remainder, as in the workbook);
  * payment fractions (month of purchase vs one month after);
  * the minimum cash balance.
Rates are the expected term structure, with the workbook as run (D192 as is), so
the numbers are the paper's; the corrected values are printed alongside.

    python 03_policy_variables.py
"""

import numpy as np
import matplotlib.pyplot as plt

from common import save
from model import TERM_RATES, Policy, Settings, solve

AS_RUN = Settings(rates=TERM_RATES.copy(), keep_d192_slip=True)
CORRECTED = Settings(rates=TERM_RATES.copy(), keep_d192_slip=False)
STEPS = np.round(np.arange(0, 1.0001, 0.05), 2)


def z(cf=(0.1, 0.1, 0.8), pf=(0.0, 1.0), mcb=250, s=AS_RUN):
    return solve(Policy(cf=cf, pf=pf, mcb=mcb), s)[0]


def main():
    print("Collection fractions (month of sale, 1 month after, 2 months after):")
    for cf in [(0.1, 0.1, 0.8), (0.1, 0.6, 0.3), (0.0, 0.0, 1.0), (1.0, 0.0, 0.0)]:
        print(f"  {cf}:  NII {z(cf=cf):8.3f}   (corrected {z(cf=cf, s=CORRECTED):8.3f})")

    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8), sharey=True)
    cases = [("month of sale fixed at 0", lambda t: (0, t, 1 - t), "% collected 1 month after (rest 2 months after)"),
             ("1 month after fixed at 0", lambda t: (t, 0, 1 - t), "% collected in month of sale (rest 2 months after)"),
             ("2 months after fixed at 0", lambda t: (t, 1 - t, 0), "% collected in month of sale (rest 1 month after)")]
    for ax, (title, make, xlabel) in zip(axes, cases):
        vals = [z(cf=make(t)) for t in STEPS]
        ax.plot(STEPS * 100, vals, marker="o", ms=3)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel(xlabel, fontsize=8)
        print(f"  {title}: NII from {vals[0]:.2f} to {vals[-1]:.2f}, monotone: {np.all(np.diff(vals) >= -1e-9)}")
    axes[0].set_ylabel("Optimal NII over six months")
    save(fig, "fig5_7_nii_vs_collection.png")

    grid = np.full((len(STEPS), len(STEPS)), np.nan)
    for i, c0 in enumerate(STEPS):
        for j, c1 in enumerate(STEPS):
            if c0 + c1 <= 1 + 1e-9:
                grid[j, i] = z(cf=(c0, c1, round(1 - c0 - c1, 2)))
    best = np.unravel_index(np.nanargmax(grid), grid.shape)
    print(f"  best over the whole grid: month of sale {STEPS[best[1]]:.0%}, 1 month after {STEPS[best[0]]:.0%}"
          f" -> NII {np.nanmax(grid):.3f}   (paper: 30.615 at 100% in the month of sale)")
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    im = ax.imshow(grid, origin="lower", extent=[-2.5, 102.5, -2.5, 102.5], cmap="viridis")
    ax.set_xlabel("% collected in month of sale")
    ax.set_ylabel("% collected 1 month after")
    ax.set_title("Optimal NII by collection policy")
    fig.colorbar(im, ax=ax)
    save(fig, "collection_policy_grid.png")

    print("\nPayment fractions (month of purchase, 1 month after):")
    pf_vals = [z(pf=(t, 1 - t)) for t in STEPS]
    print(f"  NII over all splits: min {min(pf_vals):.6f}, max {max(pf_vals):.6f}")

    print("\nMinimum cash balance:")
    mcbs = np.arange(0, 501, 50)
    m_vals = [z(mcb=m) for m in mcbs]
    for m, v in zip(mcbs, m_vals):
        print(f"  {m:4d}: NII {v:8.3f}")
    slope = np.polyfit(mcbs, m_vals, 1)[0]
    print(f"  slope: {slope:.4f} NII per unit of minimum cash")
    fig, ax = plt.subplots(figsize=(5.5, 3.6))
    ax.plot(mcbs, m_vals, marker="o")
    ax.set_xlabel("Minimum cash balance")
    ax.set_ylabel("Optimal NII")
    ax.set_title("NII vs minimum cash balance")
    save(fig, "fig9_nii_vs_minimum_cash.png")

    print("\nWhat this shows: the paper's results reproduce. NII rises steadily the faster cash is collected,\n"
          "reaching 30.615 when everything is collected in the month of sale, and falls in a straight line\n"
          "as the minimum cash balance rises. Payment fractions change nothing, to the sixth decimal place.\n"
          "Example 04 explains why each of these patterns is built into the model rather than discovered.")


if __name__ == "__main__":
    main()
