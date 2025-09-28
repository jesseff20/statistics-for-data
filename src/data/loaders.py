# -*- coding: utf-8 -*-
"""Data loading helpers for the project."""
from pathlib import Path
from typing import Callable, Optional

import pandas as pd
import requests
from io import StringIO

# Define os diretórios de dados, garantindo que existam.
DATA_DIR = Path("data")
RAW = DATA_DIR / "raw"
EXTERNAL = DATA_DIR / "external"
PROCESSED = DATA_DIR / "processed"

RAW.mkdir(parents=True, exist_ok=True)
EXTERNAL.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)


def load_california_housing(
    fetch_fn: Optional[Callable[..., object]] = None,
) -> pd.DataFrame:
    """Load the California Housing dataset and cache it as CSV."""
    if fetch_fn is None:
        from sklearn.datasets import fetch_california_housing

        fetch_fn = fetch_california_housing

    print("Baixando o dataset California Housing...")
    ds = fetch_fn(as_frame=True)
    df = ds.frame

    output_path = RAW / "california_housing.csv"
    df.to_csv(output_path, index=False)
    print(f"Dataset salvo em: {output_path}")

    return df


def load_nyc_311(
    limit: int = 100_000, request_fn: Optional[Callable[..., object]] = None
) -> pd.DataFrame:
    """Fetch NYC 311 requests via the public API respecting the limit."""
    base = "https://data.cityofnewyork.us/resource/erm2-nwe9.csv"
    params = {"": limit}

    if request_fn is None:
        request_fn = requests.get

    print(f"Baixando {limit} registros do NYC 311...")
    response = request_fn(base, params=params, timeout=180)
    response.raise_for_status()

    df = pd.read_csv(StringIO(response.text))

    output_path = EXTERNAL / "nyc_311.csv"
    df.to_csv(output_path, index=False)
    print(f"Dataset salvo em: {output_path}")

    return df