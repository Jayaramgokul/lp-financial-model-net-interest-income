# 2. The spreadsheet model

*Paper section 3 and Tables 1–3. 2013 report sections 1.2–1.3. Workbook: [`model/LP_financial_model_2013.xlsx`](../model/LP_financial_model_2013.xlsx), sheet `Sheet1`. Python: [`examples/model.py`](../examples/model.py).*

## Inputs (the sample problem)

**Sales forecast, January – July (in Rs):**

| Jan | Feb | Mar | Apr | May | Jun | Jul |
|---|---|---|---|---|---|---|
| 1,700 | 1,800 | 2,000 | 2,600 | 2,400 | 1,900 | 1,400 |

November and December sales were 1,400 and 1,500.

**Other inputs:**
- **Starting balance sheet:** cash 250, receivables 1,770, inventory 1,275,
  payables 1,275, long-term debt 1,000 at 10.5%.
- **Costs:** gross margin 25%; general and administrative expense 250 a month;
  depreciation 100 in June.
- **Tax:** 40%, paid in March and June.
- **Interest rates:** an expected term structure by month for the 20
  instruments. CDs pay 8–10%; 30-, 90- and 180-day notes cost 9–11.5%.

## The policy variables

| Policy | Company's values |
|---|---|
| Collection fractions (month of sale / 1 month after / 2 months after) | 10% / 10% / 80% |
| Payment fractions (month of purchase / 1 month after) | 0% / 100% |
| Inventory | Ending inventory = next month's cost of goods sold |
| Minimum cash balance | 250 |

## The statements, month by month

1. **Projected income statement:**
   - sales;
   - cost of goods sold;
   - gross profit;
   - G&A and depreciation;
   - operating profit;
   - interest received and paid;
   - profit before tax;
   - tax;
   - net income.

   Interest depends on the borrowing and lending decisions, so tax does too.
2. **Projected cash budget:**
   - **receipts:** each month's sales collected according to the collection
     fractions;
   - **disbursements:** suppliers, G&A, tax;
   - **operating net cash flow:** receipts minus disbursements.
3. **Financial flows:** interest received and paid, maturing CDs and notes,
   and beginning and ending cash.
4. **Projected balance sheet.**

The Python transcription mirrors these blocks function by function, with the
workbook's cell references in comments. Example
[01](../examples/01_check_against_workbook.py) checks it against every value
Excel saved: interest, cash flows, ending cash and NII. The largest
difference is 1 × 10⁻⁹.

## Details of the workbook worth knowing

- **Interest is monthly accrual.** A 90-day note's interest is charged at
  rate ÷ 12 in each month it is outstanding.
- **Ending cash must equal the minimum cash balance.** It is an equality in
  Solver, not "at least", so all surplus cash is lent and every shortfall
  borrowed.
- **Rates as saved: a flat 10%.** In the saved workbook, the 20 interest
  constants a1–a20 are a placeholder: 10% for every instrument. The paper's
  results use the term structure. Its rates are in the workbook's rate table
  and in the 2013 Solver reports' labels. The Python model offers both.
- **Hard-coded values:** January's opening cash (250) and the long-term debt
  interest (8.75 a month) are typed in, not linked to the inputs.
- **Old sales, old terms:** November and December sales are collected on the
  old 60% / 30% terms whatever collection policy is being tested.
