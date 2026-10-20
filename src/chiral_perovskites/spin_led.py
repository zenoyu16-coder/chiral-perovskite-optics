"""Absorption, CD and electroluminescence polarization in chiral spin-LEDs."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np

PAPER_DOI = "10.1038/s41586-024-07560-4"
SOURCE_DOI = "10.17605/OSF.IO/2M35K"
FILES = {
    "optical": ("Extended_data_fig_8_Absorbance_CD_CPL.txt",
                "https://osf.io/download/65b2918b4aa63c0777df18b3/"),
    "device": ("Fig_2c_current_vs_DOCP.txt",
               "https://osf.io/download/65b28ad5973819072c396b67/"),
    "repeat_a": ("Extended_data_fig_4b_polvscurrent_device1b.txt",
                 "https://osf.io/download/5gm7n/"),
    "repeat_b": ("Extended_data_fig_5b_polvscurrent_device3b.txt",
                 "https://osf.io/download/66671e4365e1de54cf8940a0/"),
}


def get_sources(data_dir: Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    records = {}
    for key, (name, uri) in FILES.items():
        path = data_dir / name
        if not path.is_file():
            with urlopen(Request(uri, headers={"User-Agent": "chiral-perovskite-optics/0.4"}),
                         timeout=45) as response:
                content = response.read()
            if not content or b"polarization" not in content.lower() and key != "optical":
                raise ValueError(f"Unexpected content for {key}")
            path.write_bytes(content)
        records[key] = {
            "name": name, "url": uri,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size
        }
    return records


def rows_tsv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        records = list(csv.DictReader(handle, delimiter="\t"))
    if not records or any(None in r for r in records):
        raise ValueError(f"Malformed TSV: {path.name}")
    return records


def numeric_pair(rows: list[dict], x: str, y: str) -> tuple[np.ndarray, np.ndarray]:
    paired = []
    for row in rows:
        a, b = row.get(x), row.get(y)
        if a not in (None, "") and b not in (None, ""):
            paired.append((float(a), float(b)))
    if len(paired) < 3:
        raise ValueError(f"Insufficient paired rows for {x} and {y}")
    result = np.asarray(paired)
    if not np.isfinite(result).all():
        raise ValueError("Non-finite data")
    return result[:, 0], result[:, 1]


def consistency_metrics(rows: list[dict]) -> dict:
    """R/S pairs are wavelength-aligned in source columns, NOT paired specimens."""
    wl_r, r_cd = numeric_pair(rows, "wavelength", "CDRMBA")
    wl_s, s_cd = numeric_pair(rows, "wavelength", "CDSMBA")
    wl_a, r_abs = numeric_pair(rows, "wavelengthABS", "ABSRMBA")
    wl_b, s_abs = numeric_pair(rows, "wavelengthABS", "ABSSMBA")
    if not np.array_equal(wl_r, wl_s) or not np.array_equal(wl_a, wl_b):
        raise ValueError("Spectral axes are not aligned")
    if not np.all(np.diff(wl_r) > 0):
        raise ValueError("CD wavelengths must ascend")
    if len(np.unique(wl_a)) != len(wl_a):
        raise ValueError("Absorption wavelengths not unique")
    anticorrelation = float(np.corrcoef(r_cd, s_cd)[0, 1])
    abs_corr = float(np.corrcoef(r_abs, s_abs)[0, 1])
    denominator = float(np.linalg.norm(r_cd - s_cd))
    if denominator == 0:
        raise ValueError("Cannot assess antisymmetry when R=S")
    mismatch = float(np.linalg.norm(r_cd + s_cd) / denominator)
    scale = float(np.linalg.norm((r_abs + s_abs) / 2))
    if scale == 0:
        raise ValueError("Cannot normalize zero absorbance")
    return {
        "cd_points": len(r_cd),
        "cd_wavelength_nm": [float(wl_r.min()), float(wl_r.max())],
        "abs_points": len(r_abs),
        "abs_wavelength_nm": [float(wl_a.min()), float(wl_a.max())],
        "cd_R_S_pearson": anticorrelation,
        "cd_antisymmetry_residual_ratio": mismatch,
        "abs_R_S_pearson": abs_corr,
        "abs_relative_l2_difference": float(np.linalg.norm(r_abs - s_abs) / scale),
        "unit_note": "The raw CD header does not specify measurement units.",
        "caution": "Wavelength samples are correlated; the optical and device datasets do not establish same-specimen pairing.",
    }


def device_metrics(rows: list[dict]) -> dict:
    vals = []
    for row in rows:
        try:
            vals.append({
                "current_from_column_1": float(row["current1M"]),
                "channel_A": float(row["polarization"]),
                "channel_B": float(row["polarization1"]),
                "reported_error_A": float(row["error"]),
                "reported_error_B": float(row["error1"]),
            })
        except (ValueError, TypeError, KeyError) as exc:
            raise ValueError("Malformed current/DOCP source columns") from exc
    for name in ("channel_A", "channel_B", "reported_error_A", "reported_error_B"):
        if not np.all(np.isfinite([v[name] for v in vals])):
            raise ValueError(f"Invalid {name}")
    if any(v["reported_error_A"] < 0 or v["reported_error_B"] < 0 for v in vals):
        raise ValueError("Negative reported error")
    opposite = sum(v["channel_A"] * v["channel_B"] < 0 for v in vals)
    return {
        "source_columns": ["current1M", "polarization", "polarization1", "error", "error1"],
        "n_current_rows": len(vals),
        "opposite_sign_rows": opposite,
        "raw_channel_assignment": "A=polarization, B=polarization1; corresponding enantiomers are unidentified in the TSV.",
        "uncertainty_note": "The file does not define the statistical meaning of error/error1.",
        "rows": vals,
    }


def duplicate_numeric_tables(a: Path, b: Path) -> bool:
    left = np.loadtxt(a, skiprows=1, ndmin=2)
    right = np.loadtxt(b, skiprows=1, ndmin=2)
    return bool(left.shape == right.shape and np.array_equal(left, right))


def create_figures(optical: list[dict], device: list[dict], out_dir: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    out_dir.mkdir(parents=True, exist_ok=True)
    r_wl, r_cd = numeric_pair(optical, "wavelength", "CDRMBA")
    s_wl, s_cd = numeric_pair(optical, "wavelength", "CDSMBA")
    a_wl, r_abs = numeric_pair(optical, "wavelengthABS", "ABSRMBA")
    _, s_abs = numeric_pair(optical, "wavelengthABS", "ABSSMBA")
    fig, axes = plt.subplots(2, 1, figsize=(8, 8), constrained_layout=True)
    axes[0].plot(r_wl, r_cd, label="R-MBA CD")
    axes[0].plot(s_wl, s_cd, label="S-MBA CD")
    axes[0].axhline(0, color="gray", linewidth=0.7)
    axes[0].set(ylabel="Deposited CD (unit not specified)", title="Chiral optical spectra (independent published samples)")
    axes[1].plot(a_wl, r_abs, label="R-MBA absorbance")
    axes[1].plot(a_wl, s_abs, label="S-MBA absorbance")
    axes[1].set(xlabel="Wavelength (nm)", ylabel="Absorbance (deposited units)")
    for ax in axes: ax.legend()
    fig.savefig(out_dir / "osf_chiral_cd_abs_pair.png", dpi=180)
    plt.close(fig)

    xs=np.asarray([float(row["current1M"]) for row in device])
    a=np.asarray([float(row["polarization"]) for row in device])
    b=np.asarray([float(row["polarization1"]) for row in device])
    ea=np.asarray([float(row["error"]) for row in device])
    eb=np.asarray([float(row["error1"]) for row in device])
    order=np.argsort(xs)
    fig, ax=plt.subplots(figsize=(7.5, 4.8), constrained_layout=True)
    ax.errorbar(xs[order], a[order], yerr=ea[order], marker="o", capsize=3, label="polarization (source column)")
    ax.errorbar(xs[order], b[order], yerr=eb[order], marker="s", capsize=3, label="polarization1 (source column)")
    ax.axhline(0,color="gray",linewidth=0.8)
    ax.set(xlabel="Applied current (raw source values; units via article)", ylabel="Degree of circular polarization (source values)", title="Published spin-LED data — column identities require figure verification")
    ax.legend(fontsize=8)
    fig.savefig(out_dir/"osf_chiral_device_docp.png",dpi=180)
    plt.close(fig)


def main(argv=None) -> int:
    parser=argparse.ArgumentParser(description="Audit experimental chiral spin-LED optical/device data")
    parser.add_argument("command",choices=("fetch","analyze"))
    parser.add_argument("--data-dir",type=Path,default=Path("data/raw/osf_2m35k"))
    parser.add_argument("--out-dir",type=Path,default=Path("results"))
    args=parser.parse_args(argv)
    manifest=get_sources(args.data_dir) if args.command=="fetch" else {
        k: {"name":name,"url":url,"sha256":hashlib.sha256((args.data_dir/name).read_bytes()).hexdigest()}
        for k,(name,url) in FILES.items()
    }
    if args.command=="fetch":
        print(json.dumps(manifest,indent=2))
        return 0
    optical=rows_tsv(args.data_dir/FILES["optical"][0])
    device=rows_tsv(args.data_dir/FILES["device"][0])
    report={
        "paper_doi":PAPER_DOI, "source_doi":SOURCE_DOI, "files":manifest,
        "optical":consistency_metrics(optical),
        "device":device_metrics(device),
        "duplicate_extended_fig_4b_and_5b":
            duplicate_numeric_tables(args.data_dir/FILES["repeat_a"][0], args.data_dir/FILES["repeat_b"][0]),
        "scope":"Static/steady-state device and spectroscopy; NOT time-resolved chiral spin lifetime data.",
    }
    args.out_dir.mkdir(parents=True,exist_ok=True)
    (args.out_dir/"osf_chiral_optical_device_audit.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    create_figures(optical,device,args.out_dir)
    print(json.dumps({"optical":report["optical"],"device_n":report["device"]["n_current_rows"],
      "device_opposite_sign":report["device"]["opposite_sign_rows"],
      "duplicate_fig_4b_5b":report["duplicate_extended_fig_4b_and_5b"]},indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
