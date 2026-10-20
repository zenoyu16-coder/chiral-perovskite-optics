"""Reproduce *one* chiral-superfluorescence result from Nature 2026 Source Data Fig. 3.

No new exciton, spin or superfluorescence kinetics model. Data are figure
source arrays, not independently acquired raw camera frames.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np

DOI = "10.1038/s41586-026-10637-x"
URL = (
    "https://media.springernature.com/original/springer-static/esm/"
    "art%3A10.1038%2Fs41586-026-10637-x/"
    "MediaObjects/41586_2026_10637_MOESM5_ESM.xlsx"
)
EXPECTED_SHA256 = "4f06825a839ba470e96fc45d9587db4d5f42067c41b2d03762e26ed64d217c29"
DEFAULT_FILE = Path("data/raw/kinetics/nature2026_source_fig3.xlsx")
XML = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
       "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def fetch(path: Path) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with urlopen(Request(URL, headers={"User-Agent": "chiral-pv-research/0.5"}), timeout=60) as response:
            payload = response.read()
        if not zipfile.is_zipfile(__import__("io").BytesIO(payload)):
            raise ValueError("Publisher response is not an XLSX workbook")
        path.write_bytes(payload)
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    if sha != EXPECTED_SHA256:
        raise ValueError(f"Source workbook hash changed: {sha}; re-audit before proceeding.")
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha, "doi": DOI, "source_url": URL}


def _column_index(cell_ref: str) -> int:
    match = re.match(r"([A-Z]+)[0-9]+$", cell_ref)
    if not match:
        raise ValueError(f"Bad XLSX cell reference: {cell_ref}")
    n = 0
    for char in match.group(1):
        n = n*26 + ord(char)-ord("A")+1
    return n-1


def read_sheet(path: Path, name: str) -> list[dict[int, str | float | None]]:
    """Small read-only OOXML reader preserving blank columns; no spreadsheet edits."""
    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        links = {r.get("Id"):r.get("Target") for r in rels}
        sheets = wb.findall("m:sheets/m:sheet", XML)
        matches = [s for s in sheets if s.get("name")==name]
        if len(matches)!=1:
            raise ValueError(f"Expected exactly one worksheet {name!r}.")
        rid = matches[0].get("{" + XML["r"] + "}id")
        target = links[rid].lstrip("/")
        internal = target if target.startswith("xl/") else "xl/"+target
        root = ET.fromstring(z.read(internal))
        strings = []
        if "xl/sharedStrings.xml" in z.namelist():
            sst = ET.fromstring(z.read("xl/sharedStrings.xml"))
            strings = ["".join(t.text or "" for t in node.findall(".//m:t", XML))
                       for node in sst.findall("m:si", XML)]
        rows = []
        for element in root.findall("m:sheetData/m:row", XML):
            row = {}
            for cell in element.findall("m:c", XML):
                idx = _column_index(cell.get("r", ""))
                typ = cell.get("t")
                val = cell.find("m:v", XML)
                if typ=="inlineStr":
                    inline=cell.find("m:is", XML)
                    parsed="".join(t.text or "" for t in inline.findall(".//m:t",XML))
                elif val is None: parsed=None
                elif typ=="s": parsed=strings[int(val.text)]
                elif typ in ("str","e"): parsed=val.text
                else:
                    try: parsed=float(val.text)
                    except (TypeError,ValueError): parsed=val.text
                row[idx] = parsed
            if row:
                rows.append(row)
        return rows


def _numeric(rows: list[dict], columns: tuple[int,...], min_rows: int = 100) -> np.ndarray:
    records = []
    for r in rows[1:]:
        if any(r.get(j) is None for j in columns):
            continue
        vals = [r[j] for j in columns]
        if any(not isinstance(v,(int,float)) for v in vals):
            raise ValueError(f"Non-numeric data in source columns {columns}")
        records.append(vals)
    a = np.asarray(records, dtype=float)
    if a.ndim != 2 or a.shape[0] < min_rows or not np.isfinite(a).all():
        raise ValueError("Insufficient valid finite worksheet data")
    return a


def fig3c_arrays(rows: list[dict]) -> tuple[np.ndarray,np.ndarray,np.ndarray,dict]:
    heads = rows[0]
    if heads.get(0)!="time (ps)" or heads.get(4)!="time (ps)":
        raise ValueError("Fig. 3c time headers not as expected")
    if "SMBA LCP" not in heads.get(1,"") or "SMBA RCP" not in heads.get(2,""):
        raise ValueError("SMBA LCP/RCP source labels changed")
    if "RMBA LCP" not in heads.get(5,""):
        raise ValueError("RMBA first channel label changed")
    a = _numeric(rows,(0,1,2,4,5,6))
    t=a[:,0]
    if np.max(abs(t-a[:,3]))>1e-4 or np.any(np.diff(t)<=0):
        raise ValueError("R/S time axes do not match or are not increasing")
    return (t, a[:,1:3], a[:,4:6],
            {"smba": [heads.get(1),heads.get(2)],
             "rmba": [heads.get(5),heads.get(6)],
             "rmba_second_header_duplicate": heads.get(5)==heads.get(6)})


def fig3d_reference(rows: list[dict], near_fluence: float = 300.0) -> dict:
    """Experimental source points only; theory columns are deliberately ignored."""
    s=_numeric(rows,(0,1,2),min_rows=3)
    r=_numeric(rows,(6,7,8),min_rows=3)
    si=int(np.argmin(abs(s[:,0]-near_fluence)))
    ri=int(np.argmin(abs(r[:,0]-near_fluence)))
    if abs(s[si,0]-near_fluence)>20 or abs(r[ri,0]-near_fluence)>20:
        raise ValueError("Missing matched Fig. 3d fluence point near 300")
    return {"SMBA": {"fluence_uJ_cm2": float(s[si,0]),
                       "dcp_fraction_from_fig3d":float(s[si,1]),
                       "deposited_error":float(s[si,2])},
            "RMBA": {"fluence_uJ_cm2": float(r[ri,0]),
                       "dcp_fraction_from_fig3d":float(r[ri,1]),
                       "deposited_error":float(r[ri,2])}}


def peak_and_gate(t: np.ndarray, y: np.ndarray, baseline_window=(-60.,-40.),
                  bright_fraction=0.20) -> dict:
    if len(t)!=len(y) or y.ndim!=2 or y.shape[1]!=2:
        raise ValueError("Expect matched time axis and two emission channels")
    baseline_mask=(t>=baseline_window[0])&(t<baseline_window[1])
    if baseline_mask.sum()<10:
        raise ValueError("Insufficient pre-burst baseline samples")
    base=np.mean(y[baseline_mask],axis=0)
    corrected=y-base
    total=corrected.sum(axis=1)
    idx=int(np.argmax(total))
    if total[idx]<=0:
        raise ValueError("No positive emission peak")
    dcp=(
        float((corrected[idx,0]-corrected[idx,1])/total[idx])
    )
    raw_total=y.sum(axis=1)
    raw_peak=int(np.argmax(raw_total))
    dcp_raw=float((y[raw_peak,0]-y[raw_peak,1])/raw_total[raw_peak])
    good=(t>=0)&(total>=bright_fraction*total[idx])&(corrected[:,0]>0)&(corrected[:,1]>0)
    if good.sum()<10:
        raise ValueError("Too few high-signal points for a descriptive comparison")
    contrasts=(corrected[good,0]-corrected[good,1])/total[good]
    return {
        "n_samples":int(len(t)),
        "time_min_ps":float(t.min()), "time_max_ps":float(t.max()),
        "median_sampling_step_ps":float(np.median(np.diff(t))),
        "peak_time_ps":float(t[idx]),
        "peak_total_baseline_corrected":float(total[idx]),
        "dcp0_raw_fraction":dcp_raw,
        "dcp0_baseline_corrected_fraction":dcp,
        "baseline_window_ps":list(baseline_window),
        "baseline_channel_means":base.tolist(),
        "bright_gate_fraction_of_peak":bright_fraction,
        "bright_gate_n_points":int(good.sum()),
        "bright_gate_time_range_ps":[float(t[good].min()),float(t[good].max())],
        "bright_gate_median_dcp_fraction":float(np.median(contrasts)),
    }


def plot_one_reproduction(t:np.ndarray, s:np.ndarray, r:np.ndarray,
                          out:Path,bright_fraction:float=.2)->None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2,2,figsize=(11.6,7.7),sharex="col")
    for i,(name,y) in enumerate((("SMBA",s),("RMBA",r))):
        base=y[(t>=-60)&(t<-40)].mean(axis=0)
        corrected=y-base
        tot=corrected.sum(axis=1)
        valid=(t>=0)&(tot>=bright_fraction*tot.max())&(corrected>0).all(axis=1)
        contrast=(corrected[valid,0]-corrected[valid,1])/tot[valid]
        time_range=(t>=0)&(t<=120)
        axes=axs[:,i]
        axes[0].plot(t[time_range],corrected[time_range,0],label="LCP / channel 1")
        axes[0].plot(t[time_range],corrected[time_range,1],
                     label="RCP" if name=="SMBA" else "RMBA channel 2*")
        axes[0].set_title(name+" time-resolved PL")
        axes[0].set_ylabel("Intensity (source a.u.; baseline-corrected)")
        axes[0].legend(fontsize=8)
        axes[1].plot(t[valid],100*contrast)
        axes[1].axhline(0,lw=.7,color="gray")
        axes[1].set_xlim(0,120)
        axes[1].set_ylim(-25,25)
        axes[1].set_xlabel("Delay (ps)")
        axes[1].set_ylabel("Bright-signal channel contrast (%)")
        axes[1].grid(alpha=.2)
    fig.suptitle("Source Data Fig. 3c / reproduced chiral SF polarization — no kinetic fit", fontsize=13, y=.98)
    fig.text(.02,.040,"Wei et al., Nature 654, 369–374 (2026) | DOI 10.1038/s41586-026-10637-x | 300 µJ/cm²",fontsize=8)
    fig.text(.02,.019,"*RMBA column 2 repeats 'LCP' in publisher XLSX; provisionally opposite-helicity. "
             "Temporal resolution ~10 ps (source spacing 0.35 ps).",fontsize=8)
    fig.tight_layout(rect=(0,.073,1,.955), h_pad=1.8, w_pad=2.5)
    out.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(out,dpi=170)
    plt.close(fig)


def analyze(source:Path, report:Path, plot:Path) -> dict:
    src=fetch(source)
    t,s,r,headers=fig3c_arrays(read_sheet(source,"Fig. 3c"))
    refs=fig3d_reference(read_sheet(source,"Fig. 3d"))
    baseline_windows=[(-60.,-50.),(-60.,-40.),(-60.,-30.),(-60.,-20.)]
    samples={}
    for label,y in (("SMBA",s),("RMBA",r)):
        main=peak_and_gate(t,y)
        changes=[peak_and_gate(t,y,win)["dcp0_baseline_corrected_fraction"] for win in baseline_windows]
        main["baseline_sensitivity_dcp0_fraction"]={
            "min":float(min(changes)),"max":float(max(changes)),
            "n_windows":len(changes),
        }
        ref=refs[label]
        difference=main["dcp0_raw_fraction"]-ref["dcp_fraction_from_fig3d"]
        main["fig3d_reference"]=ref
        main["raw_dcp0_minus_fig3d_fraction"]=float(difference)
        if abs(difference)>.005:
            raise ValueError(f"{label} Fig.3c DCP0 deviates >0.5 percentage points from Fig.3d")
        samples[label]=main
    if np.sign(samples["SMBA"]["dcp0_raw_fraction"])==np.sign(samples["RMBA"]["dcp0_raw_fraction"]):
        raise ValueError("Expected R/S sign reversal not reproduced")
    ans={
        "paper_doi":DOI,"source":src,"publisher_workbook_sheets":["Fig. 3b","Fig. 3c","Fig. 3d"],
        "fig3c_source_headers":headers,
        "pump_condition":"550 nm linear polarization; 300 microjoules per cm^2",
        "source_kind":"publication Source Data XLSX (digitized/processed figure arrays)",
        "publisher_temporal_resolution_ps_approx":10,
        "warnings":[
            "Fig. 3c RMBA second-channel header repeats LCP; paper Fig. 3b and Fig. 3d indicate opposite-helicity channel, but no author correction verified.",
            "0.3495 ps numerical delay spacing is not independent ~10 ps camera resolution.",
            "No independent acquisition replicates or R/S sample-matched calibration/IRF files here.",
            "Bright-gate contrast vs time is descriptive; not a spin or exciton polarization lifetime.",
            "Cannot infer new collective emission mechanism from the author's already published reproduction.",
        ],
        "samples":samples,
        "decision":"GO for one-figure reproducible observation; STOP before microscopic model without independent condition/replicate evidence",
    }
    plot_one_reproduction(t,s,r,plot)
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(ans,indent=2,ensure_ascii=False),encoding="utf-8")
    return ans


def main(argv=None)->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("command",choices=["fetch","analyze"])
    ap.add_argument("--source",type=Path,default=DEFAULT_FILE)
    ap.add_argument("--out",type=Path,default=Path("results/nature2026_sf_fig3c_audit.json"))
    ap.add_argument("--fig",type=Path,default=Path("results/nature2026_sf_fig3c_reproduction.png"))
    args=ap.parse_args(argv)
    if args.command=="fetch":
        print(json.dumps(fetch(args.source),indent=2))
        return 0
    result=analyze(args.source,args.out,args.fig)
    for h,record in result["samples"].items():
        print(f"{h}: raw DCP0={100*record['dcp0_raw_fraction']:+.4f}%, "
              f"baseline corrected={100*record['dcp0_baseline_corrected_fraction']:+.4f}%, "
              f"paper Fig3d={100*record['fig3d_reference']['dcp_fraction_from_fig3d']:+.4f}%")
    print(f"Output: {args.out} and {args.fig}")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
