"""Stage 2: reproducible R/S/rac structure analysis and independent CD archive audit."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .data import fetch_sources
from .nea import analyze_matched, relative_scalar_differences
from .optics import audit_cd, fetch_optics


def save_csv(destination: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError("No rows to write")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["matched-fetch", "matched-analyze", "optical-fetch", "optical-audit"])
    parser.add_argument("--manifest", type=Path, default=Path("data/nea_sources.csv"))
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--out", type=Path)
    parser.add_argument("--symprec", type=float, default=0.05)
    parser.add_argument("--cutoff", type=float, default=3.7)
    args = parser.parse_args(argv)
    if args.symprec <= 0 or args.cutoff <= 0:
        parser.error("symprec and cutoff must be positive")
    if args.command == "matched-fetch":
        print(json.dumps(fetch_sources(args.manifest, args.data_dir), indent=2))
    elif args.command == "matched-analyze":
        records = analyze_matched(args.manifest, args.data_dir, args.symprec, args.cutoff)
        output = args.out or Path("results/nea_matched_298K.csv")
        save_csv(output, records)
        for r in records:
            print(f"{r['hand']:>3}: SG={r['symmetry_space_group']:9s}, "
                  f"Pb-Br={r['pb_x_mean_A']:.4f} A, cis-var={r['cis_angle_variance_deg2']:.3f} deg^2")
        print("R-S fractional scalar differences (%):", relative_scalar_differences(records))
        print("Written", output)
    elif args.command == "optical-fetch":
        print(json.dumps(fetch_optics(args.data_dir), indent=2))
    else:
        details, points = audit_cd(args.data_dir)
        summary = args.out or Path("results/cd_front_back_audit.json")
        summary.parent.mkdir(parents=True, exist_ok=True)
        summary.write_text(json.dumps(details, indent=2), encoding="utf-8")
        save_csv(Path("results/cd_front_back_comparison.csv"), points)
        print(json.dumps(details, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
