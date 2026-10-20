from pathlib import Path

import numpy as np
import pytest

from chiral_perovskites.transient_absorption import parse, audit


def make_data(path: Path, header="\t||\t||\t||\tX\tX\tX") -> None:
    times = np.r_[np.linspace(-4, -0.2, 12), np.arange(0, 20, 1), np.linspace(20.5, 300, 65)]
    with path.open("w", encoding="utf-8") as stream:
        stream.write("Time\t\\g(D)T/T\nps\t%\n" + header + "\n")
        for t in times:
            ys = [float((i + 1) * np.exp(-max(0, t) / 60)) for i in range(6)]
            stream.write("\t".join([str(t), *(str(v) for v in ys)]) + "\n")


def test_parse_and_audit(tmp_path):
    raw = tmp_path / "example.txt"
    make_data(raw)
    arr = parse(raw)
    result = audit(arr, "test-hash")
    assert result["n_time_points"] == 97
    assert len(result["channels"]) == 6
    assert result["sample_type"] == "nonchiral_layered_perovskite"
    assert result["channels"][0]["spectral_window"] == "552-557 nm"


def test_reject_inconsistent_header(tmp_path):
    raw = tmp_path / "bad.txt"
    make_data(raw, header="\tR\tR\tR\tS\tS\tS")
    with pytest.raises(ValueError, match="channel labels"):
        parse(raw)


def test_reject_non_monotonic_times(tmp_path):
    raw = tmp_path / "badtime.txt"
    make_data(raw)
    lines = raw.read_text().splitlines()
    lines[-1] = lines[-2]
    raw.write_text("\n".join(lines) + "\n")
    with pytest.raises(ValueError, match="increasing"):
        parse(raw)
