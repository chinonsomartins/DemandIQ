# M5 Dataset Overview

**Milestone:** M1, Issue 3 | **Last updated:** 2026-11-15

## 1. Source and licensing
- **Dataset:** M5 Forecasting - Accuracy (Walmart daily unit sales)
- **URL:** https://www.kaggle.com/competitions/m5-forecasting-accuracy
- **Rules accepted on:** ‹YOU: date›
- **Permitted use (in my words, from the Rules page):** ‹YOU: one or two sentences›
- **Handling:** raw files live in `data/raw/` and are excluded from Git. Obtain them by
  following `data/README.md`.

## 2. Files

| File | Rows | Columns | Size on disk | Memory (optimised) | Purpose |
|---|---|---|---|---|---|
| calendar.csv | 1,969 | 14 | 0.1 MB | 0.1 MB | Maps `d_N` to dates; weekday, month, events, SNAP flags |
| sales_train_evaluation.csv | 30,490 | 1,947 | 116.1 MB | 114.2 MB | Daily unit sales per product-store series (wide) |
| sell_prices.csv | 6,841,121 | 4 | 194.0 MB | 58.8 MB | Weekly price per store-item-week |
| sales_train_validation.csv | 30,490 | 1,919 | 114.4 MB | not retained | First 1,913 days of the evaluation file |
| sample_submission.csv | not inspected | not inspected | 5.0 MB | not loaded | Competition submission format; unused |

**Decision:** `sales_train_evaluation.csv` is used as the full history. Time splits are
defined by this project (M2), not by the competition's hidden hold-out. This relies on the
validation file being a strict subset of the evaluation file. Verified in notebook cell 9: the two files hold the same series in the same order (ids differ only by the `_validation` / `_evaluation` suffix), and all 1,913 shared days are identical.

## 3. Structure
- **Series identifier:** `id` = item x store; 30,490 series (3,049 items x 10 stores).
- **Hierarchy columns:** `item_id`, `dept_id`, `cat_id`, `store_id`, `state_id`.
- **Time axis:** day columns `d_1` ... `d_1941`, covering 2011-01-29 to 2016-05-22
  (1,941 days, about 5.3 years).
- **Calendar extent:** 1,969 days. The final 28 days (`d_1942` onward) have calendar
  information but no sales; they correspond to the competition's forecast window.
- **Join keys:** sales.`d_N` = calendar.`d`; (calendar.`wm_yr_wk`, store_id, item_id)
  = prices key.

### Column glossary
| Table | Column | Meaning |
|---|---|---|
| sales | `id` | Unique series name (item and store) |
| sales | `item_id`, `dept_id`, `cat_id` | Product, its department, its category |
| sales | `store_id`, `state_id` | Store and its state |
| sales | `d_1` ... `d_1941` | Units sold on that day |
| calendar | `date`, `d` | Real date and the matching day label |
| calendar | `weekday`, `wday`, `month`, `year` | Day name, day number (1 = Saturday), month, year |
| calendar | `wm_yr_wk` | Walmart week ID; the link to prices |
| calendar | `event_name_1/2`, `event_type_1/2` | Special events (up to two per day) and their types |
| calendar | `snap_CA/TX/WI` | 1 if SNAP food-assistance purchases were allowed in that state that day |
| prices | `store_id`, `item_id`, `wm_yr_wk` | Store, product, and week |
| prices | `sell_price` | Selling price in that store-item-week |

## 4. Data quality findings

| Check | Result | Implication |
|---|---|---|
| Missing values, sales | 0 | None to handle |
| Missing values, prices (cells) | 0 | None to handle |
| Missing price rows (share of store-item-weeks priced) | 79.6% priced (1,757,059 of 8,598,180 combinations have no row) | Merging prices onto sales will create NaN prices. Hypothesis (to test in Issue 5): item not yet on sale, so leading zeros may not be true demand |
| Calendar event columns missing | `event_*_1`: 1,807 of 1,969; `event_*_2`: 1,964 of 1,969 | Structural: "no event"; encode as a category, do not impute |
| Duplicate rows / duplicate keys | 0 / 0 in all three tables | None to handle |
| Calendar contiguous | Yes | Safe to treat days as an unbroken sequence |
| Sales value range | 0 to 763 | int16 is safe: yes. The maximum of 763 is flagged for review in Issue 5 |
| Cross-file id and date consistency | All checks passed (sales days in calendar, price weeks in calendar, items and stores match) | Joins are safe |

## 5. Memory requirements

| Table | Naive MB | Optimised MB | Reduction |
|---|---|---|---|
| calendar | 0.3 | 0.1 | 73% |
| sales | 454.7 | 114.2 | 75% |
| prices | 318.1 | 58.8 | 82% |
| **Total** | **773** | **173** | **78%** |

- **Projected long-format size:** 59,181,090 rows at 14 bytes per row, about 0.77 GB
  (1.21 GB with a 64-bit date column). This is an arithmetic estimate, not a measurement.
- **Peak memory during reshape and merge:** to be measured in M2. Machine: 8 GB RAM.
- **Decision:** the full dataset appears feasible on 8 GB, but the choice between the full
  dataset and a store subset is finalised in M2 after profiling.

## 6. Open questions carried to Issues 4 and 5
- Are leading zeros (before an item's first price) real demand or "not yet on sale"?
- Do event and SNAP flags vary by state as documented?
- What explains the maximum daily sale of 763 units for one series? Genuine, or an anomaly?