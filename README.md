# DemandIQ

Hierarchical retail demand forecasting and inventory optimization on the M5 benchmark.

**Status:** M1, problem framing and data understanding (in progress).

## What this project does
Forecasts 28-day daily demand per product-store series, quantifies forecast uncertainty,
and translates forecasts into simulated reorder decisions under documented assumptions.
See `docs/problem_statement.md` for the full problem definition and scope.

## Repository structure
| Path | Purpose |
|---|---|
| `data/` | Dataset skeleton; raw data is excluded from Git (see `data/README.md`) |
| `notebooks/` | Exploration and analysis |
| `src/` | Reusable code: data, features, models, evaluation, forecasting, inventory |
| `app/` | Streamlit dashboard (later milestone) |
| `tests/` | Automated tests |
| `scripts/` | Utility scripts (e.g., environment check) |
| `docs/`, `reports/` | Documentation and results |
| `artifacts/` | Local model outputs (not committed) |

## Setup (Windows, PowerShell)
Prerequisites: Python 3.11 or 3.12, Git, VS Code.

```powershell
git clone https://github.com/<your-username>/DemandIQ.git
cd DemandIQ
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

For exact reproduction of the original environment, use `requirements.lock.txt` instead.

## Verify the installation
```powershell
python -m scripts.verify_env
pytest
```

## Data
Download the M5 files from Kaggle (accept the competition rules first) into `data/raw/`.
Details: `data/README.md`.

## Limitations
The benchmark is public Walmart data and is not direct evidence of performance in other
markets. The inventory component is a simulation driven by stated assumptions.