# DemandIQ: Problem Statement

**Version:** 1.0, **Milestone:** M1, **Status:** Draft for review

## 1. Business problem
Retailers must decide, for every product in every store, how much stock to hold and when to
reorder. Orders are placed before demand is known, so the decision depends on a forecast.

- **Underestimating demand** causes stockouts: lost sales, dissatisfied customers, and
  possible long-term loss of customers.
- **Overestimating demand** causes overstock: capital tied up in inventory, holding costs,
  and for perishable goods, waste and markdowns.

Because these costs are asymmetric and differ by product, an accurate point forecast alone
is insufficient. Decision-makers also need to know *how uncertain* the forecast is.

> **[To complete after literature review: 2-3 sentences with cited evidence on the scale of
> stockout and overstock costs in retail. Cite only sources you have read.]**

## 2. Target users and use case
**Primary user:** a store-level or regional replenishment planner (or demand planner) at a
multi-store retail chain.

**Use case:** at each review cycle, the planner selects a product-store combination, views
its demand history, the next 28 days of forecast demand with an uncertainty range, and a
recommended reorder point and order quantity under adjustable assumptions (lead time, service
level, costs).

**Secondary user:** a category or supply-chain manager reviewing forecast accuracy and
inventory-policy trade-offs across segments.

## 3. Forecasting objective
Predict **daily unit sales** for each selected product-store series, together with
prediction intervals, and evaluate whether a machine-learning approach improves on simple
statistical baselines and whether those forecasts improve simulated inventory outcomes.

## 4. Granularity and horizon
| Dimension | Specification |
|---|---|
| Forecast unit | Product (item) x store |
| Time resolution | Daily |
| Horizon | 28 days ahead (M5 convention) |
| Forecast origin | A fixed date; all features use only data available at the origin |
| Aggregation levels | Product-store (primary); department, store, and total via bottom-up aggregation |

The 28-day horizon is assumed to cover replenishment lead time plus review period. This
assumption is revisited in the inventory module (M6).

## 5. Measurable objectives
Thresholds are set before test-period evaluation to avoid selection bias.

| ID | Objective | Measure |
|---|---|---|
| O1 | Global ML model outperforms the Seasonal Naive baseline | Lower WRMSSE and RMSSE on rolling-origin validation. Gains reported with segment breakdown. |
| O2 | Prediction intervals are calibrated | Empirical coverage within +/-3 percentage points of nominal level, reported by horizon day and demand segment. *(Tolerance is a proposed design choice; revisit after M5.)* |
| O3 | Forecasts support an inventory policy | Under documented assumptions, the simulation reports stockout rate, unmet demand, average inventory, and estimated cost, with sensitivity analysis. |
| O4 | Results are reproducible | A new user can regenerate data preparation and core evaluation from the README. |

A model that does **not** beat the baseline is a valid outcome and will be reported as such.

## 6. Evaluation metrics
- **Point accuracy:** MAE, RMSE, WAPE, RMSSE (per series); WRMSSE (hierarchical, M5's
  official accuracy metric). Zero-demand handling is defined in the metrics module.
- **Probabilistic quality:** interval coverage and width; scaled pinball loss on quantiles.
- **Decision quality (simulated):** stockout rate, fill rate, average inventory, inventory
  turnover, estimated holding and stockout cost.

## 7. Scope
**In scope:** M5 data (starting with a tractable subset), baselines, global LightGBM,
quantile forecasts, bottom-up aggregation, assumption-based reorder-point simulation,
Streamlit dashboard, Docker packaging, tests.

**Out of scope for the MVP:** deep-learning forecasters, live point-of-sale integration,
multi-echelon optimization, automated purchasing.

## 8. Limitations and assumptions
1. M5 is public Walmart (US) data. Results are **not** evidence of performance in other
   markets, including Nigerian retail.
2. The dataset records *sales*, not true demand. Days with stockouts appear as zero sales
   (censored demand), which can bias models.
3. The inventory component is a simulation. Lead times, holding costs, stockout penalties,
   and service levels are assumptions, not observations. Results must be reported with
   sensitivity analysis and must not be presented as realized business savings.
4. Many product-store series are intermittent, so normal-distribution safety-stock formulas
   may be inaccurate for them. These series are flagged and treated separately.
5. The first release uses batch, scheduled forecasts only.

## 9. Deliverables
Reproducible pipeline, model comparison, uncertainty evaluation, inventory simulation report,
deployed dashboard, documented repository, and results report.

## 10. References
*(Add the sources you actually read in your literature review.)*