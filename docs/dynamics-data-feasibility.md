# Polarization-resolved exciton dynamics — data feasibility (20 October 2026)

**Research question.** For a fixed halide semiconductor phase, what sets the lifetime of a measured optical polarization contrast after excitation? Can genuinely chiral R/S controls reveal additional behavior beyond optical orientation present even in achiral samples?

A fit to a single exponential is **not** automatically a spin-flip lifetime. Carrier population decay, exciton annihilation, spectral overlap, instrument-response convolution, differential transition strengths, and optical anisotropy may all affect polarized transients.

## Sources assessed

| Source | Material / observable | Raw data status | Decision |
|---|---|---|---|
| Bourelle et al., *Nano Letters* (2020), DOI [10.1021/acs.nanolett.0c00867](https://doi.org/10.1021/acs.nanolett.0c00867), deposit [CAM.54010](https://doi.org/10.17863/CAM.54010) | **Nonchiral** layered BA2FAPb2I7; circular-polarization-resolved transient absorption, time-resolved PL / Faraday rotation discussed in article | Downloaded one 7-column kinetics file, 312 sampled delays; other Origin and ZIP files listed in archive | **GO for methods training only**. Explicitly not R/S comparison |
| Bhagwat, Lund master's thesis (2025), [full thesis](https://lup.lub.lu.se/student-papers/record/9211781/file/9211842.pdf) | R-MBA2PbI4 and rac-MBA2PbI4; circular pump-probe, polarization kinetics | Thesis PDF and displayed figures public; matching machine-readable original time traces **not verified** | Scientific match, but **HOLD for quantitative reanalysis** pending raw data |
| Ramakrishnan et al., *JACS* (2025), [paper](https://doi.org/10.1021/jacs.5c16029) | Chiral quasi-2D, layer-number variation, polarized spin relaxation | Paper/SI accessible in principle; matched machine-readable time traces **not verified** | HOLD; no independent channel-level data in hand |
| Liu et al., *JACS* (2025), [paper](https://doi.org/10.1021/jacs.5c05172) | Chiral low-dimensional perovskite heterostructures; polarization lifetime and orientation dependence | Public article record; machine-readable kinetics **not verified** | HOLD |
| Xiao et al., *Nature Communications* (2026), [paper](https://doi.org/10.1038/s41467-026-69455-4) | Chiral heterostructures; circular pump-probe and spin photovoltaics | Paper and SI public at [Cambridge repository](https://www.repository.cam.ac.uk/items/5fb39f17-29b7-4a90-ba73-f0830195f920); original raw traces **not verified** | HOLD |
| Fish et al., *J. Phys. Chem. Lett.* (2023), [Zenodo 7967407](https://doi.org/10.5281/zenodo.7967407) | Nonchiral 2D RP/DJ perovskites; ultrafast TA and EA | Public ZIP of measurement data | Secondary method-control possibility; no chiral labels |

The publication URLs are discovery references. **Only the Bourelle dataset's selected plain-text trace has been inspected numerically in this repository.** The data access labels distinguish a DOI/article from independently machine-readable matched kinetics.

## Additional matched chiral source data now verified

Wei et al., *Nature* 654 (2026), [DOI 10.1038/s41586-026-10637-x](https://doi.org/10.1038/s41586-026-10637-x), provide original **figure-source** LCP/second-helicity time-resolved traces for R/S-MBA-derived quasi-2D superlattices (Fig. 3c; 1,399 paired delays; 300 µJ cm^-2). We independently reproduced the published opposite-signed peak DCP at +13.49% / -13.76%. See [bounded reproduction and limits](nature2026_sf_pilot.md).

This clears the gate for a single published-result reproduction, **not** for a new spin/exciton lifetime mechanism. Individual raw camera image frames, independent fabrication batches and calibrated IRF measurements remain unavailable. The publisher's RMBA column 2 has a duplicated LCP header and is tracked as a source-label ambiguity.

## Actual audit performed

Cambridge open archive DOI 10.17863/CAM.54010 provides `FAI_575nm_20uW_Co_Cnt_Kinetics_552-557_574-579_590-595.txt` (exact source basename). The file has:
- 312 strictly increasing sampled delay times, from -5 to +1750 ps; 34 are negative (pre-pump).
- Six percent delta-transmission signals, grouped under verbatim header strings `||` (3) and `X` (3).
- Three spectral windows: 552-557, 574-579, and 590-595 nm, as named in filename.
- Source filename `Co_Cnt` suggests co/counter circular, but **header strings do not establish a sign or polarization convention**. We therefore do not compute a spin polarization, a decay lifetime, or a chirality-dependent metric.

Code validates filename content, finite data, increasing delays, baseline ranges, and reports channel-level amplitude/noise diagnostics; a plot shows the unnormalized baseline-corrected signals. Raw file is kept in git-ignored `data/raw/`; the summary and plot are tracked.

```powershell
python -m pip install -e ".[dev,viz]"
python -m chiral_perovskites.dynamics_pilot fetch
python -m chiral_perovskites.dynamics_pilot audit
python -m pytest -q
```

## Decision gate

Do **not** build a kinetic model of the R/S effect yet. Obtain at least one dataset with the following:
- R and S, ideally rac, under matched sample preparation, excitation density, phase, temperature and polarization convention;
- time axis, instrument-response or cross-correlation characterization, background-corrected raw co/counter signals and relevant calibration;
- distinct observable for exciton population dynamics, not only a polarization trace.

If unavailable, a reproducible methods exercise on the Cambridge data is sufficient. No invented chiral time traces, transfer-learning model, guessed spin lifetime, or DFT.
