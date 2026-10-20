"""Temperature-dependent S-MBA2PbI4 crystal structure analysis."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .analysis import analyze_sources
from .data import fetch_sources


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="S-MBA2PbI4 crystallographic temperature series")
    parser.add_argument("command", choices=["fetch", "analyze"])
    parser.add_argument("--manifest", type=Path, default=Path("data/sources.csv"))
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--out", type=Path, default=Path("results/temperature_summary.csv"))
    parser.add_argument("--symprec", type=float, default=0.05)
    parser.add_argument("--cutoff", type=float, default=3.7, help="Pb-I cutoff in Angstrom")
    parser.add_argument("--overwrite", action="store_true", help="Re-download source CIFs")
    args = parser.parse_args(argv)
    if args.symprec <= 0 or args.cutoff <= 0:
        parser.error("symprec and cutoff must be > 0")
    if args.command == "fetch":
        print(json.dumps(fetch_sources(args.manifest, args.data_dir, args.overwrite), indent=2))
        return 0
    rows = analyze_sources(args.manifest, args.data_dir, args.symprec, args.cutoff)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        print(f"{row['temperature_K']} K | {row['space_group']} | "
              f"V/Pb={row['volume_per_Pb_A3']:.2f} A^3 | "
              f"Pb-I={row.get('pb_i_mean_A', float('nan')):.3f} A | "
              f"skipped Pb={row['pb_sites_skipped']}")
    print(f"Wrote: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
