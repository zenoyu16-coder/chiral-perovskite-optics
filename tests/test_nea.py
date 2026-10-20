import numpy as np
import pytest
from pymatgen.core import Lattice, Structure

from chiral_perovskites.nea import pb_halide_metrics, relative_scalar_differences
from chiral_perovskites.optics import compare_front_back


def test_bromide_octahedron():
    d = 3.0
    delta = np.eye(3) * d
    cart = np.vstack([np.array([10,10,10]), np.array([10,10,10])+delta, np.array([10,10,10])-delta])
    s = Structure(Lattice.cubic(20), ["Pb"]+["Br"]*6, cart, coords_are_cartesian=True)
    metrics = pb_halide_metrics(s)
    assert metrics["pb_x_mean_A"] == pytest.approx(3.0)
    assert metrics["cis_angle_variance_deg2"] == pytest.approx(0.0,abs=1e-10)


def test_signed_local_halide_centroid_reverses_under_mirror():
    center = np.array([10.0,10.0,10.0])
    d = 3.0
    oct_dirs = np.vstack([np.eye(3)*d, -np.eye(3)*d])
    for sign in (+1, -1):
        coords = np.vstack([center, center + oct_dirs + [0, sign * 0.04, 0]])
        structure = Structure(Lattice.cubic(20), ["Pb"]+["Br"]*6, coords, coords_are_cartesian=True)
        result = pb_halide_metrics(structure)
        assert result["halide_centroid_minus_pb_b_A"] == pytest.approx(sign * 0.04)


def test_incomplete_pbbr6_errors():
    s = Structure(Lattice.cubic(20), ["Pb", "Br"], [[0.5,0.5,0.5],[0.65,0.5,0.5]])
    with pytest.raises(ValueError, match="expected 6"):
        pb_halide_metrics(s)


def test_relative_scalar_difference():
    names = ("volume_per_Pb_A3","pb_x_mean_A","pb_x_bond_distortion","cis_angle_variance_deg2")
    pair = [{"hand": h, **{name:v for name in names}} for h,v in (("S",10.0),("R",11.0))]
    differences = relative_scalar_differences(pair)
    assert differences["volume_per_Pb_A3"] == pytest.approx(100/10.5)


def test_cd_audit_reports_sum_not_mean():
    wl = [300,301,302]
    a = np.column_stack([wl,[4,6,8]])
    b = np.column_stack([wl,[2,4,10]])
    c = np.column_stack([wl,[6,10,18]])
    details, data = compare_front_back(a,b,c)
    assert details["max_abs_deposited_minus_sum_mdeg"] == 0
    assert details["max_abs_deposited_minus_mean_mdeg"] == 9
    assert data[0]["cd_arithmetic_mean_mdeg"] == 3


def test_cd_audit_rejects_mismatched_grid():
    a = np.array([[300.,2.],[301.,3.]])
    b = np.array([[301.,2.],[302.,3.]])
    with pytest.raises(ValueError, match="Wavelength"):
        compare_front_back(a,b,a)
