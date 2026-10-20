# Research log

## 2026-10-20 — Stage 1, S-MBA2PbI4 temperature baseline

Computed structural descriptors for experimentally deposited S-MBA2PbI4 at 298, 200 and 100 K (Jana et al., 2020). All retain P212121 in the chosen tolerance. This is a temperature series, not an enantiomeric comparison.

## 2026-10-20 — Stage 2, NEA2PbBr4 R/S/rac

Found matched 298 K experimental CIFs for R (Duke 1584, CCDC 2015620), S (1583, CCDC 2015618) and racemic (1588, CCDC 2015614). Downloaded and checked with pymatgen. R/S: P21 and near-equal scalar PbBr6 metrics. Racemic: P21/c and lower cis-angle distortion.

Computed signed b-projected Br-centroid/Pb displacement: R +0.034830 Å; S -0.034525 Å; rac ~0. Related microscopic polar distortion has been discussed by Sercel et al., 2025. This code makes no quantitative CD predictions.

Retrieved separate 2025 measured S-NEA thin-film CD data (Duke 2784). The deposited trace labelled 'average' is numerically front + back, not half their sum, within spectral rounding. This is an unresolved scale/metadata question, not a physics finding. No sample-level 2020–2025 merge.

Next: verify crystallographic convention and CD averaging protocol; only add modeling if a specific missing explanation emerges.
