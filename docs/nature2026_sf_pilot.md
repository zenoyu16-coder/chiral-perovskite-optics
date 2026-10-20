# Reproduction of chiral superfluorescence polarization (Nature 2026)

Source: Wei et al., *Nature* 654, 369–374 (2026), [DOI 10.1038/s41586-026-10637-x](https://doi.org/10.1038/s41586-026-10637-x), publisher Source Data Fig. 3 (XLSX). Local source SHA-256:
`4f06825a839ba470e96fc45d9587db4d5f42067c41b2d03762e26ed64d217c29`.

## Scope

One experimental observation: reproduce the sign and magnitude of the **peak transient circular-polarization contrast** from the paper's R/S superlattice emission traces.

These samples are vertically aligned quasi-2D perovskite **superlattices** with mixed PEA and R- or S-MBA spacers, predominantly n=3. They are not the pure `(R/S-MBA)2PbI4` structures analyzed in our earlier crystal baseline, nor the 2024 spin-LED injection devices. The optical observations are never merged at the sample level.

The deposited Fig. 3 workbook has:
- Fig. 3b: time-integrated LCP/RCP PL spectra for SMBA and RMBA.
- Fig. 3c: 1,399 sampled delays, -59.6505 to 428.95 ps, with paired emission channels for both handedness classes.
- Fig. 3d: experimental peak DCP versus pump fluence, together with separate theory curves.

Fig. 3c was recorded using 550 nm linearly polarized excitation at 300 µJ cm^-2. The paper reports an approximately 10 ps streak-camera resolution; the 0.3495 ps *array sampling interval* is not the instrumental temporal resolution or a set of independent repeats.

## Observable and numerical result

At the maximal total emission intensity, use the same deposited time index for the two helicity channels:

`DCP0(t_peak) = (I_LCP(t_peak) - I_RCP(t_peak)) / (I_LCP(t_peak) + I_RCP(t_peak))`.

| Source check | SMBA | RMBA |
|---|---:|---:|
| Fig. 3c direct source arrays; DCP0 | +13.4949% | -13.7612% |
| Fig. 3c baseline-corrected; -60 to -40 ps | +13.5188% | -13.8066% |
| Four baseline-window definitions; DCP0 range | +13.5128 to +13.5292% | -13.8106 to -13.7986% |
| Independent Fig. 3d deposited plotting point near 300 µJ cm^-2 | +13.5290% (296.09) | -13.6620% (294.88) |

The Fig. 3d data point is an internal consistency check of the same published study, not an independent laboratory replication. That worksheet calls the axis `DOP0 (%)` but stores the values as fractions (e.g. 0.13529 for 13.529%). The script explicitly treats them as fractions.

The two peak times in the deposited source arrays are about 53.24 and 46.25 ps. They are **not** interpreted as an intrinsic handedness-dependent delay, given separate samples and approximately 10 ps instrument resolution.

For describing the measured polarization near the burst, the script also reports the median source-channel contrast where baseline-corrected total emission exceeds 20% of its peak. This gate excludes weak-signal divisions; its median is *descriptive*, with no kinetic fit or sub-ps uncertainty implied.

## Source labeling issue

The two RMBA columns in Fig. 3c are both literally headed `Intensity (RMBA LCP)`, while Fig. 3b labels RMBA LCP/RCP explicitly. The Nature article and Fig. 3d report RMBA DCP of negative sign. Treat the second Fig. 3c column as **RMBA channel 2**, provisionally consistent with RCP; do not silently relabel the original workbook or claim author confirmation.

## Reproduce

```powershell
python -m pip install -e ".[dev,viz]"
python -m chiral_perovskites.nature_sf_pilot fetch
python -m chiral_perovskites.nature_sf_pilot analyze
python -m pytest -q
```

The `fetch` command checks the exact publisher-source SHA-256; if the publisher revises the file, it halts and requires manual review. Source data remain under git-ignored `data/raw/kinetics/`.

Outputs:
- `results/nature2026_sf_fig3c_audit.json` — numbers, source metadata, internal Fig. 3d comparison and baseline-window sensitivity.
- `results/nature2026_sf_fig3c_reproduction.png` — source transient PL and intensity-gated circular-polarization contrast.

## Scientific outcome

We reproduced the published R/S sign reversal with an original source workbook. There is no independent new physical mechanism identified by this exercise. The figure arrays provide no separate raw camera frames, sample-to-sample replication, wavelength/collection calibration or independently measured transient spin observable.

**Decision: complete this single-figure pilot and stop here.** Further physical inference would require a discriminating experiment beyond Fig. 3: independently acquired polarization-resolved transients across matched R/S/achiral controls, pump fluence and orientation, with documented camera response. Larger fitting, DFT and ML would not currently improve evidence.
