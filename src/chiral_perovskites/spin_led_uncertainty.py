"""Source-data error-bar comparison for circularly polarized electroluminescence."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .spin_led import rows_tsv, device_metrics

DEFAULT_SOURCE = Path("data/raw/osf_2m35k/Fig_2c_current_vs_DOCP.txt")
DEFAULT_OUTPUT = Path("results/spin_led_uncertainty_gate.json")


def distinguish_sign(value: float, reported_error: float, multiplier: float) -> bool:
    """Whether [value ± multiplier * quoted_error] excludes zero."""
    if reported_error < 0 or multiplier < 0:
        raise ValueError("Error and multiplier must be nonnegative.")
    return abs(value) > multiplier * reported_error


def audit_sign_evidence(rows: list[dict]) -> dict:
    source = device_metrics(rows)
    details = []
    for row in source["rows"]:
        a, b = row["channel_A"], row["channel_B"]
        ea, eb = row["reported_error_A"], row["reported_error_B"]
        entry = {
            "current_source_units_unverified": row["current_from_column_1"],
            "series_A": a,
            "series_B": b,
            "error_A_raw": ea,
            "error_B_raw": eb,
            "opposite_raw_signs": bool(a * b < 0),
        }
        for multiplier in (1, 2):
            entry[f"A_sign_survives_{multiplier}x_error"] = distinguish_sign(a, ea, multiplier)
            entry[f"B_sign_survives_{multiplier}x_error"] = distinguish_sign(b, eb, multiplier)
            entry[f"both_signs_survive_{multiplier}x_error"] = (
                entry[f"A_sign_survives_{multiplier}x_error"]
                and entry[f"B_sign_survives_{multiplier}x_error"]
                and entry["opposite_raw_signs"]
            )
        details.append(entry)
    return {
        "source_figure": "Fig. 2c of Hautzinger et al. Nature 631, 307–312 (2024)",
        "source_doi": "10.17605/OSF.IO/2M35K",
        "n_rows": len(details),
        "opposite_raw_sign_rows": sum(row["opposite_raw_signs"] for row in details),
        "both_signs_exclude_zero_at_1x_reported_error": sum(
            row["both_signs_survive_1x_error"] for row in details
        ),
        "both_signs_exclude_zero_at_2x_reported_error": sum(
            row["both_signs_survive_2x_error"] for row in details
        ),
        "interpretation_limit": (
            "Source-error multipliers provide an arithmetic sign-sensitivity "
            "comparison, without defining statistical confidence or independent device "
            "replication; the source error-bar definition is unspecified."
        ),
        "identity_limit": (
            "Source TSV has columns polarization/polarization1 without enantiomer labels. "
            "The accessible arXiv manuscript 2309.04559 contains an apparent inconsistency "
            "between equation/panel labels and the handedness-sign prose near Fig. 2. "
            "The R/S mapping requires confirmation from the published version."
        ),
        "samples_limit": (
            "These are repeated current measurements of specific devices, not six "
            "independent fabricated samples; wavelength points are not replicates."
        ),
        "rows": details,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check reported error-bar sensitivity; no model fitting")
    ap.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUTPUT)
    args = ap.parse_args(argv)
    result = audit_sign_evidence(rows_tsv(args.source))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Opposite raw signs: {result['opposite_raw_sign_rows']}/{result['n_rows']}")
    print(f"Both intervals exclude zero (1 x error): "
          f"{result['both_signs_exclude_zero_at_1x_reported_error']}/{result['n_rows']}")
    print(f"Both intervals exclude zero (2 x error): "
          f"{result['both_signs_exclude_zero_at_2x_reported_error']}/{result['n_rows']}")


if __name__ == "__main__":
    main()
