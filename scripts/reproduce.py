"""Download published inputs and regenerate the repository's result files."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DOWNLOADS = [
    ("mba_temperature", ["fetch"]),
    ("nea_analysis", ["matched-fetch"]),
    ("nea_analysis", ["optical-fetch"]),
    ("transient_absorption", ["fetch"]),
    ("spin_led", ["fetch"]),
    ("polarized_pl", ["fetch"]),
    ("fluence_response", ["--fetch"]),
]

ANALYSES = [
    ("mba_temperature", ["analyze"]),
    ("mba_temperature", ["analyze", "--symprec", "0.01",
                         "--out", "results/sensitivity_symprec_0p01.csv"]),
    ("nea_analysis", ["matched-analyze"]),
    ("nea_analysis", ["matched-analyze", "--symprec", "0.01",
                      "--cutoff", "3.6", "--out", "results/nea_matched_sensitivity.csv"]),
    ("nea_analysis", ["optical-audit"]),
    ("transient_absorption", ["audit"]),
    ("spin_led", ["analyze"]),
    ("spin_led_uncertainty", []),
    ("polarized_pl", ["analyze"]),
    ("fluence_response", []),
]


def run(module: str, arguments: list[str]) -> None:
    command = [sys.executable, "-m", "chiral_perovskites." + module, *arguments]
    print("$", " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Regenerate published-data analyses")
    parser.add_argument("--fetch", action="store_true",
                        help="Download original source files before analysis")
    args = parser.parse_args(argv)

    if args.fetch:
        for module, parameters in DOWNLOADS:
            run(module, parameters)
    for module, parameters in ANALYSES:
        run(module, parameters)
    print("Result generation completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
