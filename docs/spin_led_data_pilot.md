# Chiral optical response and spin-LED data audit — 20 October 2026

## The bounded question

In an experimental chiral-halide-perovskite device platform, how similar are R/S ordinary optical spectra, how close are the chiroptical responses to sign reversal, and do two recorded polarization-voltage/current series have consistent opposite signs?

This is **not** an extraction of spin-injection efficiency, spin lifetime, chirality transfer coefficient, or proof of a microscopic CISS mechanism. It serves as a real-data control for the broader project about exciton polarization dynamics.

## Experimental source

Hautzinger et al., *Nature* **631**, 307–312 (2024), [DOI 10.1038/s41586-024-07560-4](https://doi.org/10.1038/s41586-024-07560-4).

Data are published in [OSF 2M35K](https://doi.org/10.17605/OSF.IO/2M35K). A `fetch` command downloads exact listed files; SHA-256 and URLs are recorded in the audit JSON. The raw data are intentionally excluded from this Git repository.

Files examined:
- `Extended_data_fig_8_Absorbance_CD_CPL.txt`: separate R/S-MBA CD columns, R/S-MBA absorbance, and separate PL columns; the independent axes in the same row have different lengths. CD units are **not specified by the raw header**.
- `Fig_2c_current_vs_DOCP.txt`: source names channels `polarization` and `polarization1`; both have source-provided `error` values. The TSV alone does **not** unambiguously assign each series to R or S. No claim about which handedness produces which sign is made here.
- `Extended_data_fig_4b_polvscurrent_device1b.txt` and `Extended_data_fig_5b_polvscurrent_device3b.txt`: their numeric matrices are exactly identical, despite being labeled under separate figure references; **not independent replicate measurements** without verification from article caption.

### Parser pitfall discovered and fixed

The optical file is a *ragged* table: CD ends after 401 points, absorption after 501, PL after 696. A whitespace-splitting reader can collapse empty fields and silently shift the surviving columns; it incorrectly returned 696 CD rows in preliminary analysis. The final script uses a TAB-delimited reader, preserves empty fields, and aligns each independent pair by its own wavelength axis. Unit tests cover this exact scenario.

## Derived numerical observations

- CD: 401 R/S rows, 290–650 nm; Pearson r = -0.8752. This indicates substantial anti-correlation, not exact mirror spectra.
- CD: `||CD_R+CD_S||_2 / ||CD_R-CD_S||_2 = 0.5360`. The ratio is zero for a perfectly antisymmetric pair. It is a descriptive *shape-and-amplitude* metric, not a chiral mechanism parameter or a physically calibrated g-factor.
- Absorption: 501 R/S rows, 300–800 nm; Pearson r = +0.9992.
- Absorption: relative L2 discrepancy `||A_R-A_S||_2 / ||(A_R+A_S)/2||_2 = 0.08374`. The absorbance lines are nearly co-shaped but not identical.
- Polarized device emission: both source channels have opposite measured signs at 6/6 listed current values (1, 2, 3, 5, 10 and 15). When both values must stay away from zero after adding/subtracting 1 × the deposited error, this becomes 5/6; at 2 × the deposited error, 4/6. The errors' statistical definition is unverified, so these are not confidence levels. See `results/spin_led_uncertainty_gate.json` and [scientific decision checkpoint](science_gate_2026-10-20.md). The TSV does not independently identify R/S channel assignment, and the older arXiv manuscript has an apparent handedness/sign-convention inconsistency near Fig. 2. Do not guess the mapping or count different current points as independent device repeats.

The CD and device observations appear in the *same published study*, but the files do not prove they are measurements on the **same individual specimen**. We therefore do not correlate point-by-point CD with device DOCP or claim a causal optical-to-electrical transfer factor.

## What the data do NOT establish

A near-equal ordinary absorption line shape with opposite-signed CD does not exclude linear dichroism/birefringence contamination, thickness differences, or orientation effects.

Steady-state electroluminescence DOCP can depend on generation, injection, spin transport, radiative recombination, photon extraction, and sample/device geometry. No unique spin relaxation lifetime can be calculated from these data.

Two OSF Extended Data tables are numerically duplicated, so treating their entries as separate replications would inflate confidence.

## Reproduce

```powershell
python -m pip install -e ".[dev,viz]"
python -m chiral_perovskites.chiral_device_pilot fetch
python -m chiral_perovskites.chiral_device_pilot analyze
python -m pytest -q
```

Outputs: `results/osf_chiral_optical_device_audit.json`,
`results/osf_chiral_cd_abs_pair.png`, and
`results/osf_chiral_device_docp.png`.

## Next GO / NO-GO

**GO (limited):** use this work as a documented static optical/device control and a transferable reference for discussions with different chiral-perovskite groups.

**HOLD:** quantitative spin-lifetime physics until matched R/S time-resolved data with calibration and instrument response are obtained. To relate chirality to device behavior causally, independent fabrication batches, substrate/film orientation, optical anisotropy and identical-device configuration controls are needed.

No ML regression, DFT or mechanism-fitting follows from the present archive alone.
