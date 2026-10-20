"""Download only specified CIF entries; no untrusted ZIP extraction."""
from __future__ import annotations

import csv
import hashlib
import io
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile


def read_sources(manifest: Path) -> list[dict[str, str]]:
    with manifest.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    required = {"id", "sample", "temperature_K", "doi", "dataset_url", "cif_name"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"Invalid source manifest: {manifest}")
    return rows


def fetch_sources(manifest: Path, data_dir: Path, overwrite: bool = False) -> list[dict]:
    data_dir.mkdir(parents=True, exist_ok=True)
    fetched = []
    for row in read_sources(manifest):
        destination = data_dir / row["cif_name"]
        if Path(row["cif_name"]).name != row["cif_name"]:
            raise ValueError("Manifest CIF filenames must be basenames.")
        if not destination.exists() or overwrite:
            request = Request(row["dataset_url"], headers={"User-Agent": "chiral-perovskite-research/0.1"})
            with urlopen(request, timeout=45) as response:
                archive = response.read()
            with ZipFile(io.BytesIO(archive)) as bundle:
                candidates = [n for n in bundle.namelist()
                              if Path(n).name == row["cif_name"] and not n.endswith("/")]
                if len(candidates) != 1:
                    raise ValueError(f"Expected exactly one {row['cif_name']} in source ZIP")
                payload = bundle.read(candidates[0])
            if not payload.lstrip().startswith(b"data_"):
                raise ValueError(f"Downloaded entry does not begin with CIF data_: {destination}")
            destination.write_bytes(payload)
        fetched.append({
            "id": row["id"],
            "path": str(destination),
            "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
            "bytes": destination.stat().st_size,
        })
    return fetched
