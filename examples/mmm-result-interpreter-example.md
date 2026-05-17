# MMM Result Interpreter Example

## Prompt

```text
/mmm-result-interpreter MMM output says paid search contribution is 32% with ROI 4.2, paid social contribution is 18% with ROI 1.6, TV contribution is 12% with ROI 2.1 but wide uncertainty, affiliates contribution is 8% with ROI 3.0. Paid social marginal ROI is below 1 at current spend.
```

## Example Output

## MMM Result Interpretation

### Executive Readout

Paid search appears to be the largest and most efficient channel, but it may include demand capture and should be split into brand and non-brand if possible. Paid social contributes material volume but looks saturated at current spend because marginal ROI is below 1. TV shows potential contribution but uncertainty is wide, so budget decisions should be cautious and supported by additional validation.

### Diagnostics Check

| Diagnostic | Readout | Implication |
|---|---|---|
| uncertainty | TV wide uncertainty | avoid strong TV budget shift without validation |
| marginal ROI | paid social below 1 | current spend may be above efficient level |
| channel interpretation | paid search high ROI | check brand/non-brand mix and incrementality |

### Channel Interpretation

| Channel | Contribution | ROI/mROI | Uncertainty | Interpretation |
|---|---:|---:|---|---|
| paid search | 32% | ROI 4.2 | not supplied | strong but may include demand capture |
| paid social | 18% | mROI below 1 | not supplied | likely saturated at current spend |
| TV | 12% | ROI 2.1 | wide | promising but uncertain |
| affiliates | 8% | ROI 3.0 | not supplied | efficient, but check incrementality |

### Budget Implications

- Do not increase paid social until saturation is validated or targeting/creative changes.
- Split paid search into brand and non-brand before increasing budget.
- Keep TV stable or run a geo/flight validation before scaling.
- Review affiliate incrementality, especially voucher or last-click partners.

### Caveats and Uncertainty

- ROI is not the same as marginal ROI.
- Wide uncertainty means channel ranking may be unstable.
- Platform-attributed benchmarks should not be used as proof of incrementality.

### Follow-Up Tests or Data Improvements

- Run brand/non-brand paid search decomposition.
- Design a paid social geo or audience incrementality test.
- Validate TV with geo or flight variation where feasible.
