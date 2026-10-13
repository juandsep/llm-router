"""Drift check: the same sample is stable, a shifted sample is flagged."""

import numpy as np

from llm_router.monitoring import psi


def test_identical_sample_is_stable() -> None:
    rng = np.random.default_rng(0)
    sample = rng.normal(size=500)
    assert psi(sample, sample) < 0.01


def test_shifted_sample_is_flagged() -> None:
    rng = np.random.default_rng(0)
    reference = rng.normal(loc=0.0, scale=1.0, size=500)
    shifted = rng.normal(loc=2.0, scale=1.0, size=500)
    assert psi(reference, shifted) > 0.25
