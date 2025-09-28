# -*- coding: utf-8 -*-
"""Tests for model evaluation utilities."""
import numpy as np
import pytest

from src.models.evaluate import classification_report_proba


def test_classification_report_proba_supports_two_columns():
    y_true = np.array([0, 1, 1, 0])
    y_proba = np.array(
        [
            [0.8, 0.2],
            [0.2, 0.8],
            [0.3, 0.7],
            [0.6, 0.4],
        ]
    )

    metrics = classification_report_proba(y_true, y_proba)

    assert 0 <= metrics["auc"] <= 1
    assert 0 <= metrics["brier"] <= 1


def test_classification_report_proba_validates_threshold():
    with pytest.raises(ValueError):
        classification_report_proba([0, 1], [0.1, 0.9], threshold=2)


def test_classification_report_proba_size_mismatch():
    with pytest.raises(ValueError):
        classification_report_proba([0, 1], [0.1])