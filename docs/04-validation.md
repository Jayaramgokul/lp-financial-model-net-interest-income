# 4. Validating the model on the textbook problem

*Paper section 4 and Figures 3–4. 2013 report section 2.5. Example: [`02_validation.py`](../examples/02_validation.py).*

## What the paper did

The sample problem gives the company's plan and its outcome:
- **the plan:** a 180-day note from January, a 90-day note from February and a
  30-day note in May;
- **policies:** collections of 10% / 10% / 80% and a minimum cash balance of 250;
- **outcome:** NII of **−99.83**.

The paper ran Solver with the same policies and obtained **−98.0186**. It
judged this close enough to validate the model. The different borrowing and
lending amounts were read as a sign of multiple optimal solutions.

## Reproduced

| | NII |
|---|---|
| Paper, Figure 3 | −98.01855705 |
| Python, term-structure rates, workbook as run | **−98.01855705** |

The match is exact to eight decimal places.

## Where the gap to −99.83 comes from

The exact match depends on one cell. **Cell D192** computes the interest on
X17, the 90-day note from February, using the rate of the January note (9.5%)
instead of its own 10%. With flat rates, as the workbook is saved, this makes
no difference. With the term structure it does:

| | NII |
|---|---|
| LP optimum, D192 as in the workbook | −98.019 |
| LP optimum, D192 corrected | **−99.767** |
| Best plan using only the company's three borrowing instruments, corrected | **−99.826** |
| Textbook figure for the company's plan | −99.83 |

Corrected, the model reproduces the company's own figure: −99.826, which
rounds to −99.83. That is a stronger validation than the paper claimed. The
model's optimum improves on the company's plan by only **0.06**, so the
company's borrowing plan was already close to optimal.

The workbook's settings also explain the gap. Almost all of the 1.8
difference between −98.0 and −99.8 came from the D192 slip, not from better
borrowing.

The different decision variables do **not** come from multiple optima.
Example [04](../examples/04_looking_back.py) shows the optimal plan is
unique. They come from the company's plan not being exactly optimal.

## The 2013 report and the paper differ in wording

- **2013 report:** the result was "−98.0, exactly equal to the given solution".
- **2017 paper:** the company's figure is −99.83, and −98.0 "closely equates"
  to it.

The reproduction supports the paper's figure for the company plan.
