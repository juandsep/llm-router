"""Metric gate: fails when the recorded evaluation drops below the declared floor."""

import json
from pathlib import Path

import pytest

from llm_router.quality import assert_gate, load_gate

METRICS = Path(__file__).parent / "fixtures" / "model_metrics.json"


def test_recorded_metrics_clear_the_gate() -> None:
    assert_gate(json.loads(METRICS.read_text()), load_gate())


def test_metric_below_the_floor_fails() -> None:
    metrics = json.loads(METRICS.read_text())
    metrics["metrics"] = {"roc_auc": 0.1}
    with pytest.raises(AssertionError):
        assert_gate(metrics, load_gate())
