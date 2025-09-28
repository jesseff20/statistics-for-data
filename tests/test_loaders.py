# -*- coding: utf-8 -*-
"""Tests for the data loaders module."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.data import loaders


@pytest.fixture
def temp_data_dirs(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Provide isolated data directories for each test run."""
    raw_dir = tmp_path / "raw"
    external_dir = tmp_path / "external"
    processed_dir = tmp_path / "processed"
    raw_dir.mkdir()
    external_dir.mkdir()
    processed_dir.mkdir()

    monkeypatch.setattr(loaders, "RAW", raw_dir)
    monkeypatch.setattr(loaders, "EXTERNAL", external_dir)
    monkeypatch.setattr(loaders, "PROCESSED", processed_dir)

    return raw_dir, external_dir, processed_dir


class DummyResponse:
    def __init__(self, text: str):
        self.text = text

    def raise_for_status(self):
        return None


def test_load_california_housing_creates_csv(temp_data_dirs):
    raw_dir, _, _ = temp_data_dirs

    def fake_fetch(as_frame: bool = True):
        assert as_frame is True

        class DummyDataset:
            frame = pd.DataFrame({"MedInc": [1.5], "HouseAge": [10]})

        return DummyDataset()

    df = loaders.load_california_housing(fetch_fn=fake_fetch)

    assert list(df.columns) == ["MedInc", "HouseAge"]
    assert df.shape == (1, 2)
    assert (raw_dir / "california_housing.csv").exists()


def test_load_nyc_311_respects_limit(temp_data_dirs):
    _, external_dir, _ = temp_data_dirs
    captured = {}

    def fake_request(url, params, timeout):
        captured["url"] = url
        captured["params"] = params
        captured["timeout"] = timeout
        return DummyResponse("complaint_type\nNoise\n")

    df = loaders.load_nyc_311(limit=42, request_fn=fake_request)

    assert captured["url"].endswith("erm2-nwe9.csv")
    assert captured["params"] == {"": 42}
    assert captured["timeout"] == 180
    assert df.iloc[0]["complaint_type"] == "Noise"
    assert (external_dir / "nyc_311.csv").exists()