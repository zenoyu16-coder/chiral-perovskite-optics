# Decision checkpoint — 20 October 2026

The source workbook identified below has since been inspected. Its Fig. 3c contains matched-delay SMBA/RMBA polarization-channel time traces; a one-figure numerical reproduction has been completed in [Stage 5](nature2026_sf_pilot.md). The original instrument-frame and independent-replicate limitations still apply. The numbered decisions below document the earlier pre-inspection scientific gate.

## The question we are actually pursuing

Can chiral halide-perovskite excitation produce an **experimentally resolved and reproducible difference in polarized emission/relaxation dynamics**, distinguished from ordinary population decay, sample orientation, interface effects and measurement artifacts?

We do not need a generalized molecular-design model or to publish a paper. We do need a measurable observable, independently interpretable controls, and a result that changes our understanding.

## What the completed pilots establish

- 2020 crystal structures (R/S/rac NEA2PbBr4): symmetry and Pb-halide structural baselines. A signed displacement along a deposited lattice vector is **basis-dependent** and not itself an absolute handedness measure.
- 2024 chiral spin-LED publication, OSF source data: static R/S optical CD and absorption traces plus DOCP-current records. Optical CD alone does not determine spin injection. The active emitting layer is an **AlGaInP quantum well**, while the chiral perovskite serves as an injection/filtering layer; this is not an intrinsic chiral-perovskite transient emission measurement.
- 2020 Cambridge dataset: open time-resolved channels from a **nonchiral** layered perovskite; suitable for data handling but not a chiral R/S effect.
- 2025 NEA thin-film CD: a front/back averaging/normalization provenance question; not an independent physics result.

### Final bounded spin-LED evidence check

Published source: Hautzinger et al., *Nature* 631, 307–312 (2024), DOI 10.1038/s41586-024-07560-4. Raw data: OSF 2M35K, Fig. 2c. Our reproducible code reads the two original source columns `polarization` and `polarization1`.

| Descriptive comparison | Current points |
|---|---:|
| Opposite raw channel signs | 6/6 |
| Both intervals y ± 1 × deposited error do not cross zero | 5/6 |
| Both intervals y ± 2 × deposited error do not cross zero | 4/6 |

The error column's statistical meaning is unverified. This calculation **does not** assign confidence levels, imply independent device replications, or establish the sign of a microscopic spin polarization. The six measurements are a current series, not six independent samples.

**Sign-convention discrepancy requiring provenance:** In the accessible *arXiv* preprint 2309.04559, near Fig. 2, the displayed definition P = (I_left-I_right)/(I_left+I_right), the assignment of R/S in panels 2a and 2b, and a nearby sentence assigning the signs to S and R do not all appear mutually consistent. The OSF Fig. 2c file has no R/S labels for the two polarization columns. Until the published version is checked, retain `channel_A`/`channel_B`, without guessing an enantiomer label. This is a **metadata question**, not a claim of an error in the Nature version of record.

**Pseudo-replication risk:** The OSF Extended Fig. 4b and 5b source tables have the same numeric contents. Do not count these as two independent devices without additional provenance.

## What we will NOT do next

No regression of CD magnitude against DOCP: the optical and electrical data do not establish same-sample pairing, sample thickness, texture, error conventions or a causal relationship. No ad hoc baseline optimization intended to force R/S CD into antisymmetry. No DFT study to explain a guessed mechanism. No spin lifetime from a steady-state figure.

The completed source audits are learning assets and will remain frozen unless a concrete factual mistake is found.

## Actual data-access opportunity (not yet verified locally)

Wei et al., *Nature* **654**, 369–374 (2026), [DOI 10.1038/s41586-026-10637-x](https://doi.org/10.1038/s41586-026-10637-x), report room-temperature **R/S-MBA-derived chiral perovskite superlattices** and polarization-resolved superfluorescence using time-resolved PL (streak camera). The publisher links machine-readable **Source Data Fig. 3** and **Source Data Extended Data Fig. 7** (including an RMBA time-resolved PL experiment).

The Fig. 3 XLSX has been downloaded to git-ignored `data/raw/kinetics/nature2026_source_fig3.xlsx` (209,136 bytes; SHA-256 `4f06825a839ba470e96fc45d9587db4d5f42067c41b2d03762e26ed64d217c29`). **Its individual worksheets and raw time channels have not been inspected** in this iteration. Source Data may consist of processed figure plotting arrays rather than underlying raw camera intensities. Their existence is not yet proof that the matched R/S `I_LCP(t)`/`I_RCP(t)` pair, calibration and IRF are available.

Candidate checks:
- Download Fig. 3 and Extended Data Fig. 7 XLSX via the publisher links, respecting source attribution.
- Determine exactly which sheets encode matched R/S polarization and *time*-resolved traces, not just intensity/fluence and integrated DCP.
- Identify excitation fluence, detection band, time resolution (~10 ps from article), sample identity and whether data are direct measurements or theoretical curves.
- If complete, reproduce **one plot only**, with a predeclared observable and control. Compare R vs S, and achiral PEA when the experimental conditions permit.
- If time-resolved paired channels are absent, archive the assessment and stop; do not create proxies or a theoretical mechanism.

## Decision

**Keep the domain; do not expand the spin-LED branch.** Stage 4's static chirality vs device response data do not answer the selected exciton-dynamics question. The only next experimental-data gate worth effort is inspecting the 2026 source workbook for genuine paired chiral time-resolved polarization measurements. If absent, hold work until better data become available.

This prevents repeating the FBA/CuCl and C13/C15 failure mode: generating increasingly elaborate descriptors before identifying an independently discriminating experiment.
