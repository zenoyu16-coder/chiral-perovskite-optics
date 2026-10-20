import hashlib
import io
import zipfile

import numpy as np
import pytest

from chiral_perovskites.fluence_response import positive_pair, dcp_exclusion_points
from chiral_perovskites.fluence_sources import validate_xlsx


def test_intensity_source_parser_selects_only_paired_numeric_rows():
    rows=[{1:"Pump Fluence",2:"Intensity"},
          {1:20.0,2:4.0},{1:30.0,2:9.0},{1:40.0,2:18.0},
          {1:50.0,2:33.0},{1:80.0,2:100.0},
          {4:20.0,5:90.0}]
    a=positive_pair(rows,1,2)
    assert a.shape==(5,2)
    assert np.array_equal(a[:,0],[20,30,40,50,80])


def test_source_parser_rejects_out_of_order_and_nonpositive():
    data=[{1:float(x),2:float(10*x)} for x in (10,20,30,40,50)]
    data[-1][1]=35
    with pytest.raises(ValueError,match="increasing"):
        positive_pair(data,1,2)
    data[-1][1]=50
    data[2][2]=-1
    with pytest.raises(ValueError,match="positive"):
        positive_pair(data,1,2)


def test_double_propagated_error_threshold_is_arithmetic_only():
    data=[{0:x,1:v,2:e} for x,v,e in [
        (20,.001,.02),(40,.02,.02),(60,.04,.03),(80,.1,.03),(100,.13,.005)]]
    result=dcp_exclusion_points(data,(0,1,2))
    assert [p["interval_avoids_zero"] for p in result]==[False,False,False,True,True]


def test_xlsx_source_checksum_and_workbook_structure():
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,"w") as z:
        z.writestr("xl/workbook.xml","<workbook/>")
    content=buf.getvalue()
    validate_xlsx(content,hashlib.sha256(content).hexdigest())
    with pytest.raises(ValueError,match="checksum mismatch"):
        validate_xlsx(content,"0"*64)
    html=b"<!DOCTYPE html><body>Access restricted</body>"
    with pytest.raises(ValueError,match="instead of Excel"):
        validate_xlsx(html,hashlib.sha256(html).hexdigest())
