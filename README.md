# A linear programming model for optimal net interest income

![examples](https://github.com/Jayaramgokul/lp-financial-model-net-interest-income/actions/workflows/examples.yml/badge.svg)
![python](https://img.shields.io/badge/python-3.10%2B-blue)

**Which borrowing and lending, month by month, maximises a company's net
interest income, and how do its collection, payment and cash policies change
the answer?**

- **2013:** the model began as my BTech final-year project in Production
  Engineering at NIT Calicut (a team project): an Excel model of a company's
  income statement, cash budget and balance sheet, optimised with Solver.
- **2017–18:** I developed it into a research paper with Prof. T. Radha Ramanan
  during a research internship at IIM Indore.
- **This repository:** the original workbook, the paper, a Python transcription
  that reproduces every result in the paper, and a fresh reading of what those
  results do and do not show.

📄 **[Read the paper](paper/LP_Financial_Model_Optimal_NII_Gokulan_RadhaRamanan_2017.pdf)**
(Gokulan & Radha Ramanan, manuscript, 2017) ·
[Original Excel model](model/LP_financial_model_2013.xlsx)

## The reasoning, step by step

| | Document | Example |
|---|---|---|
| 1 | [The problem: working capital and net interest income](docs/01-working-capital-and-nii.md) | |
| 2 | [The spreadsheet model: statements, cash budget, policy variables](docs/02-the-spreadsheet-model.md) | [py](examples/01_check_against_workbook.py) |
| 3 | [The linear programme: 20 instruments, cash and lending constraints](docs/03-lp-formulation.md) | [py](examples/model.py) |
| 4 | [Validating the model on the textbook problem](docs/04-validation.md) | [py](examples/02_validation.py) |
| 5 | [How collection, payment and cash policies affect NII](docs/05-policy-variables.md) | [py](examples/03_policy_variables.py) |
| 6 | [Applying the model to a real company (2013, Prowess data)](docs/06-prowess-case-study.md) | |
| 7 | [Looking back: what the results owe to how the model was built](docs/07-looking-back.md) | [py](examples/04_looking_back.py) |

## What it found

**The paper's results**
- **The textbook company's plan** earns a net interest income of −99.83 over
  six months. The LP's validation run gave −98.02.
- **Collection:** collecting everything in the month of sale raises NII to
  **+30.6**.
- **Cash:** a lower minimum cash balance raises NII further.
- **Payments:** the timing of payments to suppliers makes no difference.

**Rebuilt in Python.** Every number reproduces exactly: −98.01855705 and
30.615. Re-reading them:
- **The validation depends on one cell.** A cell charges one note the wrong
  rate. Corrected, the model reproduces the company's own −99.83, and its
  optimum (−99.77) is only 0.06 better. The company's plan was nearly optimal.
- **"Payment timing doesn't matter" is built into the formulas.** Both
  payment rows multiply the same month's costs.
- **"Collect everything at once" is a corner solution.** The model charges
  nothing for collecting faster. The gain is worth about 1% of sales, so a
  cash discount larger than that would reverse it.
- **The optimum is unique.** The policy variables, swept one by one in the
  paper, can be optimised inside the same LP.

## Running the examples

```bash
pip install -r requirements.txt
cd examples
python 01_check_against_workbook.py      # ... through 04_looking_back.py
```

Example 01 reads the workbook's saved values and checks the Python model
against them. Charts are written to `examples/output/`.

## What is in this repository

```
paper/      the 2017 manuscript (PDF)
model/      the original Excel workbook (2012–13), with the Prowess data sheets removed
docs/       one document per step of the work
examples/   the model transcribed into Python (model.py) and four examples
```

**Not included:**
- **The 2013 team report.** Its content is summarised in the docs.
- **The Prowess company data.** It comes from a licensed database.

A later 2018 copy of the manuscript differs only in language edits, a shorter
conclusion and renumbered figures; its results are identical.

## Licence

The code in `examples/` is MIT-licensed ([LICENSE](LICENSE)). The paper is ©
Jayaram Gokulan and T. Radha Ramanan; the workbook is © Jayaram Gokulan.
