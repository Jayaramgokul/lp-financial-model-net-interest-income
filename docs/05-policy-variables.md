# 5. How the policy variables affect NII

*Paper section 5 and Figures 5–9. 2013 report chapter 3. Example: [`03_policy_variables.py`](../examples/03_policy_variables.py).*

For each setting of a policy variable, the LP is solved again. All figures
below are the paper's setting: term-structure rates, workbook as run.

## Collection fractions (Figures 5–7)

The paper varied two collection fractions in 5% steps, keeping the third at
0. In the workbook, the "2 months after" fraction is always the remainder.

| Collection policy (month of sale / 1 after / 2 after) | Optimal NII |
|---|---|
| 0% / 0% / 100% | −121.17 |
| 10% / 10% / 80% (the company's new terms) | −98.02 |
| 10% / 60% / 30% (the company's old terms) | −62.84 |
| **100% / 0% / 0%** | **+30.615** |

- **Faster collection always raises NII.** In every sweep, the more that is
  collected early, the higher the NII.
- **The corner wins.** Over the full grid, the best policy is to collect
  everything in the month of sale: **30.615**, the paper's figure.

**The textbook's question, answered.** The textbook asks what the change in
credit terms, from 10/60/30 to 10/10/80, costs the company:

- **As run:** about **35** of NII over six months (−62.84 against −98.02).
- **With D192 corrected:** about 35.8 (−64.01 against −99.77).

## Payment fractions (Figure 8)

NII is identical, to six decimal places, for every split between paying
suppliers in the month of purchase and the month after. The paper read this
as purchase timing being a non-binding constraint.
[7](07-looking-back.md) shows it is a property of two cells in the model.

## Minimum cash balance (Figure 9)

NII falls in a straight line as the minimum cash balance rises:
- **Slope:** −0.042 per unit of cash. Each unit held from February to June is
  funded by borrowing at about 10% for about five months, and
  10% × 5 ÷ 12 ≈ 0.042.
- **Range:** −87.46 at zero minimum cash, −98.02 at 250.

## The paper's conclusion

The paper concludes that the company should:
- **hold no minimum cash;**
- **collect 100% in the month of sale.**

That would raise NII from −98.0 to +30.6, and higher still with zero
minimum cash.

Within the model, both statements are true. [7](07-looking-back.md)
discusses what the model leaves out that would change them.
