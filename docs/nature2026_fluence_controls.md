# Fluence response: chiral R/S and achiral PEA controls

Date: 2026-10-20. Source: Wei et al., *Nature* 654, 369–374 (2026), DOI [10.1038/s41586-026-10637-x](https://doi.org/10.1038/s41586-026-10637-x). This is a reproducibility and control audit of **already published physics**, not a new threshold estimate or theory.

## Question

Does the presence of a steepened, superlinear superfluorescent PL response require molecular chirality? Is significant circularly polarized emission observed at the same experimental fluences?

The article already answers the first question: SF occurs in the nonchiral PEA superlattice, while circularly polarized SF is observed in the chiral R/S samples, not in PEA. Our computations only verify that the deposited numerical data are compatible with that account.

## Source files verified

| Material / observable | Publisher workbook | Sheet | Data points |
|---|---|---|---:|
| S-MBA peak PL vs fluence | Source Data Fig. 2 | Fig.2c left | 10 |
| R-MBA peak PL vs fluence | Extended Data Fig. 7 | Extended Data Fig. 7b | 10 |
| PEA peak PL vs fluence | Extended Data Fig. 6 | Extended Data Fig. 6b | 12 |
| S-MBA/R-MBA DCP vs fluence | Source Data Fig. 3 | Fig. 3d | 13 S / 11 R |

All four original XLSX files are fetched from the publisher and checked against their exact SHA-256. The public `media.springernature.com` route for Extended Data Fig. 7 temporarily returned **HTML (3,038 bytes)** masquerading as an XLSX; a successful official `static-content.springer.com` download is pinned in `fluence_sources.py`.

Raw workbooks are kept under git-ignored `data/raw/kinetics`. No source workbook is edited or redistributed.

## Independent checks and observations

The authors give **time-integrated PL** SF thresholds of 70±10 µJ/cm² (SMBA), 95±10 µJ/cm² (RMBA), and 140±10 µJ/cm² (PEA). We display those values as *published references*, not thresholds fitted to Fig. 2c/Extended Data intensity points.

All three sets show an increase in peak PL intensity over the measured fluence range, including **nonchiral PEA**. Within each sample, the figure divides the measured PL peaks by that sample's first measured value to show shape only; source detector intensities are arbitrary and cannot be compared in absolute magnitude across different samples.

For the deposited Fig. 3d DCP values, we compute the earliest sampled point where `abs(DCP) > 2 * deposited_error`: 95.4 µJ/cm² for SMBA and 134.66 µJ/cm² for RMBA. This is a user-defined **arithmetic sensitivity check**, not an independent measurement of circular-polarization onset, a 95% interval, a new threshold, or an independent replication. The article specifies that its error bars propagate uncertainty in identifying TRPL peak intensities.

The achiral PEA control **does not** have matching fluence-resolved DCP columns in the inspected Fig. 3d source workbook. The absence of circularly polarized SF in PEA is therefore taken from the article's published experimental conclusion (Supplementary Fig. 24), not recreated from the tables above.

### Source mismatch found

ED Fig. 7a (RMBA time-resolved PL traces) includes a pump labelled **85 µJ/cm²**; ED Fig. 7b's numerical fluence/intensity series has an **82 µJ/cm²** point instead. The two tables should not be joined by matching index, and no hidden correction is applied.

## Reproduce

```powershell
python -m pip install -e ".[dev,viz]"
python -m chiral_perovskites.fluence_gate --fetch
python -m chiral_perovskites.fluence_gate
python -m pytest -q
```

Outputs are `results/nature2026_fluence_control_audit.json` and `results/nature2026_fluence_control.png`.

## Scientific decision

This exercise is now **complete**. Chirality is not required for nonlinear collective PL; observed handedness-dependent DCP is a more specific response. That is an established finding of Wei et al. The current source data do not measure causality between these features across matched independently fabricated specimens, and comparing fitted thresholds across three specimens would risk attributing thickness, domain size, interface and collection differences to chirality.

A meaningful next *new* experiment would compare **R, S and achiral superlattices**, across independent batches, with the same pump fluences, calibrated detection, and paired time-resolved LCP/RCP traces including instrument-response characterization. Measure total emission and circular polarization from each specimen before attempting any mechanistic model or DFT.

No further DFT, MD, ML or additional descriptive fitting is warranted for these source files alone.
