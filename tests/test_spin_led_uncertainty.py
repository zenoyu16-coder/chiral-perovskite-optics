from chiral_perovskites.spin_led_uncertainty import (
    distinguish_sign, audit_sign_evidence
)


def test_multiplier_gate_zero_crossing():
    assert distinguish_sign(3.0, 1.0, 2.0)
    assert not distinguish_sign(1.0, 1.0, 1.0)
    assert not distinguish_sign(-0.4, 1.0, 2.0)


def test_count_is_not_all_6_significant():
    # Five raw opposite signs, but only one strong pair at twice the reported error.
    data = []
    rows = [
        (1, 4, -5, 1, 1),
        (2, 0.2, -5, 1, 1),
        (3, 2, -1, 1, 1),
        (4, -4, 4, 1, 1),
        (5, 3, -3, 2, 2),
        (6, 4, 5, 1, 1),
    ]
    for current, a, b, ea, eb in rows:
        data.append({
            "current1M": str(current),
            "polarization": str(a), "polarization1": str(b),
            "error": str(ea), "error1": str(eb)
        })
    report = audit_sign_evidence(data)
    assert report["n_rows"] == 6
    assert report["opposite_raw_sign_rows"] == 5
    assert report["both_signs_exclude_zero_at_1x_reported_error"] == 3
    assert report["both_signs_exclude_zero_at_2x_reported_error"] == 2
    assert "without defining statistical confidence" in report["interpretation_limit"]
