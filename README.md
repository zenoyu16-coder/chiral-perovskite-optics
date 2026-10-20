# Optical data from chiral layered perovskites

This started with a comparison of R-, S- and racemic NEA₂PbBr₄ crystal structures. The symmetry assignments were straightforward, but the available optical measurements were made on different crystals or thin films. There was no direct way to relate a particular octahedral distortion to a measured circular-dichroism signal.

I subsequently looked at published optical datasets that contained both polarization channels, especially the chiral superlattice measurements reported by Wei et al. in 2026. The repository contains the corresponding analysis scripts, selected plots and structural comparisons. All spectra and crystal structures are taken from the cited experimental studies.

## Time-resolved emission

Wei et al., [*Nature* **654**, 369–374 (2026)](https://doi.org/10.1038/s41586-026-10637-x), published polarization-resolved photoluminescence from superlattices made with R- or S-MBA. Source Data Fig. 3c contains 1,399 delay points for each sample, measured at a pump fluence of 300 µJ cm⁻².

![Time-resolved PL and polarization contrast](results/nature2026_sf_fig3c_reproduction.png)

Taking the left- and right-circular channels at the maximum of their summed intensity gives peak circular polarization of +13.49% for S-MBA and −13.76% for R-MBA. The corresponding values after subtracting the pre-burst background are +13.52% and −13.81%. Both agree with the published values near 300 µJ cm⁻².

There is a small but important issue in the Excel file: the second RMBA channel is also headed `LCP`. Its numerical values reproduce the negative polarization reported in the paper when treated as the opposite-helicity channel. The script preserves the deposited header and records this interpretation separately.

The source traces are sampled approximately every 0.35 ps, although the streak-camera resolution reported in the paper is about 10 ps. I have left the analysis at the measured polarization contrast rather than fitting a relaxation time to that sampling interval.

## Pump fluence and the PEA control

The same paper contains fluence-dependent PL for S-MBA, R-MBA and the nonchiral PEA superlattice. PEA also shows superfluorescence. The paper reports circularly polarized superfluorescence for the two chiral samples.

![Published PL fluence response and circular polarization](results/nature2026_fluence_control.png)

| Sample | Superfluorescence threshold reported by Wei et al. (µJ cm⁻²) |
| --- | ---: |
| S-MBA | 70 ± 10 |
| R-MBA | 95 ± 10 |
| PEA | 140 ± 10 |

These thresholds are taken from the paper's time-integrated PL analysis. The plotted intensity curves are normalized separately, since their raw detector units are not comparable between specimens.

Another mismatch occurs in the deposited RMBA data: Extended Data Fig. 7a has a time trace labeled 85 µJ cm⁻², whereas Fig. 7b lists an intensity point at 82 µJ cm⁻². The scripts keep these records separate.

## Other measurements

The [Hautzinger et al. spin-LED dataset](https://doi.org/10.1038/s41586-024-07560-4) has R/S-MBA absorption, CD and circularly polarized electroluminescence data. The absorption spectra nearly overlap (Pearson r = 0.9992), while the CD traces change sign but are not exact mirror images (r = −0.8752). The electroluminescence comes from an AlGaInP quantum well, so it is treated as a separate device experiment.

The [Jana et al. crystal structures](https://doi.org/10.1038/s41467-020-18485-7) give `P2₁` for R/S-NEA₂PbBr₄ and `P2₁/c` for the racemate at 298 K. The local Pb–Br geometry and a separate S-MBA₂PbI₄ temperature series are retained under `results/`. An additional front/back CD dataset and a nonchiral transient-absorption example were used to check source-file handling.

[Detailed results](docs/results.md) · [Methods](docs/methods.md) · [Original datasets](data/README.md)

## Running the analyses

Python 3.10 or later:

```bash
python -m pip install -e ".[dev,viz]"
python scripts/reproduce.py --fetch
python -m pytest -q
```

The first script downloads the original CIF and spectroscopy files and regenerates the plots and tables. When the input files are already present, `python scripts/reproduce.py` reruns the calculations without downloading them.

Source measurements stay in `data/raw/`, outside version control. `src/chiral_perovskites/` contains the analysis routines; `results/` contains the published-data comparisons. `python scripts/verify_results.py` checks the committed outputs against [their recorded hashes](results/manifest.json).

## Possible experiment

I have not collected new samples or polarization-resolved measurements for this repository. Before attempting a time-resolved chirality experiment, the practical first step is to establish whether reliable circular-polarization-resolved PL is available for matched R/S films, with sample rotation and polarization calibration. Without that measurement, further analysis of these published traces would mostly revisit the authors' results.

[Experimental notes](docs/experimental-follow-up.md) · [License](LICENSE) · [Citation](CITATION.cff)
