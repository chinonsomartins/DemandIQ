# Data

Raw data is **not** stored in Git.

## Primary dataset
M5 Forecasting Accuracy (Walmart daily unit sales):
https://www.kaggle.com/competitions/m5-forecasting-accuracy

Accept the competition rules on Kaggle, download the files, and place them in `data/raw/`.

## Layout
- `raw/`       original files, never modified
- `interim/`   intermediate outputs (e.g., reshaped long-format data)
- `processed/` model-ready datasets and feature tables

Every file in `interim/` and `processed/` must be regenerable from `raw/` by code in `src/`.