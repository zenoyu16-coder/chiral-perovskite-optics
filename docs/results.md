# Results and data notes

These calculations use source files associated with Jana et al. (2020), Hautzinger et al. (2024), Sercel et al. (2025) and Wei et al. (2026). The figures in this repository were regenerated from the deposited data.

## Chiral superlattice emission

Wei et al. measured R/S-MBA-derived superlattices at 550 nm excitation and 300 µJ cm⁻² pump fluence. The Fig. 3c workbook has two intensity columns for each handedness, with 1,399 common delay points. The peak polarization was calculated at the maximum of the two channels' summed intensity.

| Quantity | S-MBA | R-MBA |
| --- | ---: | ---: |
| Peak delay in source file (ps) | 53.24 | 46.25 |
| Circular polarization at peak | +13.49% | −13.76% |
| After pre-burst background subtraction | +13.52% | −13.81% |
| Experimental point in published Fig. 3d | +13.53% | −13.66% |

The background calculation used −60 to −40 ps as its default interval. Varying the early window produced only small changes in peak polarization; the actual window-dependent values are in [the numerical output](../results/nature2026_sf_fig3c_audit.json). The 7 ps difference in the tabulated peak delays is not resolved as a sample-independent dynamical difference by a camera with approximately 10 ps temporal resolution.

The second RMBA column is labeled LCP in the original Excel file, just like the first. Keeping its numbers and interpreting it as the opposite-helicity channel recovers the negative polarization given in Fig. 3d. The file remains unchanged.

[Polarized-emission figure](../results/nature2026_sf_fig3c_reproduction.png)

## Excitation-density dependence

The deposited source tables provide 10 S-MBA, 10 R-MBA and 12 PEA measurements of peak PL against pump fluence. Wei et al. report time-integrated-PL superfluorescence thresholds of 70 ± 10, 95 ± 10 and 140 ± 10 µJ cm⁻², respectively.

All three samples exhibit superfluorescence, including the PEA sample without a chiral spacer. The authors also report no circularly polarized superfluorescence for PEA. The accessible Fig. 3d source workbook, however, contains fluence-dependent DCP points only for S-MBA and R-MBA.

For those deposited DCP points, the first measurement satisfying `|DCP| > 2 × reported error` occurs at 95.4 µJ cm⁻² for S-MBA and 134.66 µJ cm⁻² for R-MBA. This is a check on the supplied error bars, separate from the superfluorescence threshold fit in the paper.

The Extended Data Fig. 7a RMBA time series contains a nominal 85 µJ cm⁻² trace; the corresponding Fig. 7b source table lists 82 µJ cm⁻². The analyses leave these entries unpaired.

[Fluence comparison](../results/nature2026_fluence_control.png) · [Source values](../results/nature2026_fluence_control_audit.json)

## Spin-LED spectra

Hautzinger et al. deposited 401 aligned R/S circular-dichroism points and 501 absorption points. The R/S Pearson correlations are −0.8752 for CD and +0.9992 for absorption. The raw CD curves are not exactly antisymmetric; the norm ratio `||CD_R + CD_S|| / ||CD_R − CD_S||` is 0.5360.

The two device-polarization columns have opposing signs at all six current settings. Requiring both values' intervals to exclude zero leaves five current settings under ±one deposited error and four under ±two errors. The meaning of those error bars is not defined in the source table, and the columns are labeled `polarization` and `polarization1`, without an explicit R/S mapping. These measurements belong to spin-LED devices whose emitting layer is an AlGaInP quantum well.

[Optical spectra](../results/osf_chiral_cd_abs_pair.png) · [Device measurements](../results/osf_chiral_device_docp.png)

## Structure measurements

The 298 K R/S-NEA₂PbBr₄ structures are both `P2₁); the racemic structure is `P2₁/c`. Mean Pb–Br lengths from the deposited CIFs are 3.0344, 3.0366 and 3.0267 Å for S, R and racemic, with cis-angle variances of 40.17, 40.47 and 19.75 deg². The b-axis projection of the local halide-centroid displacement reverses sign between the deposited R and S settings, but the sign depends on the chosen crystallographic axis.

A separate S-MBA₂PbI₄ series covers 100, 200 and 298 K. The measured front/back CD spectra of a different S-NEA₂PbBr₄ film show another source-format discrepancy: the archived trace labeled as an average agrees numerically with the *sum* of front and back spectra to rounding. The original trace and the arithmetic mean are stored separately.

[Crystal comparison](../results/nea_matched_298K.csv) · [Temperature series](../results/temperature_summary.csv) · [Front/back CD comparison](../results/cd_front_back_comparison.csv)

## What these datasets can be used for

The studies involve different specimens and in some cases different device architectures. The scripts reproduce optical contrasts, deposited fluence trends and local crystal geometry. The available figure-source workbooks do not include independent fabrication replicates or original camera frames. Further investigation of polarization retention therefore depends on additional measurements rather than a combined numerical fit to these datasets.
