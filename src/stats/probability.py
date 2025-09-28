# -*- coding: utf-8 -*-
"""Probability utilities used across the project."""
from __future__ import annotations

from typing import Iterable

import numpy as np
from scipy import stats


def bernoulli_pmf(k: int, p: float) -> float:
    """Return the probability of observing `k` in a Bernoulli(p)."""
    if k not in (0, 1):
        raise ValueError("k must be 0 or 1 for a Bernoulli distribution.")
    if not 0 <= p <= 1:
        raise ValueError("p must be between 0 and 1.")
    return p if k == 1 else 1 - p


def normal_cdf(x: float, mean: float = 0.0, std: float = 1.0) -> float:
    """Evaluate the Normal CDF in `x` with the given location and scale."""
    if std <= 0:
        raise ValueError("std must be positive.")
    return float(stats.norm.cdf(x, loc=mean, scale=std))


def sample_mean(values: Iterable[float]) -> float:
    """Return the arithmetic mean ignoring NaN values."""
    arr = np.asarray(list(values), dtype=float)
    if arr.size == 0:
        raise ValueError("values must contain at least one element")
    return float(np.nanmean(arr))