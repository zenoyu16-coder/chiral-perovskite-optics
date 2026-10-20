# Chiral Perovskite Optics

Experimental-crystal-structure and spectroscopy exploration of chiral layered halide perovskites.

Question: Which experimentally observable optical and optoelectronic responses depend on molecular handedness, and which controls are needed before relating those signals to exciton or spin dynamics?

The repository uses real experimental data and keeps source provenance. There is no ML or DFT model at this stage.

## Stage 4 — experimental chiral optical/device control (current)

An unexpectedly useful open dataset comes from Hautzinger et al., *Nature* **631**, 307–312 (2024), [doi:10.1038/s41586-024-07560-4](https://doi.org/10.1038/s41586-024-07560-4), [raw OSF archive](https://doi.org/10.17605/OSF.IO/2M35K).

We reproduce R/S-MBA2PbI4 absorbance and CD spectra plus two reported spin-LED DOCP channels without inventing spin lifetimes or assigning unlabeled channel identities. Correctly parsing the ragged optical TSV is critical: it contains **401 CD**, **501 absorption**, and **696 PL** rows on different wavelength axes. The verified optical results give R/S absorbance correlation +0.9992 and CD correlation -0.8752. The two recorded device DOCP series have opposite signs at all 6 tabulated currents, but the TSV by itself does not assign each channel to R or S or establish independent device batches. Two other figure-source files contain exact duplicate numerical values and must not be counted as independent replicates.

See [data audit, limitations and decision gate](docs/spin_led_data_pilot.md).

```powershell
python -m pip install -e ".[dev,viz]"
python -m chiral_perovskites.chiral_device_pilot fetch
python -m chiral_perovskites.chiral_device_pilot analyze
python -m pytest -q
```

Derived plots and a source-hashed report are saved under `results/osf_chiral_*`. An additional bounded error-bar sensitivity check is available via `python -m chiral_perovskites.spin_led_gate` (6/6 raw opposite signs, 5/6 at ±1× source error and 4/6 at ±2×; **not** a confidence test). The source data stay untracked under `data/raw/`. This is a **static optical/device control**, while matched chiral time-resolved polarization data remain the unresolved gate. See [science decision checkpoint](docs/science_gate_2026-10-20.md) before expanding this branch.

## Stage 3 — exciton and polarization dynamics (data-access gate)

Before developing a kinetic mechanism, we audited availability of original, **matched R/S time-resolved polarization measurements**. See [data feasibility and acceptance criteria](docs/dynamics-data-feasibility.md). No complete downloadable R/S counterpart with independently verified timing/channel metadata has been secured yet.

As a **nonchiral methodological control**, we downloaded a plain-text polarization-resolved transient absorption dataset associated with Bourelle et al., *Nano Letters* (2020), [doi:10.1021/acs.nanolett.0c00867](https://doi.org/10.1021/acs.nanolett.0c00867), Cambridge [CAM.54010](https://doi.org/10.17863/CAM.54010). The published article identifies the studied material as BA2FAPb2I7.

```powershell
python -m pip install -e ".[dev,viz]"
python -m chiral_perovskites.dynamics_pilot fetch
python -m chiral_perovskites.dynamics_pilot audit
python -m pytest -q
```

This stage parses 312 time points and six deposition-labeled channels, checks baseline/noise, and plots traces. Results: `results/dynamics_cambridge_qa.json` and `results/dynamics_cambridge_channels.png`. Neither a spin lifetime nor a chiral effect is inferred from this archive. The next gate is access to a properly documented R/S or matched chiral/rac sample-level kinetic dataset.

## Stage 2 — matched NEA2PbBr4 (current)

We use original 298 K single-crystal CIFs from Jana et al., *Nature Communications* 11, 4699 (2020), doi: [10.1038/s41467-020-18485-7](https://doi.org/10.1038/s41467-020-18485-7):

| Sample | Duke ID | CCDC | Space group | Pb-Br mean (Å) | cis-angle variance (deg²) | Br-centroid shift along b (Å) |
|---|---:|---:|---|---:|---:|---:|
| S-NEA2PbBr4 | 1583 | 2015618 | P21 | 3.0344 | 40.173 | -0.034525 |
| R-NEA2PbBr4 | 1584 | 2015620 | P21 | 3.0366 | 40.467 | +0.034830 |
| rac-NEA2PbBr4 | 1588 | 2015614 | P21/c | 3.0267 | 19.749 | ~0 |

The signed quantity is the mean over Pb sites of the projected vector from Pb to the centroid of its six nearest Br neighbors. It uses the **deposited cell's positive b-axis**, not an independently fixed laboratory direction. The R/S sign reversal agrees with a polar-distortion motif discussed by Sercel et al. (2025); it is **not** a Berry-phase polarization or a quantitative CD prediction.

The raw racemic CIF gives **P21/c (No. 14)**, as confirmed from the file and symmetry analysis; this is the structure actually evaluated. The comparison uses separate crystals, so small R/S metric differences include experimental variation.

See [stage 2 interpretation and limitations](docs/nea-pilot.md).

### Reproduce

Python >=3.10:

```powershell
python -m pip install -e ".[dev]"
python -m chiral_perovskites.pilot2 matched-fetch
python -m chiral_perovskites.pilot2 matched-analyze
python -m pytest -q
```

Expected output: `results/nea_matched_298K.csv`. Use `--symprec 0.01` to repeat the space-group analysis at a tighter symmetry tolerance.

Raw CIFs are downloaded from Duke HybriD3 and are excluded from Git. `data/nea_sources.csv` records dataset, DOI, temperature, handedness and CCDC identifiers.

## Stage 2 — separate optical archive audit

An independent dataset from Sercel et al., *Advanced Materials* 37, 2415901 (2025), [doi:10.1002/adma.202415901](https://doi.org/10.1002/adma.202415901), contains measured front-side, back-side and a third “average” CD spectrum for a **S-NEA2PbBr4 thin film**, plus absorbance.

```powershell
python -m chiral_perovskites.pilot2 optical-fetch
python -m chiral_perovskites.pilot2 optical-audit
```

The 301 spectral points span 300–600 nm. The downloaded third CD trace is numerically equal to the **sum** of front and back curves (maximum deviation ~0.00008 mdeg), rather than their arithmetic mean. The archive may reflect a factor-of-two processing or plotting convention; this is an **unresolved metadata/normalization question**, not evidence of erroneous physics. Both the archived curve and a separately reconstructed arithmetic mean are retained, without overwriting either.

These 2025 film spectra do not refer to the same single crystals as the 2020 CIFs. Do not join them into a sample-level predictor.

Outputs: `results/cd_front_back_audit.json` and `results/cd_front_back_comparison.csv`.

## Stage 1 — S-MBA2PbI4 temperature series

The initial pilot used S-MBA2PbI4 single-crystal structures at 298, 200 and 100 K (Duke IDs 1585–1587; same 2020 paper). It measures volume per Pb, Pb-I bond lengths and octahedral distortion:

```powershell
chiral-pv fetch
chiral-pv analyze
```

Output: `results/temperature_summary.csv`. This series has only S structures; it is **not** an R/S comparison.

## Next questions

- Which structural handedness or polar-displacement quantity is invariant to a change of crystallographic axis setting, and how should its sign be established?
- How were front/back CD spectra combined in the 2025 dataset? Can we reproduce the displayed figure with documented scale factors?
- After excluding morphology-related apparent CD contributions, what optical signal remains, and can a simple physically defined geometric observable explain its sign?

We will only consider DFT or ML if a specific observation requires it.

Data license and credit: [Duke HybriD3](https://materials.hybrid3.duke.edu/). The analysis code is MIT licensed.
