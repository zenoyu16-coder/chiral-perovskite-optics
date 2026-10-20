import numpy as np
import pytest
from pymatgen.core import Lattice, Structure

from chiral_perovskites.analysis import describe_cif, octahedral_geometry, pb_i_octahedra


def test_perfect_octahedron():
    d = 3.1
    vectors = np.array([[d, 0, 0], [-d, 0, 0],
                        [0, d, 0], [0, -d, 0],
                        [0, 0, d], [0, 0, -d]])
    result = octahedral_geometry(vectors)
    assert result["pb_i_mean_A"] == pytest.approx(d)
    assert result["pb_i_bond_distortion"] == pytest.approx(0, abs=1e-14)
    assert result["cis_angle_variance_deg2"] == pytest.approx(0, abs=1e-12)
    assert result["trans_angle_mean_deg"] == pytest.approx(180)


def test_octahedral_geometry_requires_six_bonds():
    with pytest.raises(ValueError):
        octahedral_geometry(np.ones((5, 3)))


def test_neighbor_geometry_on_synthetic_structure(tmp_path):
    d = 3.1
    origin = np.array([6, 6, 6])
    delta = np.array([[d, 0, 0], [-d, 0, 0],
                      [0, d, 0], [0, -d, 0],
                      [0, 0, d], [0, 0, -d]])
    coords = np.vstack([origin, origin + delta])
    s = Structure(Lattice.cubic(12), ["Pb"] + ["I"] * 6, coords, coords_are_cartesian=True)
    metrics, skipped = pb_i_octahedra(s)
    assert skipped == 0
    assert metrics["pb_i_mean_A"] == pytest.approx(d)
    assert metrics["cis_angle_variance_deg2"] == pytest.approx(0, abs=1e-10)
    path = tmp_path / "synthetic.cif"
    s.to(filename=str(path))
    description = describe_cif(path)
    assert description["pb_sites"] == 1
    assert description["pb_sites_skipped"] == 0
