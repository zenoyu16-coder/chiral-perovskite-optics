"""Octahedral geometry and symmetry descriptors from experimental CIFs."""
from __future__ import annotations

import hashlib
import math
from itertools import combinations
from pathlib import Path

import numpy as np
from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

from .data import read_sources


def _angle(v1: np.ndarray, v2: np.ndarray) -> float:
    cosine = float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    return math.degrees(math.acos(max(-1.0, min(1.0, cosine))))


def _pairings(indices: tuple[int, ...]):
    if not indices:
        yield ()
        return
    first = indices[0]
    for other in indices[1:]:
        rest = tuple(i for i in indices[1:] if i != other)
        for suffix in _pairings(rest):
            yield ((first, other),) + suffix


def octahedral_geometry(vectors: np.ndarray) -> dict[str, float]:
    """Six Pb->I vectors; optimally assign 3 nonoverlapping trans pairs."""
    vectors = np.asarray(vectors, dtype=float)
    if vectors.shape != (6, 3):
        raise ValueError("A complete PbI6 octahedron must contain six bond vectors.")
    lengths = np.linalg.norm(vectors, axis=1)
    if np.min(lengths) <= 0:
        raise ValueError("Zero-length bond.")
    angles = {(i, j): _angle(vectors[i], vectors[j]) for i, j in combinations(range(6), 2)}
    trans = min(
        _pairings(tuple(range(6))),
        key=lambda group: sum((180.0 - angles[min(i, j), max(i, j)]) ** 2 for i, j in group),
    )
    trans_pairs = {tuple(sorted(pair)) for pair in trans}
    cis_angles = [angle for pair, angle in angles.items() if pair not in trans_pairs]
    assert len(cis_angles) == 12
    mean_bond = float(np.mean(lengths))
    return {
        "pb_i_mean_A": mean_bond,
        "pb_i_bond_distortion": float(np.mean(np.abs(lengths - mean_bond)) / mean_bond),
        "cis_angle_variance_deg2": float(sum((angle - 90) ** 2 for angle in cis_angles) / 11),
        "trans_angle_mean_deg": float(np.mean([angles[tuple(sorted(pair))] for pair in trans])),
    }


def pb_i_octahedra(structure: Structure, cutoff_A: float = 3.7) -> tuple[dict, int]:
    """Each Pb gets 6 nearest I images within the cutoff; report incompleteness."""
    properties = []
    skipped = 0
    for pb in structure:
        if pb.specie.symbol != "Pb":
            continue
        iodides = sorted(
            (n for n in structure.get_neighbors(pb, cutoff_A) if n.specie.symbol == "I"),
            key=lambda n: n.nn_distance,
        )
        if len(iodides) != 6:
            skipped += 1
            continue
        vectors = np.array([n.coords - pb.coords for n in iodides], dtype=float)
        properties.append(octahedral_geometry(vectors))
    if not properties:
        return {}, skipped
    return {key: float(np.mean([item[key] for item in properties])) for key in properties[0]}, skipped


def describe_cif(path: Path, symprec: float = 0.05, cutoff_A: float = 3.7) -> dict:
    structure = Structure.from_file(str(path))
    if not structure.is_ordered:
        raise ValueError(f"Disordered sites in {path.name}; explicit occupancy handling required.")
    pb_count = sum(site.specie.symbol == "Pb" for site in structure)
    if pb_count == 0:
        raise ValueError(f"No Pb sites in {path.name}")
    analyzer = SpacegroupAnalyzer(structure, symprec=symprec)
    ops = analyzer.get_symmetry_operations(cartesian=False)
    # Sohncke-group classification uses the rotation parts of the symmetry operations.
    sohncke = all(np.linalg.det(op.rotation_matrix) > 0 for op in ops)
    bond_metrics, skipped = pb_i_octahedra(structure, cutoff_A=cutoff_A)
    result = {
        "formula": structure.composition.reduced_formula,
        "space_group": analyzer.get_space_group_symbol(),
        "space_group_number": analyzer.get_space_group_number(),
        "sohncke_space_group": bool(sohncke),
        "sites": len(structure),
        "pb_sites": pb_count,
        "cell_a_A": float(structure.lattice.a),
        "cell_b_A": float(structure.lattice.b),
        "cell_c_A": float(structure.lattice.c),
        "volume_A3": float(structure.volume),
        "volume_per_Pb_A3": float(structure.volume / pb_count),
        "pb_sites_skipped": skipped,
        "symprec_A": symprec,
        "cutoff_A": cutoff_A,
    }
    result.update(bond_metrics)
    return result


def analyze_sources(manifest: Path, data_dir: Path, symprec: float = 0.05, cutoff_A: float = 3.7):
    rows = []
    for source in read_sources(manifest):
        path = data_dir / source["cif_name"]
        if not path.is_file():
            raise FileNotFoundError(f"Missing {path}. Run 'chiral-pv fetch' first.")
        metrics = describe_cif(path, symprec=symprec, cutoff_A=cutoff_A)
        rows.append({
            "dataset_id": source["id"],
            "sample": source["sample"],
            "reported_hand": source["handedness"],
            "temperature_K": int(source["temperature_K"]),
            "doi": source["doi"],
            "cif_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            **metrics,
        })
    return rows
