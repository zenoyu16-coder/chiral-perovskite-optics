"""Matched 298 K R/S/rac NEA2PbBr4 experimental CIF comparison.

The scalar geometry metrics are even under mirror reflection; they
cannot assign the sign or magnitude of optical activity.
"""
from __future__ import annotations

import hashlib
import numpy as np
from pathlib import Path
from pymatgen.core import Structure
from pymatgen.io.cif import CifParser
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

from .analysis import octahedral_geometry
from .data import read_sources


def pb_halide_metrics(structure: Structure, halogen: str = "Br", cutoff_A: float = 3.7) -> dict:
    """Report complete sixfold Pb-X neighbors; fail instead of silently skipping."""
    records = []
    b_axis_unit = structure.lattice.matrix[1] / np.linalg.norm(structure.lattice.matrix[1])
    for site in structure:
        if site.specie.symbol != "Pb":
            continue
        nbrs = sorted(
            (n for n in structure.get_neighbors(site, cutoff_A) if n.specie.symbol == halogen),
            key=lambda n: n.nn_distance,
        )
        if len(nbrs) != 6:
            raise ValueError(f"Pb site has {len(nbrs)} {halogen} neighbors within {cutoff_A} A (expected 6)")
        vectors = np.array([n.coords - site.coords for n in nbrs])
        local = octahedral_geometry(vectors)
        records.append({
            "halide_centroid_minus_pb_b_A": float(np.dot(vectors.mean(axis=0), b_axis_unit)),
            "pb_x_mean_A": local["pb_i_mean_A"],
            "pb_x_bond_distortion": local["pb_i_bond_distortion"],
            "cis_angle_variance_deg2": local["cis_angle_variance_deg2"],
            "trans_angle_mean_deg": local["trans_angle_mean_deg"],
        })
    if not records:
        raise ValueError("No Pb atoms in structure.")
    return {key: float(np.mean([record[key] for record in records])) for key in records[0]}


def analyze_matched(manifest: Path, data_dir: Path, symprec: float = 0.05, cutoff_A: float = 3.7) -> list[dict]:
    rows = read_sources(manifest)
    if len(rows) != 3 or {r["handedness"] for r in rows} != {"R", "S", "rac"}:
        raise ValueError("Exactly one R, S and rac entry are required.")
    if len({r["sample"] for r in rows}) != 1 or len({r["temperature_K"] for r in rows}) != 1:
        raise ValueError("Matched samples must share chemistry and experimental temperature.")
    results = []
    for row in rows:
        path = data_dir / row["cif_name"]
        if not path.is_file():
            raise FileNotFoundError(f"Missing {path}; run matched-fetch first.")
        s = Structure.from_file(str(path))
        if not s.is_ordered:
            raise ValueError(f"Partial occupancies in {path.name}; cannot automatically compare.")
        if "Br" not in s.composition or "Pb" not in s.composition:
            raise ValueError(f"Expected Pb-Br compound in {path}")
        sga = SpacegroupAnalyzer(s, symprec=symprec)
        operations = sga.get_symmetry_operations(cartesian=False)
        sohncke = all(np.linalg.det(o.rotation_matrix) > 0 for o in operations)
        has_inversion = any(np.allclose(o.rotation_matrix, -np.eye(3)) for o in operations)
        properties = pb_halide_metrics(s, cutoff_A=cutoff_A)
        block = next(iter(CifParser(str(path))._cif.data.values()))
        flack_raw = block.data.get("_refine_ls_abs_structure_Flack", "")
        results.append({
            "dataset_id": row["id"], "sample": row["sample"], "hand": row["handedness"],
            "temperature_K": int(row["temperature_K"]), "ccdc": row["ccdc"], "doi": row["doi"],
            "cif_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "flack_parameter_cif": str(flack_raw),
            "formula": s.composition.reduced_formula,
            "symmetry_space_group": sga.get_space_group_symbol(),
            "symmetry_number": sga.get_space_group_number(),
            "sohncke": bool(sohncke), "has_inversion": bool(has_inversion),
            "pb_sites": int(s.composition["Pb"]), "volume_per_Pb_A3": float(s.volume/s.composition["Pb"]),
            "symprec_A": symprec, "cutoff_A": cutoff_A, **properties,
        })
    chem = [r["formula"] for r in results]
    if len(set(chem)) != 1:
        raise ValueError(f"Formula mismatch across nominally matched samples: {chem}")
    return results


def relative_scalar_differences(rows: list[dict]) -> dict:
    """Percentage R-S differences; scalar parity-even structural quantities only."""
    pair = {r["hand"]: r for r in rows}
    return {name: 100.0 * (pair["R"][name] - pair["S"][name])
            / ((pair["R"][name] + pair["S"][name]) / 2.0)
            for name in ("volume_per_Pb_A3","pb_x_mean_A","pb_x_bond_distortion","cis_angle_variance_deg2")}
