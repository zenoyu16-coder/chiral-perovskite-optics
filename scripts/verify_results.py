"""Check committed analysis artifacts against results/manifest.json."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
MANIFEST = RESULTS / "manifest.json"

EXPECTED = (
    "cd_front_back_audit.json",
    "cd_front_back_comparison.csv",
    "dynamics_cambridge_channels.png",
    "dynamics_cambridge_qa.json",
    "nature2026_fluence_control.png",
    "nature2026_fluence_control_audit.json",
    "nature2026_sf_fig3c_audit.json",
    "nature2026_sf_fig3c_reproduction.png",
    "nea_matched_298K.csv",
    "nea_matched_sensitivity.csv",
    "osf_chiral_cd_abs_pair.png",
    "osf_chiral_device_docp.png",
    "osf_chiral_optical_device_audit.json",
    "sensitivity_symprec_0p01.csv",
    "spin_led_uncertainty_gate.json",
    "temperature_summary.csv",
)


def inventory() -> dict:
    manifest = {}
    for name in EXPECTED:
        path = RESULTS / name
        if not path.is_file():
            raise FileNotFoundError(f"Missing expected analysis output: {path}")
        content = path.read_bytes()
        # Git stores CSV and JSON with LF line endings (see .gitattributes).
        # Hash the checked-in representation on both Windows and Linux.
        if path.suffix in {".json", ".csv"}:
            content = content.replace(b"\r\n", b"\n")
        manifest[name] = {
            "sha256": hashlib.sha256(content).hexdigest(),
            "bytes": len(content),
        }
    unexpected = sorted(
        p.name for p in RESULTS.iterdir()
        if p.is_file() and p.name not in EXPECTED and p.name != MANIFEST.name
    )
    if unexpected:
        raise ValueError(f"Unexpected result files: {unexpected}")
    return {
        "description": "SHA-256 fingerprints of published-data analyses",
        "files": manifest,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true",
                        help="Record current output fingerprints after an intentional rebuild")
    args = parser.parse_args(argv)

    current = inventory()
    if args.update:
        MANIFEST.write_text(
            json.dumps(current, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Recorded {len(current['files'])} results in {MANIFEST.relative_to(ROOT)}")
        return 0

    if not MANIFEST.is_file():
        raise FileNotFoundError("Missing results/manifest.json. Use --update to create it.")
    expected = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if expected != current:
        mismatches = [
            name for name in current["files"]
            if current["files"][name] != expected.get("files", {}).get(name)
        ]
        raise ValueError(f"Result fingerprints differ from manifest: {mismatches}")
    print(f"Verified {len(current['files'])} result files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
