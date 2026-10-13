"""Population Stability Index: drift check with no extra dependency beyond numpy.

PSI is a convenience threshold, not physics. Tune the cutoffs per feature and
record why: 0.1 watch, 0.2 investigate, 0.25 retrain.
"""

from __future__ import annotations

import numpy as np

EPS = 1e-6

__all__ = ["psi"]


def psi(
    expected: list[float] | np.ndarray, actual: list[float] | np.ndarray, bins: int = 10
) -> float:
    """PSI between two 1-D samples. Bin edges come from `expected` quantiles."""
    e = np.asarray(expected, dtype=float)
    a = np.asarray(actual, dtype=float)
    if e.size == 0 or a.size == 0:
        raise ValueError("psi needs two non-empty samples")

    edges = np.quantile(e, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf

    e_pct = np.clip(np.histogram(e, bins=edges)[0] / e.size, EPS, None)
    a_pct = np.clip(np.histogram(a, bins=edges)[0] / a.size, EPS, None)
    return float(np.sum((a_pct - e_pct) * np.log(a_pct / e_pct)))
