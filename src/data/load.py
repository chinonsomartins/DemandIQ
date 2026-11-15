"""Memory-efficient readers for the M5 files, plus data-quality helpers.

Design rules
- Hierarchy columns are read as `category`: they repeat heavily (3 states, 10 stores,
  7 departments, 3 categories), so storing integer codes plus one lookup table is far
  smaller than storing the string in every row.
- `id` is left as a plain string column: it is unique per row, so a category would add
  overhead and save nothing.
- Daily sales are stored as int16. Rather than assume they fit, we read as int32 first and
  verify the range, so silent overflow is impossible.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src import config

HIERARCHY_COLS = ["item_id", "dept_id", "cat_id", "store_id", "state_id"]
SALES_FILES = {
    "validation": "sales_train_validation.csv",
    "evaluation": "sales_train_evaluation.csv",
}
INT16_MAX = int(np.iinfo(np.int16).max)


def memory_mb(df: pd.DataFrame) -> float:
    """True memory footprint in MB. deep=True counts the string payload of object columns."""
    return df.memory_usage(deep=True).sum() / 1024**2


def read_calendar(path: str | Path | None = None) -> pd.DataFrame:
    path = Path(path) if path else config.RAW_DIR / "calendar.csv"
    dtypes = {
        "wm_yr_wk": "int16",
        "weekday": "category",
        "wday": "int8",
        "month": "int8",
        "year": "int16",
        "event_name_1": "category",
        "event_type_1": "category",
        "event_name_2": "category",
        "event_type_2": "category",
        "snap_CA": "int8",
        "snap_TX": "int8",
        "snap_WI": "int8",
    }
    return pd.read_csv(path, dtype=dtypes, parse_dates=["date"])


def read_sales(path: str | Path | None = None, version: str = "evaluation") -> pd.DataFrame:
    path = Path(path) if path else config.RAW_DIR / SALES_FILES[version]

    header = pd.read_csv(path, nrows=0).columns  # read column names only
    day_cols = [c for c in header if c.startswith("d_")]

    dtypes = {c: "category" for c in HIERARCHY_COLS}
    dtypes.update({c: "int32" for c in day_cols})
    df = pd.read_csv(path, dtype=dtypes)

    lowest, highest = int(df[day_cols].min().min()), int(df[day_cols].max().max())
    if lowest < 0 or highest > INT16_MAX:
        raise ValueError(f"Sales range [{lowest}, {highest}] does not fit int16")
    return df.astype({c: "int16" for c in day_cols})


def read_prices(path: str | Path | None = None) -> pd.DataFrame:
    path = Path(path) if path else config.RAW_DIR / "sell_prices.csv"
    dtypes = {
        "store_id": "category",
        "item_id": "category",
        "wm_yr_wk": "int16",
        "sell_price": "float32",  # prices have 2 decimals; float32's ~7 digits are ample
    }
    return pd.read_csv(path, dtype=dtypes)


def quality_report(df: pd.DataFrame, key_cols: list[str]) -> dict:
    """Missing values and duplicates. `key_cols` is the column set that SHOULD be unique."""
    missing = df.isna().sum()
    return {
        "rows": len(df),
        "columns": df.shape[1],
        "columns_with_missing": {c: int(n) for c, n in missing[missing > 0].items()},
        "full_row_duplicates": int(df.duplicated().sum()),
        "key_duplicates": int(df.duplicated(subset=key_cols).sum()),
    }