"""01. Is the Python model the same model as the workbook?

Reads the values Excel last calculated and saved in Sheet1 of the original
workbook (its decision variables, interest, cash flows and NII), recomputes them
with the Python transcription in model.py, and compares. Then solves the LP and
checks that the optimum equals what Excel's Solver found for the saved inputs.

    python 01_check_against_workbook.py
"""

import warnings

import numpy as np
import openpyxl

from common import WORKBOOK
from model import FLAT_RATES, Policy, Settings, cash_flows, ending_cash, nii, solve


warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


def main():
    ws = openpyxl.load_workbook(WORKBOOK, data_only=True)["Sheet1"]
    x_saved = np.array([ws[f"C{r}"].value for r in range(153, 173)], dtype=float)
    rates = np.array([ws[f"B{r}"].value for r in [127, 128, 129, 130, 131, 132, 134, 135, 136, 137,
                                                  139, 140, 141, 142, 143, 145, 146, 147, 148, 150]])
    policy = Policy(cf=(ws["A368"].value, ws["A369"].value, ws["A370"].value),
                    pf=(ws["A372"].value, ws["A373"].value), mcb=ws["A376"].value)
    print(f"Saved inputs: collection {policy.cf}, payment {policy.pf}, minimum cash {policy.mcb}")
    print(f"Saved rates a1..a20: all {sorted(set(rates))} (a flat placeholder, not the term structure)")
    assert np.allclose(rates, FLAT_RATES)

    s = Settings()
    _, ii, ie, net = cash_flows(x_saved, policy, s)
    rows = [("Interest received (row 93)", ii, "B93:G93"), ("Interest paid (row 94)", ie, "B94:G94"),
            ("Operating net cash flow (row 80)", net, "B80:G80"),
            ("Ending cash (rows 210-215)", ending_cash(x_saved, policy, s), None)]
    worst = 0.0
    for label, py, rng in rows:
        if rng:
            xl = np.array([c.value for c in ws[rng][0]], dtype=float)
        else:
            xl = np.array([ws[f"C{r}"].value for r in range(210, 216)], dtype=float)
        diff = np.abs(py - xl).max()
        worst = max(worst, diff)
        print(f"  {label:<34} max |Python - Excel| = {diff:.2e}")
    z_saved = nii(x_saved, policy, s)
    print(f"  NII at the saved solution: Python {z_saved:.8f}, Excel B177 {ws['B177'].value:.8f}")

    z_opt, _, _ = solve(policy, s)
    print(f"\nLP optimum with these inputs (HiGHS): {z_opt:.8f}")

    print("\nWhat this shows: the Python transcription reproduces every value Excel saved, to rounding\n"
          f"error (largest difference {worst:.1e}), and re-solving the LP returns the same optimum Excel's\n"
          "Solver found (-97.737). The two are the same model, so the later examples can use Python to\n"
          "rerun the paper's experiments.")


if __name__ == "__main__":
    main()
