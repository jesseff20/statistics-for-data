# -*- coding: utf-8 -*-
"""Tests for probability utilities."""
import math

import numpy as np
import pytest

from src.stats import probability


def test_bernoulli_pmf_validates_input():
    assert probability.bernoulli_pmf(1, 0.3) == pytest.approx(0.3)
    assert probability.bernoulli_pmf(0, 0.3) == pytest.approx(0.7)

    with pytest.raises(ValueError):
        probability.bernoulli_pmf(2, 0.5)

    with pytest.raises(ValueError):
        probability.bernoulli_pmf(1, 1.5)


def test_normal_cdf_basic_properties():
    left_tail = probability.normal_cdf(-1.0)
    right_tail = probability.normal_cdf(1.0)

    assert left_tail < 0.5 < right_tail
    assert math.isclose(right_tail, 1 - left_tail, rel_tol=1e-7)

    with pytest.raises(ValueError):
        probability.normal_cdf(0.0, std=0.0)


def test_sample_mean_ignores_nan():
    values = [1.0, np.nan, 3.0]
    result = probability.sample_mean(values)
    assert result == pytest.approx(2.0)

    with pytest.raises(ValueError):
        probability.sample_mean([])