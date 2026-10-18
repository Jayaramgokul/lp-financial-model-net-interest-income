# 6. Applying the model to a real company (2013)

*2013 report chapter 4. Not in the 2017 paper's results. No data included.*

## What was done

The 2013 project applied the model to a real company: **Aarti Industries
Ltd**, a chemicals company. Its data came from **Prowess**, the Centre for
Monitoring Indian Economy's database of Indian company financials:
- sales;
- cost of goods sold;
- operating profit;
- assets and inventories;
- debtor, creditor and inventory days.

The model was adapted from months to years:
- **Instruments:** 1-, 2- and 3-year notes and deposits, all at 4%.
- **Assumptions:** ending inventory and purchases equal to next period's cost
  of goods sold, and taxes at 40%.
- **History:** the two missing earlier years were forecast.

Solver was run twice: once to maximise NII and once to minimise the cash
conversion cycle (CCC).

## Results reported

| Objective | Optimum |
|---|---|
| Net interest income | −47.45 |
| Cash conversion cycle | 2,160.3 |

The report concluded that both values could be improved by relaxing the
policy variables, the same levers studied in [5](05-policy-variables.md).

## Why the data is not here

Prowess is a licensed commercial database, so its figures cannot be
republished. The workbook in [`model/`](../model/) has had the Prowess sheets
removed. The textbook problem in [2](02-the-spreadsheet-model.md)–[5](05-policy-variables.md)
is fully reproducible.

## Read today

A CCC of 2,160 would be implausible in days for a manufacturer. With the
model adapted to annual periods, its units are unclear, and I would not
interpret it without rerunning the case.
