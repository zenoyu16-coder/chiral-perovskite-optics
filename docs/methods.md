# Methods

## Crystal structures

Experimental CIFs are parsed with pymatgen, using the source-specific manifests under `data/`. The 298 K R/S/rac NEA₂PbBr₄ set is checked for composition and temperature agreement. Space groups are assigned with spglib (default `symprec=0.05 Å`; a separate result uses `0.01 Å`).

For each Pb site, the six halide neighbors within 3.7 Å are used to calculate the mean Pb–X bond length, normalized bond-length deviation, mean trans angle and cis-angle variance. The 12 cis angles are found after pairing the six vectors into the three nearest-to-opposite trans pairs. Sites without six neighbors are reported as incomplete or, in the matched NEA analysis, rejected.

The mean halide-centroid displacement projected onto the deposited crystal's positive b-axis is also recorded. Its sign changes when that axis is reversed and cannot assign absolute structural handedness. R/S comparisons use the original crystallographic assignments.

`mba_temperature.py` produces `results/temperature_summary.csv`; `nea_analysis.py matched-analyze` produces `results/nea_matched_298K.csv`. Corresponding symmetry-tolerance checks are stored as separate CSV files.

## Circular dichroism and polarized devices

S-NEA film CD is read from the Duke front/back and deposited combined traces; `optics.py` computes the arithmetic mean separately and reports the residual relative to the archive. No numerical correction is applied to the deposited spectrum.

The Hautzinger et al. OSF table is parsed with a tab-delimited reader retaining missing fields and independent wavelength axes. Pearson correlation and normalized L2 differences describe R/S CD and absorbance shape. These are descriptive within-dataset comparisons.

Spin-LED circular polarization comes from the deposited `polarization`/`polarization1` columns. `spin_led_uncertainty.py` counts settings where their raw signs differ and where both supplied error intervals exclude zero at one or two times the archived error. The source error-bar definition and device channel-to-enantiomer mapping remain unverified.

## Time-resolved polarization

The circular polarization of emitted light is calculated at the maximum of the sum of the two recorded emission channels:

\[
DCP_0 = \frac{I_\mathrm{LCP}(t_\mathrm{peak})-I_\mathrm{RCP}(t_\mathrm{peak})}
{I_\mathrm{LCP}(t_\mathrm{peak})+I_\mathrm{RCP}(t_\mathrm{peak})}.
\]

The publisher's Fig. 3c source arrays contain 1,399 matched delay samples for each R/S-MBA-derived superlattice. `polarized_pl.py` reproduces the peak value from the original channels and optionally subtracts the mean early pre-burst signal (−60 to −40 ps). Additional pre-burst windows assess sensitivity to this choice.

For a graphical time-dependent contrast, the denominator is restricted to positive channels with combined intensity at least 20% of its corrected peak. That mask is a plotting condition; no decay constants are fitted. The approximately 0.35 ps sample spacing is distinct from the reported approximately 10 ps streak-camera resolution.

The independent Fig. 3d measured DCP points near 300 µJ cm⁻² are used to check the Fig. 3c reproduction. The RMBA second-channel heading is duplicated as LCP; `polarized_pl.py` retains that source label and annotates the inferred opposing-helicity interpretation.

## Fluence response

`fluence_response.py` reads peak-intensity/fluence arrays for S-MBA (Fig. 2c), R-MBA (Extended Data Fig. 7b) and PEA (Extended Data Fig. 6b). The left-panel plot divides intensity by each sample's first measured value, solely to compare trends. Time-integrated-PL superfluorescence thresholds of 70±10, 95±10 and 140±10 µJ cm⁻² are reproduced from Wei et al.; no additional threshold fit is performed.

Fig. 3d lists circular polarization and propagated peak-intensity errors for the chiral samples. The first sampled point with `|DCP| > 2 × reported_error` is recorded for each sample. This arithmetic rule does not define a statistical confidence interval or an independent threshold.

The Cambridge nonchiral transient-absorption example is handled by `transient_absorption.py`, which validates its time axis, checks pre-pump signals and plots the six original source-labeled channels.

## Execution and software

Install with `python -m pip install -e ".[dev,viz]"`. `python scripts/reproduce.py --fetch` downloads and analyzes the source datasets; `python scripts/reproduce.py` uses local source files. Unit tests run with `python -m pytest -q`. Source and output hashes are checked by `python scripts/verify_results.py`.

The script suite depends on NumPy, pymatgen and matplotlib, and uses the Python standard library for tabular input, ZIP/XLSX parsing and file hashing. The read-only Excel parser preserves blank columns and treats mixed experimental/theory worksheet columns separately.
