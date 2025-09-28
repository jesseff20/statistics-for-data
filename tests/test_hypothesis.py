# -*- coding: utf-8 -*-
"""Tests for the hypothesis module."""
import numpy as np

from src.stats import hypothesis


def test_two_sample_ttest_returns_finite_values():
    rng = np.random.default_rng(123)
    sample_a = rng.normal(loc=0.0, scale=1.0, size=30)
    sample_b = rng.normal(loc=0.3, scale=1.0, size=30)

    stat, pvalue = hypothesis.two_sample_ttest(sample_a, sample_b)

    assert np.isfinite(stat)
    assert 0 <= pvalue <= 1


def test_chi_square_independence_expected_shapes():
    table = np.array([[12, 18], [32, 38]])

    chi2, pvalue, dof, expected, residuals = hypothesis.chi_square_independence(table)

    assert np.isfinite(chi2)
    assert 0 <= pvalue <= 1
    assert dof == 1
    assert expected.shape == table.shape
    assert residuals.shape == table.shape