"""Pump-fluence dependence of PL and circular polarization in perovskite superlattices."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from .polarized_pl import read_sheet
from .fluence_sources import fetch as fetch_sources

SOURCE_FILES = {
    "SMBA": ("nature2026_source_fig2.xlsx", "Fig.2c left", (1, 2)),
    "RMBA": ("nature2026_source_ED7.xlsx", "Extended Data Fig. 7b", (0, 1)),
    "PEA": ("nature2026_source_ED6.xlsx", "Extended Data Fig. 6b", (1, 2)),
}
FIG3_FILE = "nature2026_source_fig3.xlsx"
NATURE_DOI = "10.1038/s41586-026-10637-x"
PUBLISHED_THRESHOLDS = {
    "SMBA": [70, 10],
    "RMBA": [95, 10],
    "PEA": [140, 10],
}


def positive_pair(rows: list[dict], col_x: int, col_y: int) -> np.ndarray:
    values = []
    for r in rows:
        x, y = r.get(col_x), r.get(col_y)
        if x is None or y is None:
            continue
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            continue
        values.append([float(x), float(y)])
    a = np.asarray(values, dtype=float)
    if a.ndim != 2 or a.shape[0] < 5:
        raise ValueError("Need at least five deposited experimental fluence/intensity pairs")
    if not np.isfinite(a).all() or np.any(a <= 0):
        raise ValueError("Expected positive finite pump fluence and intensity")
    if not np.all(np.diff(a[:,0]) > 0):
        raise ValueError("Fluences must be strictly increasing")
    return a


def dcp_exclusion_points(rows: list[dict], columns: tuple[int,int,int],
                         multiplier: float = 2) -> list[dict]:
    """Arithmetic |deposited DCP| > multiplier × reported propagated error."""
    result = []
    for r in rows:
        triplet = [r.get(i) for i in columns]
        if not all(isinstance(v, (int,float)) for v in triplet):
            continue
        fluence, signal, error = [float(x) for x in triplet]
        if fluence<=0 or error<0 or not np.isfinite([fluence,signal,error]).all():
            raise ValueError("Invalid measured DCP point")
        result.append({
            "pump_uJ_cm2":fluence,
            "dcp_fraction":signal,
            "propagated_peak_error_fraction":error,
            "interval_avoids_zero":bool(abs(signal)>multiplier*error),
        })
    if len(result)<5 or any(b["pump_uJ_cm2"]<=a["pump_uJ_cm2"] for a,b in zip(result,result[1:])):
        raise ValueError("Invalid or unordered source DCP fluences")
    return result


def audit_all(folder: Path) -> dict:
    manifest = {}
    intensity = {}
    for key, (filename, sheet, columns) in SOURCE_FILES.items():
        f=folder/filename
        data=positive_pair(read_sheet(f,sheet),*columns)
        threshold,err=PUBLISHED_THRESHOLDS[key]
        normalized=data[:,1]/data[0,1]
        intensity[key] = {
            "n_fluences":int(len(data)),
            "raw_fluence_uJ_cm2":data[:,0].tolist(),
            "raw_peak_PL_source_units":data[:,1].tolist(),
            "within_sample_intensity_relative_to_first_point":normalized.tolist(),
            "paper_time_integrated_SF_threshold_uJ_cm2":threshold,
            "paper_threshold_quoted_error_uJ_cm2":err,
            "source_sheet":sheet,
        }
        manifest[key]={"publisher_workbook":filename,
                       "sha256":hashlib.sha256(f.read_bytes()).hexdigest()}
    fp=folder/FIG3_FILE
    manifest["DCP"]={"publisher_workbook":FIG3_FILE,
                     "sha256":hashlib.sha256(fp.read_bytes()).hexdigest()}
    rows=read_sheet(fp,"Fig. 3d")
    dcp={}
    for hand,cols in (("SMBA",(0,1,2)),("RMBA",(6,7,8))):
        points=dcp_exclusion_points(rows,cols,multiplier=2.0)
        candidates=[v for v in points if v["interval_avoids_zero"]]
        first=candidates[0]["pump_uJ_cm2"] if candidates else None
        nominal,err=PUBLISHED_THRESHOLDS[hand]
        dcp[hand]={
            "n_deposited_points":len(points),
            "source_points":points,
            "first_2x_error_nonzero_fluence_uJ_cm2":first,
            "first_2x_error_vs_paper_threshold": (
                "above published upper threshold reference" if first is not None and first>nominal+err
                else "not above published upper threshold reference"
            ),
        }
    src=read_sheet(folder/"nature2026_source_ED7.xlsx","Extended Data Fig. 7a")
    fluences=[]
    for col,v in sorted(src[0].items()):
        if col==0 or not isinstance(v,str) or "µJ" not in v:
            continue
        import re
        match=re.search(r"([0-9]+)",v)
        if match:fluences.append(int(match.group(1)))
    r_b=set(int(round(x)) for x in intensity["RMBA"]["raw_fluence_uJ_cm2"])
    unmatched=[v for v in fluences if v not in r_b]
    return {
        "paper_doi":NATURE_DOI,"files":manifest,
        "science_question":"Do source arrays show superlinear SF-like emission in achiral and chiral samples, while DCP emerges robustly only in chiral ones?",
        "published_reference_thresholds_from_time_integrated_PL":PUBLISHED_THRESHOLDS,
        "intensity":intensity,"dcp":dcp,
        "RMBA_ED7a_fluences_not_in_ED7b_rounded":unmatched,
        "data_limits":[
            "All three fluence-intensity datasets are source figure arrays, not independent raw streak camera frames.",
            "Source peak PL intensity is in arbitrary units, and detector/sample normalization between specimens is unknown. Normalization to the first point is only a shape display.",
            "Published SF thresholds come from time-integrated PL; this script does not refit them to these time-resolved intensity points.",
            "Published article reports achiral PEA superfluorescence without circularly polarized SF, but no fluence-resolved PEA DCP points were found in the inspected Fig. 3d source arrays.",
            "Two times the plotted propagated peak-intensity uncertainty is a descriptive exclusion-of-zero gate, NOT a 95-percent confidence interval.",
            "RMBA ED7a time-series header says 85 uJ/cm2 whereas ED7b intensity record uses 82 uJ/cm2; do not join those traces by position without clarification.",
            "Fluence sampling differs across specimens; this analysis cannot assign threshold ordering solely to chirality, nor prove a causal mechanism.",
            "No independently replicated R/S/PEA matched sets or calibrated system response are provided here.",
        ],
        "decision":"Reference superfluorescence thresholds are retained from the publication; intensity values are normalized within each specimen."
    }


def plot_gate(audit:dict,out:Path)->None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig,(left,right)=plt.subplots(1,2,figsize=(11.5,4.6))
    for name,series in audit["intensity"].items():
        x=np.asarray(series["raw_fluence_uJ_cm2"])
        y=np.asarray(series["within_sample_intensity_relative_to_first_point"])
        threshold,err=PUBLISHED_THRESHOLDS[name]
        left.plot(x,y,marker="o",label=f"{name} (published SF: {threshold}±{err})")
        left.axvspan(threshold-err,threshold+err,alpha=.07)
    left.set_xscale("log");left.set_yscale("log")
    left.set_xlabel("Pump fluence (µJ/cm²)")
    left.set_ylabel("Source PL peak / first measured PL peak")
    left.set_title("Within-sample response only")
    left.legend(fontsize=8)
    left.grid(alpha=.25)
    for name,pts in audit["dcp"].items():
        x=np.array([r["pump_uJ_cm2"] for r in pts["source_points"]])
        y=100*np.array([r["dcp_fraction"] for r in pts["source_points"]])
        e=100*np.array([r["propagated_peak_error_fraction"] for r in pts["source_points"]])
        right.errorbar(x,y,yerr=e,marker="o",capsize=2,label=name)
    right.axhline(0,color="gray",linewidth=.8)
    right.set_xlabel("Pump fluence (µJ/cm²)")
    right.set_ylabel("Peak DCP (%)")
    right.set_title("Chiral samples only; published Fig. 3d")
    right.legend(fontsize=8)
    right.grid(alpha=.25)
    fig.suptitle("Nature 2026 published chiral vs achiral SF controls — no fitted threshold",fontsize=12)
    fig.text(.015,.01,"Publisher Source Data: Fig. 2c, Ext. Figs. 6b/7b, Fig. 3d. Different specimens; arbitrary detector scales; paper threshold refs.",fontsize=8)
    fig.tight_layout(rect=[0,.04,1,.94])
    out.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(out,dpi=160)
    plt.close(fig)


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--folder",type=Path,default=Path("data/raw/kinetics"))
    p.add_argument("--fetch",action="store_true",help="Fetch/verify original publisher XLSX files only")
    p.add_argument("--out",type=Path,default=Path("results/nature2026_fluence_control_audit.json"))
    p.add_argument("--figure",type=Path,default=Path("results/nature2026_fluence_control.png"))
    args=p.parse_args(argv)
    if args.fetch:
        print(json.dumps(fetch_sources(args.folder),indent=2))
        return
    audit=audit_all(args.folder)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(audit,indent=2),encoding="utf-8")
    plot_gate(audit,args.figure)
    for sample in ("SMBA","RMBA","PEA"):
        print(sample,"intensity points:",audit["intensity"][sample]["n_fluences"],
              "published integrated-SF threshold:",PUBLISHED_THRESHOLDS[sample])
    for sample in ("SMBA","RMBA"):
        print(sample,"first 2x source-error nonzero DCP:",
              audit["dcp"][sample]["first_2x_error_nonzero_fluence_uJ_cm2"])
    print("RMBA unpaired nominal fluences in a vs b:",audit["RMBA_ED7a_fluences_not_in_ED7b_rounded"])
    print("Saved:",args.out,args.figure)


if __name__=="__main__":main()
