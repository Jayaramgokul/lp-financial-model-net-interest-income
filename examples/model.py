"""The 2013 spreadsheet model, transcribed formula by formula into Python.

Each function mirrors a block of `Sheet1` in model/LP_financial_model_2013.xlsx
(the cell references are given in comments), so the Python and the workbook can
be checked against each other. The model is affine in the 20 decision
variables X1..X20, which is what lets Excel's Simplex LP solver (and scipy's
HiGHS solver here) find the optimum.

Policy variables (inputs, not decision variables, in both the workbook and here):
    cf = (month of sale, 1 month after, 2 months after) collection fractions
    pf = (month of purchase, 1 month after) payment fractions
    mcb = minimum cash balance, which each month's ending cash must equal
"""

from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import linprog

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

# Sales forecast (Sheet1 B52:H52) and base period (B4:C4, Nov and Dec).
SALES = [1700, 1800, 2000, 2600, 2400, 1900, 1400]          # Jan .. Jul
SALES_NOV, SALES_DEC = 1400, 1500
GROSS_MARGIN = 0.25                                          # B42
G_AND_A = 250                                                # row 55
DEPRECIATION = [0, 0, 0, 0, 0, 100]                          # row 56
TAX_RATE = 0.40                                              # A383
TAX_PAYABLE_DEC = 200                                        # C15, paid in March
LTD_INTEREST = 8.75                                          # 1,000 at 10.5% / 12, hard-coded in the sheet
OPENING_CASH = 250                                           # B97, hard-coded

# The 20 instruments (rows 153-172), with the annual rates of the expected term
# structure (rows 26-31), as labelled in the 2013 Solver reports.
INSTRUMENTS = [
    ("30-day CD", "Jan", .08), ("30-day CD", "Feb", .09), ("30-day CD", "Mar", .10),
    ("30-day CD", "Apr", .095), ("30-day CD", "May", .09), ("30-day CD", "Jun", .09),
    ("90-day CD", "Jan", .095), ("90-day CD", "Feb", .09), ("90-day CD", "Mar", .095),
    ("90-day CD", "Apr", .09),
    ("30-day note", "Jan", .09), ("30-day note", "Feb", .10), ("30-day note", "Mar", .115),
    ("30-day note", "Apr", .11), ("30-day note", "May", .095),
    ("90-day note", "Jan", .095), ("90-day note", "Feb", .10), ("90-day note", "Mar", .11),
    ("90-day note", "Apr", .11),
    ("180-day note", "Jan", .10),
]
TERM_RATES = np.array([r for _, _, r in INSTRUMENTS])
FLAT_RATES = np.full(20, 0.10)            # the a1..a20 constants as saved in the workbook (B127:B150)


@dataclass
class Policy:
    cf: tuple = (0.10, 0.10, 0.80)
    pf: tuple = (0.0, 1.0)
    mcb: float = 250.0


@dataclass
class Settings:
    rates: np.ndarray = field(default_factory=lambda: FLAT_RATES.copy())
    # D192 computes the interest on X17 with a16 (cell B145) instead of a17 (B146).
    # It makes no difference with flat rates; with the term structure it does.
    keep_d192_slip: bool = True
    # Rows 75-76 pay pf0 x COGS(t) + pf1 x COGS(t), so the split cannot matter.
    # With this switch, the month-of-purchase share pays THIS month's purchases
    # (= next month's COGS) and the rest pays LAST month's purchases (= this
    # month's COGS). Not the workbook's formulation; used in example 04.
    purchase_timing_fix: bool = False


def monthly_interest(x, s):
    """Rows 176-195: rate x amount / 12 for each instrument (index 0 = X1)."""
    a = s.rates.copy()
    if s.keep_d192_slip:
        a[16] = s.rates[15]
    return a * x / 12


def interest_received(d):
    """Row 93 (Jan .. Jun), from D176..D185 = d[0..9]."""
    return np.array([0, d[0] + d[6], d[1] + d[6] + d[7], d[2] + d[6] + d[7] + d[8],
                     d[3] + d[7] + d[8] + d[9], d[4] + d[8] + d[9]])


def interest_paid(d):
    """Row 94, from D186..D195 = d[10..19], plus long-term debt interest."""
    L = LTD_INTEREST
    return np.array([L,
                     L + d[10] + d[15] + d[19],
                     L + d[11] + d[15] + d[16] + d[19],
                     L + d[12] + d[15] + d[16] + d[17] + d[19],
                     L + d[13] + d[16] + d[17] + d[18] + d[19],
                     L + d[14] + d[17] + d[18] + d[19]])


def receipts(p):
    """Row 70. Nov and Dec sales are collected under the base 60% / 30% pattern, hard-coded."""
    S = SALES
    c0, c1, c2 = p.cf
    return np.array([S[0] * c0 + 0.6 * SALES_DEC + 0.3 * SALES_NOV,
                     S[1] * c0 + S[0] * c1 + 0.3 * SALES_DEC,
                     S[2] * c0 + S[1] * c1 + S[0] * c2,
                     S[3] * c0 + S[2] * c1 + S[1] * c2,
                     S[4] * c0 + S[3] * c1 + S[2] * c2,
                     S[5] * c0 + S[4] * c1 + S[3] * c2])


