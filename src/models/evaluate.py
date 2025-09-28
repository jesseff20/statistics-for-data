# -*- coding: utf-8 -*-
"""Model evaluation helpers for probabilistic classifiers."""
from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.metrics import brier_score_loss, roc_auc_score


def _ensure_1d_proba(y_proba: Any) -> np.ndarray:
    """Normalise probability-like inputs to a 1D positive-class array."""
    arr = np.asarray(y_proba)
    if arr.ndim == 1:
        return arr
    if arr.ndim == 2:
        if arr.shape[1] == 1:
            return arr[:, 0]
        if arr.shape[1] == 2:
            return arr[:, 1]
    raise ValueError(
        "y_proba must be 1D or a two-column array of class probabilities for binary classification."
    )


def classification_report_proba(y_true, y_proba, threshold: float = 0.5):
    """Compute AUC and Brier score for probabilistic classifiers."""
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1.")

    proba = _ensure_1d_proba(y_proba)

    if len(y_true) != len(proba):
        raise ValueError("y_true and y_proba must have the same number of samples.")

    auc = roc_auc_score(y_true, proba)

    return {
        "auc": auc,
        "threshold": threshold,
        "brier": brier_score_loss(y_true, proba),
    }