"""02. Validating the model on the textbook problem (paper section 4.1).

The paper validates the model on a sample problem whose company plan earns a
net interest income of -99.83, using 180-day notes from January, 90-day notes
from February and 30-day notes in May, with the company's policy (collections
10% / 10% / 80%, minimum cash 250). Solving the LP with those policy variables
and the expected term structure of interest gave -98.0186 (paper Figure 3).

This script reproduces that number, shows where the gap to -99.83 comes from,
and reruns the company's own plan inside the model.

    python 02_validation.py
"""

import numpy as np
from scipy.optimize import linprog

from model import INSTRUMENTS, TERM_RATES, Policy, Settings, affine, ending_cash, nii, receipts, solve


def company_plan(s, p):
    """Best NII using only the company's borrowing instruments (plus any lending)."""
    allowed = set(range(10)) | {14, 16, 19}         # lending; 30-day May, 90-day Feb, 180-day Jan notes
    c, c0 = affine(lambda x: np.atleast_1d(nii(x, p, s)))
    Ae, be = affine(lambda x: ending_cash(x, p, s))
    A = np.zeros((6, 20))
    for m, cols in enumerate([(0, 6), (1, 7), (2, 8), (3, 9), (4,), (5,)]):
        A[m, list(cols)] = 1
    r = linprog(-c.ravel(), A_ub=A, b_ub=receipts(p), A_eq=Ae, b_eq=p.mcb - be,
                bounds=[(0, None) if i in allowed else (0, 0) for i in range(20)], method="highs")
    return float(c.ravel() @ r.x + c0[0]), r.x


def show(x):
    for (kind, month, rate), v in zip(INSTRUMENTS, x):
        if v > 1e-6:
            print(f"    {kind:<13} {month}  @ {rate:.3f}   {v:9.2f}")


def main():
    p = Policy()
    as_run = Settings(rates=TERM_RATES.copy(), keep_d192_slip=True)
    corrected = Settings(rates=TERM_RATES.copy(), keep_d192_slip=False)

    z, x, _ = solve(p, as_run)
    print(f"LP optimum, term-structure rates, as in the workbook: NII = {z:.8f}")
    print("  paper, Figure 3:                                   NII = -98.01855705")
    show(x)

    zc, xc, _ = solve(p, corrected)
    print(f"\nSame LP with cell D192 corrected (X17 at its own 10% rate): NII = {zc:.4f}")

    zp, xp = company_plan(corrected, p)
    print(f"\nBest plan using only the company's instruments (180-day Jan, 90-day Feb, 30-day May notes,\n"
          f"plus any lending), corrected model:                         NII = {zp:.4f}")
    print("  textbook figure for the company's plan:                   NII = -99.83")
    show(xp)

    print(f"\nGap between LP optimum and company plan: {zc - zp:.3f}")
    print("\nWhat this shows: the paper's -98.0186 is reproduced exactly, but only with a cell slip in the\n"
          "workbook. Cell D192 charges the 90-day February note (X17) at 9.5%, the rate of the January note,\n"
          "instead of its own 10%. Corrected, the optimum is -99.77, and the company's own plan, run through\n"
          "the same model (its three borrowing instruments, amounts chosen by the LP), gives -99.83: exactly\n"
          "the textbook's figure. That is the stronger validation the paper was looking for: the model\n"
          "reproduces the company's number, and the LP improves on the company's plan only slightly (by\n"
          "0.06), so the company's borrowing plan was close to optimal.")


if __name__ == "__main__":
    main()
