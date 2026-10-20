# Matched crystal pilot — 2026-10-20

## Inputs

Jana et al. (2020), doi:10.1038/s41467-020-18485-7, deposited experimental 298 K crystal structures:
- R-NEA2PbBr4, CCDC 2015620, Duke dataset 1584.
- S-NEA2PbBr4, CCDC 2015618, Duke dataset 1583.
- rac-NEA2PbBr4, CCDC 2015614, Duke dataset 1588.

Their molecular formulas and nominal temperature match. They are *three distinct crystals*, not exact mirror-transformed computational copies. The source archive hashes are recorded in the derived result CSV.

## Computation

Read each raw CIF with pymatgen and determine the space group at symprec=0.05 Å, checking 0.01 Å as a sensitivity case. Every Pb must have exactly six Br neighbors within 3.7 Å; do not auto-repair missing ligands. For each octahedron calculate:

- Mean Pb–Br distance.
- Mean absolute bond length deviation divided by mean length (dimensionless).
- Squared cis-angle deviations from 90°, divided by 11 (deg²), for 12 cis pairs identified by minimizing trans-pair deviation.
- Mean trans angle (deg).
- Signed local centroid shift: b-hat dot [(1/6) sum_(6 Br) (r_Br - r_Pb)], averaged over Pb sites (Å).

The neighbor coordinates include periodic images selected by pymatgen. The last observable is **a local structural displacement**, not the material polarization. Its sign depends on the direction of b, so do not interpret it without an explicit crystallographic convention. Use experimental absolute-structure information to attach an R/S label.

## Observations

S and R both adopt P21 (No. 4); their unit-cell volume per Pb differs by only 0.193% and their mean Pb–Br distances by 0.072%. Their local Br centroid shifts along b are -0.034525 and +0.034830 Å, respectively.

The racemic CIF has P21/c (No. 14), inversion symmetry, and zero net b-projected Br centroid shift. Its cis-angle variance (19.749 deg²) is lower than both R and S (~40.2 deg²). Ordinary scalar octahedral distortion and the sign of a polar structural displacement are therefore different questions.

This reproduces a known structural motif; it is not a novel effect. No optical activity follows automatically from the structural result.

## Separate spectroscopy context

Sercel et al. (2025), doi:10.1002/adma.202415901, modeled chiral excitons in R/S-NEA2PbBr4 and compared with measured CD on S-NEA thin films. Duke archived the spectra in datasets 2784 (CD) and 2785 (absorption).

The CD archive has three wavelength-aligned columns stored in separate files described as front, back, and average. Numerical verification across all 301 wavelengths shows that the deposited 'average' equals front + back to within 0.00008 mdeg, not (front + back)/2. The corresponding two possible scalings are kept separate in CSV and audit JSON. We have not established the plotting convention; **do not treat the factor-of-two as a confirmed error**.

No 2025 thin-film CD value is merged with a 2020 single-crystal geometry measurement as if taken on the same specimen.

## Go / no-go

Proceed to interpretation only if:
- signed displacement survives symmetry-tolerance and nearest-neighbor robustness checks;
- R/S relative axis assignments and absolute-structure labels can be traced through source CIFs;
- the optical front/back treatment is clarified, including signs and scale factors;
- a follow-up has a genuinely independent observation to explain.

Otherwise finish this pilot as a reproducible exercise and choose a different well-characterized material.
