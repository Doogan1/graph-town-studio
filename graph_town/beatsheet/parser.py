"""CSV beat-sheet parser.

Reads a CSV with columns ``beat_id, t_start, t_end, narration, visual_type,
scene_spec, notes`` and produces structured :class:`Beat` objects.

``scene_spec`` is a small DSL, chosen to be easy to write by hand in a
spreadsheet: an ordinary Python-call-shaped string of keyword arguments, e.g.

    vertex_deletion(nx_graph=g1, vertex=3)
    two_switch(nx_graph=g1, edge1=(1, 2), edge2=(3, 4))
    recap(title="Havel-Hakimi", steps=["Sort degrees", "Remove max", "Repeat"])

Bare identifiers (like ``g1`` above) are treated as named references to be
resolved later — typically against a graph a video script constructs in
Python and registers with the dispatcher — rather than literal values.
"""

from __future__ import annotations

import ast
import csv
from dataclasses import dataclass, field
from pathlib import Path


class SceneSpecError(ValueError):
    """Raised when a scene_spec string can't be parsed."""


@dataclass(frozen=True)
class Ref:
    """A named reference in a scene_spec (e.g. ``g1``), resolved by the dispatcher."""

    name: str


@dataclass
class Beat:
    beat_id: str
    t_start: float
    t_end: float
    narration: str
    visual_type: str
    scene_name: str
    scene_args: dict = field(default_factory=dict)
    notes: str = ""


def parse_scene_spec(spec: str) -> tuple[str, dict]:
    """Parse a ``scene_name(key=value, ...)`` string into (scene_name, kwargs)."""
    spec = spec.strip()
    try:
        tree = ast.parse(spec, mode="eval")
    except SyntaxError as exc:
        raise SceneSpecError(f"Invalid scene_spec syntax: {spec!r}") from exc

    call = tree.body
    if not isinstance(call, ast.Call) or not isinstance(call.func, ast.Name):
        raise SceneSpecError(
            f"scene_spec must look like 'scene_name(arg=value, ...)': {spec!r}"
        )
    if call.args:
        raise SceneSpecError(f"scene_spec only supports keyword arguments: {spec!r}")

    scene_name = call.func.id
    args = {kw.arg: _eval_arg(kw.value, spec) for kw in call.keywords}
    return scene_name, args


def _eval_arg(node: ast.expr, spec: str):
    if isinstance(node, ast.Name):
        return Ref(node.id)
    try:
        return ast.literal_eval(node)
    except (ValueError, TypeError) as exc:
        raise SceneSpecError(f"Unsupported value in scene_spec: {spec!r}") from exc


def parse_beatsheet(path: str | Path) -> list[Beat]:
    """Parse a beat-sheet CSV into a list of :class:`Beat` objects, in file order."""
    beats = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            spec = (row.get("scene_spec") or "").strip()
            scene_name, scene_args = parse_scene_spec(spec) if spec else ("", {})
            beats.append(
                Beat(
                    beat_id=row["beat_id"],
                    t_start=float(row["t_start"]),
                    t_end=float(row["t_end"]),
                    narration=row["narration"],
                    visual_type=row["visual_type"],
                    scene_name=scene_name,
                    scene_args=scene_args,
                    notes=row.get("notes", "") or "",
                )
            )
    return beats
