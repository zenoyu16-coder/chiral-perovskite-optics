from pathlib import Path
import numpy as np
import pytest

from chiral_perovskites.spin_led import (
    rows_tsv, numeric_pair, consistency_metrics, device_metrics, duplicate_numeric_tables
)


def test_ragged_multispectral_tsv_keeps_columns_aligned(tmp_path):
    f=tmp_path/"ragged.txt"
    f.write_text(
        "wavelength\tCDRMBA\tCDSMBA\twavelengthABS\tABSRMBA\tABSSMBA\twavelengthPL\n"
        "290\t1\t-1\t800\t0.1\t0.12\t450\n"
        "291\t2\t-2\t799\t0.2\t0.22\t451\n"
        "292\t3\t-3\t798\t0.3\t0.32\t452\n"
        "\t\t\t797\t0.4\t0.42\t453\n"
        "\t\t\t\t\t\t454\n",encoding="utf-8"
    )
    rows=rows_tsv(f)
    cdx,cd=numeric_pair(rows,"wavelength","CDRMBA")
    ax,ab=numeric_pair(rows,"wavelengthABS","ABSRMBA")
    assert len(cdx)==3 and len(ax)==4
    assert np.array_equal(cdx,[290,291,292])
    assert np.array_equal(ax,[800,799,798,797])
    assert np.array_equal(cd,[1,2,3])
    assert np.array_equal(ab,[.1,.2,.3,.4])


def test_synthetic_parity_metrics():
    rows=[]
    for i in range(5):
        rows.append({
            "wavelength":str(i+300),"CDRMBA":str(i+1),"CDSMBA":str(-(i+1)),
            "wavelengthABS":str(800-i),"ABSRMBA":str(i+2),"ABSSMBA":str(i+2),
        })
    metrics=consistency_metrics(rows)
    assert metrics["cd_points"]==5 and metrics["abs_points"]==5
    assert metrics["cd_R_S_pearson"]==pytest.approx(-1)
    assert metrics["abs_R_S_pearson"]==pytest.approx(1)
    assert metrics["cd_antisymmetry_residual_ratio"]==pytest.approx(0)
    assert metrics["abs_relative_l2_difference"]==pytest.approx(0)


def test_misaligned_wavelengths_rejected():
    rows=[{"wavelength":str(i+300),"CDRMBA":str(i+1),
           "CDSMBA":str(-(i+1)),"wavelengthABS":str(800-i),
           "ABSRMBA":str(i+2),"ABSSMBA":str(i+2)} for i in range(5)]
    rows[2]["wavelength"]="999"
    with pytest.raises(ValueError,match="CD wavelengths must ascend"):
        consistency_metrics(rows)


def test_device_sign_count_and_no_r_s_mapping():
    rows=[
        {"current1M":"1","polarization":"1.2","polarization1":"-2.2","error":"0.2","error1":"0.3"},
        {"current1M":"2","polarization":"-0.4","polarization1":"-0.8","error":"0.1","error1":"0.3"},
    ]
    report=device_metrics(rows)
    assert report["opposite_sign_rows"]==1
    assert report["n_current_rows"]==2
    assert "unidentified" in report["raw_channel_assignment"]


def test_exact_repeat_detection_ignores_delimiter_style(tmp_path):
    a,b=tmp_path/"a.txt",tmp_path/"b.txt"
    a.write_text("x\ty\n1\t2\n3\t4\n",encoding="utf-8")
    b.write_text("x y\n1 2\n3 4\n",encoding="utf-8")
    assert duplicate_numeric_tables(a,b)
    b.write_text("x y\n1 2\n3 5\n",encoding="utf-8")
    assert not duplicate_numeric_tables(a,b)
