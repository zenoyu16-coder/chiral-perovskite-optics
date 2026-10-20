# Research log

## 2026-10-20 — Stage 1, S-MBA2PbI4 temperature baseline

Computed structural descriptors for experimentally deposited S-MBA2PbI4 at 298, 200 and 100 K (Jana et al., 2020). All retain P212121 in the chosen tolerance. This is a temperature series, not an enantiomeric comparison.

## 2026-10-20 — Stage 2, NEA2PbBr4 R/S/rac

Found matched 298 K experimental CIFs for R (Duke 1584, CCDC 2015620), S (1583, CCDC 2015618) and racemic (1588, CCDC 2015614). Downloaded and checked with pymatgen. R/S: P21 and near-equal scalar PbBr6 metrics. Racemic: P21/c and lower cis-angle distortion.

Computed signed b-projected Br-centroid/Pb displacement: R +0.034830 Å; S -0.034525 Å; rac ~0. Related microscopic polar distortion has been discussed by Sercel et al., 2025. This code makes no quantitative CD predictions.

Retrieved separate 2025 measured S-NEA thin-film CD data (Duke 2784). The deposited trace labelled 'average' is numerically front + back, not half their sum, within spectral rounding. This is an unresolved scale/metadata question, not a physics finding. No sample-level 2020–2025 merge.

Next: verify crystallographic convention and CD averaging protocol; only add modeling if a specific missing explanation emerges.


## 2026-10-20 — Stage 3: exciton dynamics data availability

After scientific audit of Stage 2, selected a more general physical question: polarization-resolved exciton relaxation and the extent to which a true chiral R/S control changes it. Initial literature/data inspection confirms that accessible papers and displayed plots do not guarantee independently reusable R/S-resolved ultrafast kinetics.

Downloaded a machine-readable, open **nonchiral** transient absorption trace from Cambridge [CAM.54010](https://doi.org/10.17863/CAM.54010). It contains 312 time points (-5 to 1750 ps) and six polarization-labeled columns. Independently coded input checks, baseline/noise summary and a channel plot. Header channels `||` and `X` are preserved without guessing which optical convention they represent. We do **not** fit a spin lifetime from this exercise.

The complete source survey, decisions, and go/no-go criteria are in `docs/dynamics-data-feasibility.md`. The study will only expand when original chiral R/S kinetic data (plus instrument response and measurement metadata) can be obtained.

## 2026-10-20 — Stage 4: public experimental chiral spin-LED optical/device baseline

Hautzinger et al., Nature 631 (2024) deposit real R/S-MBA2PbI4 CD/absorbance and spin-LED polarization data under OSF 2M35K. Downloaded sources, SHA-256 tracked, and wrote `chiral_device_pilot.py` with regression tests against ragged TSV column shifts.

The correct measured series counts are 401 CD rows, 501 absorbance rows and 696 PL rows. CD R/S correlation -0.8752, absorbance R/S correlation +0.9992; the two published polarization channel series have opposite reported signs at all six current values, but source TSV labels do not identify which channel is R/S. Also discovered that two extended-figure source tables have exactly equal numeric contents, so avoid counting them twice.

This is a descriptive steady-state cross-check, NOT the chiral pump-probe kinetics originally sought. Do not infer a spin-lifetime, chiral injection transfer efficiency or mechanistic CISS from these source files. See `docs/spin_led_data_pilot.md`.