import zipfile
from pathlib import Path

import numpy as np
import pytest

from chiral_perovskites.nature_sf_pilot import (
    _column_index, read_sheet, fig3c_arrays, fig3d_reference, peak_and_gate
)


def test_excel_column_indices():
    assert [_column_index(x) for x in ("A1","G40","Z2","AA9")] == [0,6,25,26]
    with pytest.raises(ValueError):
        _column_index("0")


def test_xlsx_reader_preserves_separated_source_columns(tmp_path):
    """A tiny workbook with skipped column D and two independent traces."""
    path = tmp_path / "test.xlsx"
    workbook = ('<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                '<sheets><sheet name="Fig. 3c" sheetId="1" r:id="rId1"/></sheets></workbook>')
    rels = ('<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
            'Target="worksheets/sheet1.xml"/></Relationships>')
    xml = ('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'
           '<row r="1"><c r="A1" t="inlineStr"><is><t>time (ps)</t></is></c>'
           '<c r="B1" t="inlineStr"><is><t>Intensity ( SMBA LCP)</t></is></c>'
           '<c r="C1" t="inlineStr"><is><t>Intensity (SMBA RCP)</t></is></c>'
           '<c r="E1" t="inlineStr"><is><t>time (ps)</t></is></c>'
           '<c r="F1" t="inlineStr"><is><t>Intensity (RMBA LCP)</t></is></c>'
           '<c r="G1" t="inlineStr"><is><t>Intensity (RMBA LCP)</t></is></c>'
           '</row><row r="2"><c r="A2"><v>1</v></c><c r="B2"><v>2</v></c>'
           '<c r="C2"><v>3</v></c><c r="E2"><v>1</v></c>'
           '<c r="F2"><v>4</v></c><c r="G2"><v>5</v></c></row>'
           '</sheetData></worksheet>')
    with zipfile.ZipFile(path,"w") as z:
        z.writestr("xl/workbook.xml",workbook)
        z.writestr("xl/_rels/workbook.xml.rels",rels)
        z.writestr("xl/worksheets/sheet1.xml",xml)
    rows=read_sheet(path,"Fig. 3c")
    assert rows[0][6]=="Intensity (RMBA LCP)"
    assert rows[1][0]==1
    assert 3 not in rows[1]
    assert rows[1][4]==1
    assert rows[1][6]==5


def test_time_trace_spectrum_gate_and_baseline():
    t = np.linspace(-60, 140, 501)
    burst = 8000 * np.exp(-0.5 * ((t-45)/18)**2)
    y = np.column_stack([25 + .56 * burst, 45 + .44 * burst])
    result = peak_and_gate(t,y)
    assert result["dcp0_baseline_corrected_fraction"] == pytest.approx(0.12,abs=1e-4)
    assert result["dcp0_raw_fraction"] < result["dcp0_baseline_corrected_fraction"]
    assert result["bright_gate_n_points"] > 20
    assert 44 < result["peak_time_ps"] < 46


def test_source_time_axis_must_match():
    headers={0:"time (ps)",1:"Intensity ( SMBA LCP)",2:"Intensity (SMBA RCP)",
             4:"time (ps)",5:"Intensity (RMBA LCP)",6:"Intensity (RMBA LCP)"}
    rows=[headers]
    for k in range(110):
        rows.append({0:float(k),1:100.,2:90.,4:float(k)+1.,5:90.,6:100.})
    with pytest.raises(ValueError, match="time axes"):
        fig3c_arrays(rows)


def test_duplicate_rmba_header_is_recorded_not_silently_assigned():
    headers={0:"time (ps)",1:"Intensity ( SMBA LCP)",2:"Intensity (SMBA RCP)",
             4:"time (ps)",5:"Intensity (RMBA LCP)",6:"Intensity (RMBA LCP)"}
    rows=[headers]
    for k in range(110):
        rows.append({0:float(k),1:110.,2:90.,4:float(k),5:80.,6:100.})
    t,s,r,meta=fig3c_arrays(rows)
    assert len(t)==110
    assert meta["rmba_second_header_duplicate"] is True
    assert r[0,1]==100


def test_fig3d_fluence_comparison_ignores_theory_columns():
    rows=[{}]
    for p,d1,d2 in ((290.,.135,-.137),(300.,.136,-.138),(310.,.139,-.142)):
        rows.append({0:p,1:d1,2:.001,3:"theory",
                     6:p,7:d2,8:.003,9:"theory"})
    refs=fig3d_reference(rows)
    assert refs["SMBA"]["fluence_uJ_cm2"] == 300
    assert refs["RMBA"]["dcp_fraction_from_fig3d"] == pytest.approx(-.138)
