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

## 2026-10-20 — Scope and evidence gate after Stage 4

Rechecked the Nature 2024 spin-LED paper against its 2023 arXiv manuscript Fig. 2. The preprint has an apparent handedness-to-sign inconsistency across panel labels, intensity convention and adjacent prose; the underlying OSF source data do not explicitly label the two DOCP series as R and S. Accordingly the analysis keeps anonymous A/B labels.

New bounded uncertainty test, using deposited Fig. 2c errors without assigning their statistical interpretation: raw signs opposite 6/6 current settings; both A/B error intervals avoid zero at 1x error for 5/6 and 2x error for 4/6. Current points are not independent fabricated devices. See `results/spin_led_uncertainty_gate.json` and `docs/science_gate_2026-10-20.md`.

Found Wei et al., Nature 654 (2026), DOI 10.1038/s41586-026-10637-x, with R/S chiral perovskite superfluorescence, a time-resolved Fig. 3 and publisher XLSX Source Data. Downloaded Fig. 3 XLSX only; its columns and sample-level pairing are NOT yet verified. This is the next data-access checkpoint. Do not expand spin-LED correlations or fit a kinetic mechanism without validated matched raw data.


## 2026-10-20 — Stage 5: real R/S time-resolved chiral superfluorescence

Source Data Fig. 3 of Wei et al., Nature 654 (2026), DOI 10.1038/s41586-026-10637-x, retrieved (209,136 byte XLSX). Fig. 3c has 1399 matched-delay sample points for SMBA and RMBA helicity-channel emission. Validated against the deposited experimental Fig. 3d curve. Reproduced peak DCP0 +13.4949% (SMBA) and -13.7612% (RMBA), near the reported +13.5%/-13.8%. Baseline corrections do not change their signs or magnitude materially. RMBA Fig. 3c carries two literal 'LCP' headers; this is flagged rather than silently repaired.

Reproducible code plus tests in `nature_sf_pilot.py`; raw figure workbook not redistributed. The 0.3495 ps source sampling step is far finer than the reported ~10 ps camera temporal resolution. Different sample peak times are not interpretable as intrinsic handedness delays. This is the completed single-observation pilot and does not justify a spin/exciton lifetime fit or large DFT/ML work. See `docs/nature2026_sf_pilot.md`.


## 2026-10-20 — Stage 6: chiral/achiral fluence controls and stopping decision

Downloaded and verified publisher source workbooks for Wei et al. Nature 2026 SMBA, RMBA, and PEA superlattice pump-fluence series (Fig. 2c; Extended Data Figs. 6a,b / 7a,b; Fig. 3d). The initial ED7 link returned HTML, which was rejected and replaced by the publisher's valid static-content Excel. Four source SHA-256 hashes are pinned in `fluence_sources.py`.

The source lists 10 SMBA, 10 RMBA and 12 PEA peak-intensity points. Nonchiral PEA has nonlinear superfluorescence, so collective emission does not itself require molecular chirality. Published *time-integrated* SF thresholds are 70±10, 95±10, 140±10 µJ cm^-2 for S,R,PEA. Simple 2x propagated-error rules for source DCP identify the first sampled nonzero S/R points at 95.4 and 134.66 µJ cm^-2; these are NOT new physical thresholds.

Found an 85 (ED7a) vs 82 (ED7b) µJ cm^-2 labelling inconsistency in RMBA source workbooks. No row-index merging or imputed condition is permitted.

Science gate: the main claims and detailed quantum-optics mechanism belong to the authors. This is a faithful control-focused replication, and does not independently establish structural cause, spin lifetime, or an original result. Future useful work requires an experiment with independent R/S/PEA batches, paired LCP/RCP time-resolved measurements, comparable growth and pump/collection conditions, and calibrated IRF. Freeze public-data analysis now rather than multiplying descriptors. See `docs/nature2026_fluence_controls.md`.
