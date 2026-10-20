"""Front/back circular-dichroism data from S-NEA2PbBr4 thin films."""
from __future__ import annotations

import hashlib
import io
from pathlib import Path
from urllib.request import urlopen, Request
from zipfile import ZipFile

import numpy as np

CD_DATASET = "2784"
ABS_DATASET = "2785"
DOI = "10.1002/adma.202415901"
DATASETS = {
    CD_DATASET: ("data1.txt", "data2.txt", "data3.txt", "info.txt"),
    ABS_DATASET: ("data.txt", "info.txt"),
}


def fetch_optics(raw_dir: Path) -> list[dict]:
    """Download known, named files from original Duke archives; don't blindly extract ZIP."""
    entries = []
    for dataset, files in DATASETS.items():
        dest = raw_dir / "optical" / dataset
        dest.mkdir(parents=True, exist_ok=True)
        missing = [name for name in files if not (dest / name).exists()]
        if missing:
            uri = f"https://materials.hybrid3.duke.edu/materials/datasets/{dataset}/files/"
            with urlopen(Request(uri, headers={"User-Agent":"chiral-pv/0.2"}), timeout=45) as response:
                archive = ZipFile(io.BytesIO(response.read()))
            with archive:
                for name in missing:
                    matches = [member for member in archive.namelist()
                               if Path(member).name == name and not member.endswith("/")]
                    if len(matches) != 1:
                        raise ValueError(f"{dataset}: missing/duplicated {name}")
                    (dest / name).write_bytes(archive.read(matches[0]))
        entries.extend({"dataset": dataset, "filename": name,
                        "sha256": hashlib.sha256((dest / name).read_bytes()).hexdigest()}
                       for name in files)
    return entries


def compare_front_back(front: np.ndarray, back: np.ndarray, deposited: np.ndarray) -> tuple[dict, list[dict]]:
    for array in (front, back, deposited):
        if array.ndim != 2 or array.shape[1] != 2 or not np.isfinite(array).all():
            raise ValueError("Each spectrum must contain finite wavelength/signal columns")
    if len(front) != len(back) or len(front) != len(deposited):
        raise ValueError("CD spectra row counts differ")
    wavelength = front[:, 0]
    if (np.diff(wavelength) <= 0).any() or not np.allclose(wavelength, back[:, 0], atol=1e-8) or not np.allclose(wavelength, deposited[:, 0], atol=1e-8):
        raise ValueError("Wavelength grids differ")
    raw_sum = front[:, 1] + back[:, 1]
    arithmetic_mean = raw_sum / 2.0
    from_sum = deposited[:, 1] - raw_sum
    from_mean = deposited[:, 1] - arithmetic_mean
    details = {
        "source_doi": DOI,
        "dataset_id": CD_DATASET,
        "sample_type": "thin_film",
        "data_labels": ["front", "back", "average (as deposited)"],
        "rows": int(len(wavelength)),
        "wavelength_min_nm": float(wavelength.min()),
        "wavelength_max_nm": float(wavelength.max()),
        "max_abs_deposited_minus_sum_mdeg": float(np.abs(from_sum).max()),
        "max_abs_deposited_minus_mean_mdeg": float(np.abs(from_mean).max()),
        "rmse_deposited_minus_sum_mdeg": float(np.sqrt(np.mean(from_sum ** 2))),
        "rmse_deposited_minus_mean_mdeg": float(np.sqrt(np.mean(from_mean ** 2))),
        "note": "The archived combined curve agrees with front+back within rounding; the original normalization convention is unspecified.",
    }
    data = [
        {"wavelength_nm":float(w), "cd_front_mdeg":float(f), "cd_back_mdeg":float(b),
         "cd_deposited_average_mdeg":float(p), "cd_arithmetic_mean_mdeg":float(m)}
        for w,f,b,p,m in zip(wavelength,front[:,1],back[:,1],deposited[:,1],arithmetic_mean)
    ]
    return details,data


def audit_cd(raw_dir: Path) -> tuple[dict, list[dict]]:
    base = raw_dir / "optical" / CD_DATASET
    spectra = [np.loadtxt(base / f"data{i}.txt") for i in (1,2,3)]
    return compare_front_back(*spectra)
