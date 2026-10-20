"""Polarization-resolved transient absorption in a nonchiral layered perovskite."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np

DATASET_DOI = "10.17863/CAM.54010"
PAPER_DOI = "10.1021/acs.nanolett.0c00867"
SOURCE_URL = (
    "https://api.repository.cam.ac.uk/server/api/core/bitstreams/"
    "8db61f35-266f-474a-952a-7a7015e85645/content"
)
RAW_FILENAME = "FAI_575nm_20uW_Co_Cnt_Kinetics.txt"
DATASET_MATERIAL = "BA2FAPb2I7 (nonchiral reference; paper nomenclature)"
TIME_WINDOWS = ("552-557 nm", "574-579 nm", "590-595 nm")
GROUPS = ("|| (source header)", "X (source header)")


def fetch(destination: Path) -> dict:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.is_file():
        with urlopen(Request(SOURCE_URL, headers={"User-Agent": "chiral-perovskite-optics/0.3"}), timeout=60) as response:
            payload = response.read()
        if not payload.startswith(b"Time\t"):
            raise ValueError("Downloaded data has unexpected header")
        destination.write_bytes(payload)
    return {"raw_file": str(destination), "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
            "byte_count": destination.stat().st_size, "dataset_doi": DATASET_DOI, "source_url": SOURCE_URL}


def parse(path: Path) -> np.ndarray:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if len(lines) < 20 or not lines[0].startswith("Time") or "ps" not in lines[1]:
        raise ValueError("Unexpected Cambridge kinetics header/units")
    if lines[2].split() != ["||", "||", "||", "X", "X", "X"]:
        raise ValueError("Source channel labels have changed; verify manuscript before proceeding.")
    arr = np.loadtxt(path, skiprows=3, ndmin=2)
    if arr.shape[1] != 7 or len(arr) < 20:
        raise ValueError("Expected one time column and six response columns")
    if not np.isfinite(arr).all() or not np.all(np.diff(arr[:, 0]) > 0):
        raise ValueError("Time axis not strictly increasing or non-finite source data")
    if np.sum(arr[:, 0] < 0) < 5 or np.sum(arr[:, 0] > 0) < 20:
        raise ValueError("Insufficient pre-pump/post-pump observations")
    return arr


def audit(arr: np.ndarray, sha256: str) -> dict:
    t = arr[:, 0]
    pre = (t < 0) & (t >= -4)
    early = (t >= 1) & (t <= 10)
    late = (t >= 100) & (t <= 200)
    if min(pre.sum(), early.sum(), late.sum()) < 5:
        raise ValueError("Missing baseline, early or late time range")
    cols = []
    for i in range(6):
        y = arr[:, i + 1]
        mean = float(np.mean(y[pre]))
        sd = float(np.std(y[pre], ddof=1))
        corr = y - mean
        post = t >= 0
        idx = np.flatnonzero(post)[np.argmax(np.abs(corr[post]))]
        cols.append({
            "index_1based": i + 1,
            "source_header": GROUPS[i // 3],
            "spectral_window": TIME_WINDOWS[i % 3],
            "baseline_mean_percent": mean,
            "baseline_std_percent": sd,
            "early_mean_corrected_percent": float(np.mean(corr[early])),
            "late_mean_corrected_percent": float(np.mean(corr[late])),
            "peak_abs_corrected_percent": float(np.abs(corr[idx])),
            "peak_time_ps": float(t[idx]),
        })
    return {
        "dataset_doi": DATASET_DOI,
        "paper_doi": PAPER_DOI,
        "sample_type": "nonchiral_layered_perovskite",
        "material": DATASET_MATERIAL,
        "raw_sha256": sha256,
        "time_unit": "ps",
        "signal_unit": "percent_delta_T_over_T",
        "n_time_points": int(len(t)),
        "time_range_ps": [float(t.min()), float(t.max())],
        "pre_pump_count": int(np.sum(t < 0)),
        "valid_source_labels": ["||", "X"],
        "channel_assignment": "NOT independently verified as co/counter-circular from file header; source filename includes Co_Cnt",
        "scientific_limit": "Nonchiral reference material; measured channel amplitudes and temporal windows are descriptive.",
        "channels": cols,
    }


def plot(arr: np.ndarray, destination: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    t = arr[:, 0]
    fit = (t >= 0.1) & (t <= 1000)
    fig, ax = plt.subplots(figsize=(9, 5))
    for i in range(6):
        y = arr[:, i + 1]
        baseline = float(np.mean(y[(t < 0) & (t >= -4)]))
        ax.plot(t[fit], (y-baseline)[fit],
                label=f"{GROUPS[i//3]} / {TIME_WINDOWS[i%3]}", lw=1.25)
    ax.set_xscale("log")
    ax.set_xlabel("Pump-probe delay (ps)")
    ax.set_ylabel("Baseline-corrected ΔT/T (%)")
    ax.set_title("Nonchiral BA2FAPb2I7: deposited polarization-resolved TA channels")
    ax.legend(fontsize=7, ncol=2)
    ax.grid(alpha=0.25)
    fig.text(0.01, 0.01, "Source: Cambridge DOI 10.17863/CAM.54010 | channel ||/X labels unverified | not R/S chirality data", fontsize=8)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    destination.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destination, dpi=180)
    plt.close(fig)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Data-level QA for an open nonchiral TA reference")
    ap.add_argument("command", choices=["fetch", "audit"])
    ap.add_argument("--raw", type=Path, default=Path("data/raw/kinetics/cambridge_54010") / RAW_FILENAME)
    ap.add_argument("--out", type=Path, default=Path("results/dynamics_cambridge_qa.json"))
    ap.add_argument("--fig", type=Path, default=Path("results/dynamics_cambridge_channels.png"))
    args = ap.parse_args(argv)
    manifest = fetch(args.raw) if args.command == "fetch" else {
        "sha256": hashlib.sha256(args.raw.read_bytes()).hexdigest()
    }
    if args.command == "fetch":
        print(json.dumps(manifest, indent=2))
    else:
        arr = parse(args.raw)
        result = audit(arr, manifest["sha256"])
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        plot(arr, args.fig)
        print(f"Audited {result['n_time_points']} delays across {len(result['channels'])} channels")
        print(f"Wrote {args.out} and {args.fig}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
