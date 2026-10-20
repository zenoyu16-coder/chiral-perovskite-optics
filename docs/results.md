# Results

Numerical values below are derived from original published data, with experimental references retained separately from our calculations. Figure-source data may contain plotting resampling or other processing performed by the original authors.

## Polarized superfluorescence

Wei et al., [*Nature* (2026)](https://doi.org/10.1038/s41586-026-10637-x), measured R/S-MBA-derived quasi-2D superlattices with 550 nm linearly polarized excitation at 300 µJ cm⁻² (Fig. 3c).

| Quantity | S-MBA | R-MBA |
| --- | ---: | ---: |
| Peak emission time in deposited traces (ps) | 53.24 | 46.25 |
| Peak DCP from original channels | +13.4949% | −13.7612% |
| Peak DCP after early background subtraction | +13.5188% | −13.8066% |
| Fig. 3d point near 300 µJ cm⁻² | +13.5290% | −13.6620% |

The baseline-corrected DCP changes by less than approximately 0.02 percentage points across the tested pre-burst windows for each handedness. The peak timing difference is smaller than the approximately 10 ps camera temporal resolution and was measured on different samples. It is not assigned to chirality-dependent relaxation.

The original RMBA Fig. 3c headers repeat LCP for the second channel. Reconstructed polarization has the same sign and magnitude as the paper's Fig. 3d measurement when that channel is treated as the opposing helicity; the source file is not edited.

[Time-resolved figure](../results/nature2026_sf_fig3c_reproduction.png) · [Numerical summary](../results/nature2026_sf_fig3c_audit.json)

## Fluence and achiral control

The same publication reports superfluorescence in S-MBA, R-MBA and achiral PEA superlattices. The authors' time-integrated-PL threshold values are 70±10, 95±10 and 140±10 µJ cm⁻², respectively.

The deposited peak-intensity series contain 10 S, 10 R and 12 PEA fluence points. Fluence-dependent polarization is available for the chiral samples; the original paper reports the absence of circularly polarized superfluorescence in the PEA control.

For a comparison with the supplied DCP error bars, the first sampled points satisfying `|DCP| > 2 × reported_error` occur at 95.4 µJ cm⁻² (S) and 134.66 µJ cm⁻² (R). This is a numerical comparison of measured plotting points, separate from the authors' physical SF threshold estimates.

[Fluence comparison](../results/nature2026_fluence_control.png) · [Source workbook audit](../results/nature2026_fluence_control_audit.json)

## R/S optical spectra and spin-LED measurements

The [Hautzinger et al. (2024)](https://doi.org/10.1038/s41586-024-07560-4) deposit contains 401 wavelength-aligned R/S CD measurements and 501 absorption points. The corresponding R/S correlations are −0.8752 for CD and +0.9992 for absorption. CD differs from perfect antisymmetry; its normalized sum/difference L2 ratio is 0.5360.

Two spin-LED polarization columns have opposite signs at all six recorded current values. Both values remain separated from zero at five points under ±one reported error and four under ±two errors. The current settings do not represent independent fabricated devices; the source table also lacks an unambiguous R/S mapping for those two columns.

[Optical figure](../results/osf_chiral_cd_abs_pair.png) · [Spin-LED figure](../results/osf_chiral_device_docp.png) · [Error-bar analysis](../results/spin_led_uncertainty_gate.json)

## Crystal symmetry and other source audits

At 298 K, the experimental R/S-NEA₂PbBr₄ crystal structures are assigned to `P2₁` and the racemic structure to `P2₁/c`. The corresponding mean Pb–Br lengths are approximately 3.0344, 3.0366 and 3.0267 Å; their cis-angle variances are 40.17, 40.47 and 19.75 deg². The signed b-axis displacement in the original cell setting is a coordinate-dependent projection.

The S-MBA₂PbI₄ temperature series provides a separate structural baseline at 100, 200 and 298 K. The S-NEA₂PbBr₄ film CD archive and the nonchiral Cambridge transient absorption traces are independent spectroscopy checks and have no sample-level connection to the crystal comparison.

[NEA crystal comparison](../results/nea_matched_298K.csv) · [MBA temperature series](../results/temperature_summary.csv) · [CD source check](../results/cd_front_back_audit.json) · [Nonchiral transient absorption](../results/dynamics_cambridge_qa.json)

## Scope of the evidence

The results reproduce measurements and conclusions already published by the cited authors. In particular, collective optical emission in the achiral PEA control and helicity-dependent emission in the chiral superlattices are established properties of the source study.

The available source files contain processed figure arrays but no original streak-camera frames or independent fabrication replicates. Cross-paper samples differ in structure, growth and detection; quantitative microscopic mechanisms and spin lifetimes are outside the present analyses.
