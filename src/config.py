"""Central configuration: paths and global settings.

All other modules import paths from here, so no path is ever hard-coded elsewhere.
Values can be overridden through environment variables (or a local .env file).
"""
import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")  # silently does nothing if .env is absent

_data_dir = Path(os.getenv("DEMANDIQ_DATA_DIR", "data"))
DATA_DIR = _data_dir if _data_dir.is_absolute() else PROJECT_ROOT / _data_dir
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
REPORTS_DIR = PROJECT_ROOT / "reports"

RANDOM_SEED = int(os.getenv("DEMANDIQ_SEED", "42"))