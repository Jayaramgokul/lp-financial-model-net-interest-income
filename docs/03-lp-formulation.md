# 3. The linear programme

*Paper section 3.1. Workbook rows 122–246. Python: `solve()` in [`examples/model.py`](../examples/model.py).*

## Decision variables

There are twenty: the amounts lent or borrowed, by instrument and starting
month.

| Variables | Instrument | Starting months |
|---|---|---|
| X1–X6 | 30-day CD (lending) | Jan – Jun |
| X7–X10 | 90-day CD (lending) | Jan – Apr |
| X11–X15 | 30-day note (borrowing) | Jan – May |
| X16–X19 | 90-day note (borrowing) | Jan – Apr |
| X20 | 180-day note (borrowing) | Jan |

The paper's list of variables skips X19. In the workbook, X19 is the April
90-day note.

## Objective

Maximise NII over the six months:

```
max Z = Σ interest received on X1..X10  −  Σ interest paid on X11..X20  −  interest on long-term debt
```

Each instrument earns or costs rate × amount ÷ 12 for each month it is
outstanding.

## Constraints

1. **Lending is limited by receipts:** each month,
   X(30-day CD) + X(90-day CD) ≤ that month's cash receipts.
2. **Cash balance:** each month,
   - beginning cash + operating net cash flow + interest received − interest
     paid + maturing CDs − new CDs + new notes − maturing notes
   - must equal the minimum cash balance.
3. **Non-negativity:** all amounts ≥ 0.
4. **Policy variables:** collection and payment fractions lie between 0% and
   100%.

## What Solver actually varied

Excel's Solver settings, saved in the workbook, list only **X1–X20** as
changing cells. The policy variables are inputs: constraint 4 merely
checks their range. The paper studies them by re-running Solver at each
setting, in 5% steps, and plotting the results; see [5](05-policy-variables.md).
The abstract's description of the collection and purchase fractions as
decision variables therefore describes the study's aim, not the LP. Doing
it literally is possible, because the fractions enter linearly. Example
[04](../examples/04_looking_back.py) solves that version in one LP, which
reaches the same answer.

## Solving it now

[`model.py`](../examples/model.py) builds the objective and constraints by
reading the coefficients off the transcribed model, which is exact because
the model is affine in X. It then solves with SciPy's HiGHS solver.
