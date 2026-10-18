# 7. Looking back

*Written later, after rebuilding the model in Python and rerunning every experiment. The paper, the workbook and their results are unchanged; this is how I read them now. Example: [`04_looking_back.py`](../examples/04_looking_back.py).*

Every number in the paper reproduces: −98.0186 for the validation and 30.615
for the best collection policy. Rebuilding the model also showed which
results come from the business problem, and which from the way the model was
built.

## 1. The validation rests on one cell

The paper's −98.0186 reproduces only with a slip in cell D192: the 90-day
February note is charged the January note's rate.

Corrected, the model reproduces the company's own −99.83. Its optimum,
−99.77, is only 0.06 better. That is a cleaner validation than the paper
gave, and it changes the reading:
- **The company's plan was nearly optimal.** The LP adds very little.
- **The gap was the slip.** The 1.8 improvement the paper reported was almost
  entirely the cell error. See [4](04-validation.md).

## 2. "Purchase fractions do not affect NII" is built in

Both payment rows in the workbook multiply the **same** month's cost of goods:

```
paid(t) = pf0 × COGS(t) + pf1 × COGS(t) = COGS(t)
```

So the split can never change cash flow. Paid in the right months, with this
month's purchases and last month's, paying suppliers sooner costs NII, as it
should:

| Share paid in the month of purchase | NII |
|---|---|
| 0% | −98.0 |
| 50% | −104.4 |
| 100% | −111.0 |

The paper's "non-binding constraint" finding is a property of the
formulas, not of the business.

## 3. "Collect everything at once" is a corner solution

**Why the corner.** NII rises steadily with faster collection, and the
model charges nothing for collecting faster. So the optimum is always the
extreme: 100% in the month of sale.

**What it is worth.** The gain over the company's terms is 128.6 over six
months, about **1% of sales**. Getting customers to pay at once usually costs
something: a cash discount, or customers lost to competitors offering credit.
Any such cost above about 1% of sales would make the "optimal" policy worse
than the company's.

**The same for cash.** The recommendation to hold zero minimum cash is the
same kind of result. The model has no cost of running out of cash, so less
cash is always better.

**The fix.** A fuller model would add these costs as constraints or
penalties, and the policy question would become a genuine trade-off.

## 4. The policy variables can be optimised directly

The abstract describes the collection and purchase fractions as decision
variables, but Solver only ever changed the 20 borrowing and lending
amounts. The fractions enter the model linearly, so they *can* be LP
variables. One solve with 22 variables lands on the same corner (100 / 0 / 0,
NII 30.615) that the paper reached with a grid of Solver runs.

## 5. There is one optimal plan, not several

The paper read the difference between its plan and the company's as
evidence of multiple optimal solutions. Checking the range of every
instrument across all plans with the optimal NII shows **zero** range. The
optimum is unique. The plans differ because the company's plan is not quite
optimal.

## 6. Smaller points

- **The balance sheet doesn't balance.** It balances only in January. The
  February gap of 680.89 is exactly the January 90-day CD, which drops out of
  assets although it matures in April. The LP does not use the balance sheet,
  so the results are unaffected, but it could not have served as a check.
- **Inconsistencies in the manuscript:**
  - the text gives the tax rate as 4% where the workbook uses 40%;
  - the list of variables skips X19;
  - the sentence describing the minimum-cash figure says "purchase fraction";
  - "Terry and Zeitlow" most likely means Maness & Zietlow.
- **The saved workbook uses a placeholder rate.** Its interest constants are a
  flat 10%, not the term structure the paper used. Anyone opening it should
  know that the saved state reproduces −97.74, not the paper's figures.

## What I would add now

- **Costs for the levers:** for faster collection, through discounts or lost
  sales, and for low cash, through a shortfall penalty or a chance constraint.
- **Uncertain sales:** robust or stochastic LP, since a plan that is optimal
  for one sales forecast can be infeasible for another.
- **The paper's own question as a single model:** the policy variables
  optimised alongside the financing decisions, with the costs above, rather
  than swept one at a time.