def cash_flows(x, p, s):
    """Everything that depends on the decision variables x (length 20)."""
    d = monthly_interest(x, s)
    ii, ie = interest_received(d), interest_paid(d)
    cogs = np.array(SALES[:6]) * (1 - GROSS_MARGIN)
    op_profit = np.array(SALES[:6]) - cogs - G_AND_A - np.array(DEPRECIATION)
    tax = TAX_RATE * (op_profit + ii - ie)                       # rows 60-61
    # Rows 75-76: both payment rows multiply the SAME month's cost of goods,
    # so (pf0 + pf1) x COGS = COGS whatever the split.
    paid = p.pf[0] * cogs + p.pf[1] * cogs
    if s.purchase_timing_fix:
        cogs_next = np.array(SALES[1:7]) * (1 - GROSS_MARGIN)      # purchases this month (row 71)
        paid = p.pf[0] * cogs_next + p.pf[1] * cogs
    taxes_paid = np.array([0, 0, TAX_PAYABLE_DEC + tax[:3].sum(), 0, 0, tax[3:].sum()])
    net_operating = receipts(p) - (paid + G_AND_A + taxes_paid)  # row 80
    return d, ii, ie, net_operating


def ending_cash(x, p, s):
    """Rows 210-215: ending cash each month, with beginning cash = previous ending (= MCB)."""
    d, _, _, net = cash_flows(x, p, s)
    X = np.concatenate([[0], x])          # 1-based, so X[1] is X1
    D = np.concatenate([[0] * 176, d])    # D[176] .. D[195], as in the sheet
    begin = [OPENING_CASH] + [p.mcb] * 5
    L = LTD_INTEREST
    return np.array([
        begin[0] + net[0] - X[1] - X[7] + X[11] + X[16] + X[20] - L,
        begin[1] + net[1] + D[176] + D[182] - D[186] - D[191] - D[195]
        + X[1] - X[2] - X[8] - X[11] + X[12] + X[17] - L,
        begin[2] + net[2] + D[177] + D[182] + D[183] - D[187] - D[191] - D[195] - D[192] - D[193]
        + X[2] - X[3] - X[9] - X[12] + X[13] + X[18] - L,
        begin[3] + net[3] + D[182] + D[178] + D[183] + D[184] - D[188] - D[192] - D[193] - D[195]
        - X[4] + X[7] - X[13] + X[14] - X[16] + X[3] - X[10] + X[19] - L,
        begin[4] + net[4] + D[179] + D[183] + D[184] + D[185] - D[189] - D[192] - D[193] - D[194] - D[195]
        + X[4] - X[5] + X[8] - X[14] + X[15] - X[17] - L,
        begin[5] + net[5] + D[180] + D[184] + D[185] - D[190] - D[193] - D[194] - D[195]
        + X[5] - X[6] + X[9] - X[15] - X[18] - L,
    ])


def nii(x, p, s):
    """B177: net interest income over the six months = sum(row 93) - sum(row 94)."""
    _, ii, ie, _ = cash_flows(x, p, s)
    return ii.sum() - ie.sum()


def affine(f, n=20):
    """Coefficients (A, b) with f(x) = A @ x + b, exact because f is affine."""
    b = np.asarray(f(np.zeros(n)), dtype=float)
    A = np.column_stack([np.asarray(f(np.eye(n)[i]), dtype=float) - b for i in range(n)])
    return A, b


def solve(p=None, s=None, mcb_is_minimum=False):
    """Maximise NII subject to the workbook's constraints. Returns (nii, x, result)."""
    p, s = p or Policy(), s or Settings()
    c, c0 = affine(lambda x: np.atleast_1d(nii(x, p, s)))
    Aend, bend = affine(lambda x: ending_cash(x, p, s))
    # Lending in a month cannot exceed that month's receipts (rows 203-208).
    R = receipts(p)
    Aub = np.zeros((6, 20))
    for m, cols in enumerate([(0, 6), (1, 7), (2, 8), (3, 9), (4,), (5,)]):
        Aub[m, list(cols)] = 1
    bub = R
    if mcb_is_minimum:   # ending cash >= MCB instead of = MCB (not the workbook's formulation)
        Aub, bub = np.vstack([Aub, -Aend]), np.concatenate([bub, bend - p.mcb])
        Aeq = beq = None
    else:
        Aeq, beq = Aend, p.mcb - bend
    res = linprog(-c.ravel(), A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq,
                  bounds=[(0, None)] * 20, method="highs")
    if not res.success:
        return None, None, res
    return float(c.ravel() @ res.x + c0[0]), res.x, res
