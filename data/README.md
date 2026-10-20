# Data sources

Source files are retrieved from the original publishers or research repositories. The `data/raw/` directory is excluded from version control; the tracked files contain source identifiers, derived results, figures and hashes.

| System | Measurement | Reference and raw source | Code |
| --- | --- | --- | --- |
| R/S/rac NEA₂PbBr₄, 298 K | Single-crystal CIF | [Jana et al. (2020)](https://doi.org/10.1038/s41467-020-18485-7), [Duke HybriD3](https://materials.hybrid3.duke.edu/), datasets 1583, 1584, 1588 | `nea_analysis.py` |
| S-MBA₂PbI₄, 100/200/298 K | Single-crystal CIF | Same publication, Duke datasets 1587, 1586, 1585 | `mba_temperature.py` |
| S-NEA₂PbBr₄ film | Front/back CD and absorption | [Sercel et al. (2025)](https://doi.org/10.1002/adma.202415901), Duke datasets 2784, 2785 | `nea_analysis.py` |
| Nonchiral BA₂FAPb₂I₇ | Polarization-resolved transient absorption | [Bourelle et al. (2020)](https://doi.org/10.1021/acs.nanolett.0c00867), [Cambridge CAM.54010](https://doi.org/10.17863/CAM.54010) | `transient_absorption.py` |
| R/S-MBA optical spectra and spin-LEDs | CD, absorption, electroluminescence polarization | [Hautzinger et al. (2024)](https://doi.org/10.1038/s41586-024-07560-4), [OSF 2M35K](https://doi.org/10.17605/OSF.IO/2M35K) | `spin_led.py` |
| R/S-MBA and PEA superlattices | Polarization-resolved TRPL, fluence response | [Wei et al. (2026)](https://doi.org/10.1038/s41586-026-10637-x), Source Data Fig. 2/3 and Extended Data Figs. 6/7 | `polarized_pl.py`, `fluence_response.py` |

## Crystallographic identifiers

`nea_sources.csv` stores the 298 K NEA₂PbBr₄ CIFs: S (CCDC 2015618), R (CCDC 2015620) and racemic (CCDC 2015614). `sources.csv` stores the three temperatures for S-MBA₂PbI₄.

The NEA single-crystal structures and the separately published S-NEA thin-film optical spectra are distinct experimental specimens. The same applies to the 2024 spin-LED devices and the 2026 superlattices. A numerical association across these datasets does not imply a sample-level correlation.

## Publisher source workbooks

The four XLSX files used for the superfluorescence comparison are downloaded with `python -m chiral_perovskites.fluence_response --fetch`. Source Data Fig. 2 and Fig. 3 and Extended Data Figs. 6/7 are verified against fixed SHA-256 hashes in `fluence_sources.py`. The Extended Data Fig. 7 workbook was retrieved through Springer's `static-content.springer.com` endpoint; the alternative `media.springernature.com` response returned HTML rather than an XLSX.

The 2026 figure-source files contain processed plotting arrays rather than independent raw camera acquisitions. Fig. 3c labels both RMBA channels as LCP; the signal comparison is compatible with the expected opposing helicity, but the original label is preserved in the audit. The RMBA time-series sheet lists a nominal 85 µJ cm⁻² trace where the separate intensity sheet lists 82 µJ cm⁻².

## Other provenance notes

The 2024 OSF optical table has separate wavelength axes for CD, absorption and PL in a single tab-delimited file. Missing cells must be preserved while reading; ordinary whitespace splitting shifts columns. Two deposited extended-figure tables contain identical numerical data and are not counted as independent device replicates.

The 2025 Duke CD dataset labels a third trace as an average of the front and back measurements. Its numerical values correspond to their sum within rounding. The archived curve and a separately calculated arithmetic mean are both retained in `results/cd_front_back_comparison.csv`.

The Cambridge data are nonchiral; the six deposited transient-absorption channels are retained with their original `||` and `X` labels. They are used for methodological comparison, not evidence of chirality.

The complete derived-file inventory and fingerprints are in [results/manifest.json](../results/manifest.json). Refer to the source studies for original sample preparation, measurement calibration and figure conventions.
