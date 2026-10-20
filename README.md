# Chiral Perovskite Optics

A small, structure-first exploration of **chirality, crystal geometry, and optical response** in layered hybrid perovskites.

**Scientific question:** Under which controlled structural and measurement conditions can an organic enantiomer produce an observable chiroptical semiconductor response?

This is a learning and exploratory repository, not a paper-oriented molecular-screening or DFT project. No unverified mechanism claims, trained predictors, or invented optical measurements.

## First completed pilot: temperature series in S-MBA2PbI4

The initial experimental structures are **S-(alpha-methylbenzylammonium)2PbI4**, measured at **298, 200, and 100 K** and hosted by the Duke Hybrid Organic–Inorganic Materials Database. All three come from the same paper:

Jana *et al.*, *Nature Communications* **11**, 4699 (2020), [doi:10.1038/s41467-020-18485-7](https://doi.org/10.1038/s41467-020-18485-7).

The pilot calculates:
- Space-group assignment and whether the reported symmetry contains improper operations (Sohncke test).
- Unit-cell volume **per Pb**, which is less sensitive to changes in cell setting than raw unit-cell volume.
- Mean nearest-neighbor Pb–I distance, bond-length distortion index, and PbI6 cis-angle variance.
- CIF SHA-256 and source identifiers so each derived row is traceable.

**Important:** A Sohncke space group allows a chiral structure, but does not establish R/S absolute configuration. PbI6 distortions do **not** quantify optical chirality or prove chirality transfer. The present data have *only S* structures, so they cannot establish a R/S effect.

## Run locally

Requires Python >=3.10. The first run downloads about 1–2 MB of CIF/ZIP data from their original public database.

```powershell
python -m pip install -e ".[dev]"
chiral-pv fetch
chiral-pv analyze
python -m pytest -q
```

Without installing the CLI entry point, use `python -m chiral_perovskites fetch` and `python -m chiral_perovskites analyze` after `pip install -e .`.

The source manifest is `data/sources.csv`. Raw CIF files stay under `data/raw/` and are **not redistributed in Git**. Derived output is `results/temperature_summary.csv`.

To check geometry robustness, repeat with e.g. `chiral-pv analyze --symprec 0.01 --cutoff 3.6 --out results/sensitivity.csv`. Do not treat any single symmetry tolerance or neighbor cutoff as definitive.

## Exploration after the pilot

1. Obtain an **R/S experimental crystal pair at matched temperature, composition and polymorph**; check CIF provenance and absolute-structure assignment. Do not compare incompatible crystal settings as if they shared Cartesian axes.
2. Assemble actual absorption/CD/LD and sample-orientation metadata for that pair. See [optical measurement protocol](docs/optical-data-protocol.md).
3. Ask whether an observed difference survives controls for crystal phase, film orientation and optical anisotropy. Only then decide if electronic-structure modelling adds explanatory value.

No DFT or ML is scheduled until a measurable discrepancy makes it necessary.

## Caveats

Experimental CIFs can contain disorder, occupancy issues or uncertain H positions. This first analysis rejects partial occupancy rather than making invisible repairs. The geometric descriptors average over intact PbI6 octahedra within a stated cutoff; `pb_sites_skipped` reports sites without exactly six I neighbors. Octahedral angle variance is geometric and does not provide a confidence interval. Comparing volumes per Pb assumes the structures have compatible chemistry and crystallographic identification.

Source papers to read:
- [Jana et al. (2020), structure chirality transfer](https://doi.org/10.1038/s41467-020-18485-7)
- [Sheikh et al. (2022), R/S-MBA2PbI4 photophysics and CIF supplements](https://doi.org/10.1039/D2CC01811J)
- [Scalon et al., Tuning Phase Purity in Chiral 2D Perovskites](https://doi.org/10.1002/adom.202300776)
- [Large exchange-driven intrinsic circular dichroism (2024)](https://doi.org/10.1038/s41467-024-46851-2)

Code in this repository is available under the MIT license. Original experimental data remain attributed to their source providers.
