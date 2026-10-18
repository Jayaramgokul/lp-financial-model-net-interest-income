# 1. The problem: working capital and net interest income

*Paper sections 1–2. 2013 report chapter 1.*

## The question

A company's short-term finances depend on timing:
- **cash coming in:** collections from customers;
- **cash going out:** payments to suppliers, overheads and taxes.

When the two are mismatched, the company borrows short term to cover the gap.
When it has surplus cash, it can lend it out (here, certificates of deposit, CDs).

**Net interest income (NII)** is the interest earned on lending minus the
interest paid on borrowing. Over a six-month plan, the question is: **which
borrowing and lending, month by month, maximises NII**, while keeping a
minimum cash balance every month?

A second question follows. The company also sets **policies**:
- how quickly customers pay (collection fractions);
- how quickly suppliers are paid (payment fractions);
- how much cash to keep in hand.

How do those policies change the best achievable NII?

## Why linear programming

Each month's cash position is a sum of terms: receipts, payments, maturing
loans and deposits, and interest at fixed rates. So for fixed policies, every
constraint and the NII itself are **linear** in the amounts borrowed and lent.
That makes the problem a linear programme (LP), which Excel's Solver, using
the Simplex method, solves exactly.

## How the work developed

| When | What | Where |
|---|---|---|
| 2012–13 | BTech final-year project, Production Engineering, NIT Calicut (team project). An Excel model of the income statement, cash budget and balance sheet. Solver optimised NII and, separately, the cash conversion cycle. Validated on a textbook problem, then applied to a company from the Prowess database. | [model/](../model/), described in [6](06-prowess-case-study.md) |
| 2017–18 | Rewritten as a research paper with Prof. T. Radha Ramanan, during my research internship at IIM Indore. Focused on NII, with a fuller treatment of how the policy variables affect it. | [paper/](../paper/) |
| Now | The model transcribed into Python, every number in the paper reproduced, and the results re-read. | [examples/](../examples/), [7](07-looking-back.md) |

The paper cites "Terry and Zeitlow (2000)" for the modelling approach and the
sample problem. This most likely refers to Terry S. Maness and John T.
Zietlow's *Short-Term Financial Management*, with Maness's first name used in
place of his surname. I have not been able to confirm the edition or the
source of the sample problem.
