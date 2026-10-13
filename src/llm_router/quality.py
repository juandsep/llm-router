"""Metric gate: a model ships only if it clears the declared floor.

The gate is JSON (not YAML) to keep the layer dependency-free. `config/model_gate.json`
is the single source of truth: the training pipeline reads it, and so does
`tests/test_model_quality.py`.
"""

from __future__ import annotations

import json
from pathlib import Path

DEFAULT_GATE_PATH = Path("config/model_gate.json")

__all__ = ["assert_gate", "load_gate"]


def load_gate(path: Path = DEFAULT_GATE_PATH) -> dict:
    return json.loads(Path(path).read_text())


def assert_gate(metrics: dict, gate: dict) -> None:
    """Raise AssertionError when the primary metric is below the floor."""
    name = gate["primary_metric"]
    try:
        value = float(metrics["metrics"][name])
    except KeyError as exc:
        raise AssertionError(
            f"metric '{name}' missing from the evaluation output"
        ) from exc

    floor = float(gate["minimum_acceptable"])
    if value < floor:
        raise AssertionError(f"{name}={value:.4f} below the required minimum {floor}")
