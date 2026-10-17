# Project Case Study — Retail Demand Intelligence Platform

## Executive summary

An end-to-end, **historical retail demand forecasting and inventory intelligence demonstration** built with Python, MySQL, Power BI, XGBoost, and Streamlit. Starting with the M5 sales/calendar/prices dataset, the project develops store-level and selected product-level demand forecasts, tests them using time-aware validation, and turns the forecast outputs into an interactive inventory-risk simulator.

**Live demo:** https://retail-demand-intelligence-scbt7jcazpccwnp9mxmqpl.streamlit.app/  
**Repository:** https://github.com/sunnyraavan6-Sunny/retail-demand-intelligence

> The forecast window is **April 25–May 22, 2016**, and simulated stock figures are used throughout the inventory module. This work demonstrates analytical and engineering capability; it has **not** been shown to reduce actual retailer stockouts or holding costs.

## 1. Business problem

Retail decision makers need to understand:

- **How much demand is expected overall?** Store totals support broad capacity and purchasing discussions.
- **Which products may need attention?** Selected SKU forecasts reveal item-level variability.
- **How much trust should be placed in the forecasts?** Backtesting against a simple seasonal baseline provides evidence of model value.
- **What if inventory or lead time changes?** Scenario analysis makes reorder-threshold trade-offs visible.

The project addresses these questions through a transparent, reproducible sequence from historical data preparation to a deployed UI.

## 2. Dataset and scope

| Dimension | Implementation |
|---|---|
| Dataset | M5 Forecasting – Accuracy (historical sales, calendar, sell prices) |
| Store | CA_1 |
| Store-level history | 730 consecutive days |
| Product universe | 3,049 products in CA_1 sales data |
| Product forecast model | 20 selected products |
| Forecast horizon | 28 days |
| Historical forecast period | Apr 25 to May 22, 2016 |
| Available inventory data | No genuine stock-on-hand feed; inventory quantities are simulated |

The training, exploration, and dashboard development were performed locally. The production-style Streamlit demonstration deliberately relies on precomputed CSV outputs instead of requiring a live database, a model training environment, or third-party credentials to serve each page.

## 3. Data preparation and analytics

1. **Load and validate:** inspect missing and zero sales, duplicate keys, date continuity, and relevant data types.
2. **Reshape and enrich:** convert wide daily sales columns into daily item observations and join to a calendar; use prices for exploratory revenue reporting where the relevant join is available.
3. **Explore:** summarize daily volume, category contributions, leading products, and slow-moving products; investigate seasonality and holiday effects.
4. **Persist analytical outputs:** develop MySQL 8 views and use Power BI for interactive sales and product reporting.
5. **Prepare model-ready series:** aggregate CA_1 store demand and generate selected item-level daily histories.

**Artifacts built in the full local workflow:** SQL analytics views, two Power BI report pages (**Sales Overview** and **Product Intelligence**), Jupyter forecasting notebooks, model exports, forecast/report CSVs, and a five-tab Streamlit application. The public lightweight repository does not claim to include all development assets.

## 4. Forecasting design

### Target A — daily CA_1 store units

Predict aggregate units sold per day. Evaluate a **28-day seasonal-naïve benchmark** against **XGBoost regression** trained using calendar patterns, historical lags, shifted rolling statistics, and known calendar/SNAP indicators.

### Target B — daily units for 20 selected products

Train a pooled XGBoost regression model with product identification through one-hot-encoded features, plus the temporal feature set. Re-select top products using only pre-forecast history for each backtesting fold to avoid choosing validation winners using future results.

### Time-aware evaluation

- A **chronological 28-day holdout** gives an understandable final test-window comparison.
- **Four rolling-origin backtests** provide a broader check across changing historical conditions.
- The naïve benchmark and XGBoost are evaluated over the same periods at each forecasting level.
- WAPE is pooled using **summed absolute errors divided by summed actual units**, rather than an unweighted average of fold percentages.

### Results — rolling-origin backtest (primary portfolio comparison)

| Forecast level | Seasonal naïve WAPE | XGBoost WAPE | Relative error reduction |
|---|---:|---:|---:|
| CA_1 store | 11.18% | **7.70%** | ~31.1% |
| 20 selected products | 45.94% | **38.95%** | ~15.2% |

XGBoost improved WAPE in all four tested backtest folds for both levels.

### Results — final chronological 28-day holdout (distinct protocol)

| Forecast level | Seasonal naïve WAPE | XGBoost WAPE |
|---|---:|---:|
| CA_1 store | 10.05% | **4.13%** |
| 20 selected products | 40.50% | **31.14%** |

Product-level error is substantially higher than aggregate-store error. The metrics are **not comparable as if the models predict the same target**: they have different aggregation, volatility, and product coverage.

## 5. Inventory decision-support logic

With 28-day model outputs available, the project derives projected demand for lead times of **7, 14, and 28 days**, then adds a deliberately simple safety-stock buffer:

```text
safety_stock = ceil(1.645 × std(last 90 days of daily sales) × sqrt(lead_time_days))
reorder_point = ceil(expected_demand_during_lead_time + safety_stock)
inventory_position = stock_on_hand + incoming_units - backordered_units
```

Risk classes:

| Status | Illustrative rule | Business interpretation |
|---|---|---|
| Critical | Inventory position < expected lead-time demand | Shortfall may occur even before safety buffer |
| Reorder Review | Demand ≤ inventory position ≤ reorder point | Expected demand covered, buffer may be insufficient |
| Adequate | Inventory position > reorder point | Above the modeled replenishment threshold |

All starting stock quantities in the example dashboard are **simulated**. The user can edit hypothetical on-hand stock, orders, backorders, and lead time interactively without writing changes to the source data. "Shortfall to reorder point" is a gap to an illustrative threshold, **not a recommended order quantity**.

**Modeling caution:** The `1.645` safety factor is a normal approximation under strong assumptions. Actual service levels require calibration against forecast error, correlated daily demand, uncertain lead times, supply constraints, and business costs. The simulator is educational, not operational replenishment advice.

## 6. Delivery and user experience

The dashboard exposes five tabs:

| Tab | User workflow |
|---|---|
| Executive Overview | Scan 28-day total projected demand, top products, backtest metrics, simulated risks |
| Store Forecast | Review daily/weekly demand shape and forecast volume |
| Product Intelligence | Select among 20 products and compare 7-/14-/28-day forecasts |
| Inventory Risk | Filter simulated stock risk and interactively change inventory conditions |
| Model Performance | Compare model metrics against seasonal-naïve baseline across validation folds |

The deployment package includes only the Streamlit code, theme, precomputed CSV files, minimal Python dependencies, and documentation. It runs on Streamlit Community Cloud, and the pages were tested in a separate local deployment directory before publication.

## 7. Architecture and responsibilities of each tool

```text
Historical M5 files
  -> pandas data cleaning, long-format transformation, enrichment
  -> MySQL analytical views + Power BI exploration (local workflow)
  -> calendar/lag/rolling feature engineering
  -> chronological holdout + 4-fold rolling-origin evaluation
  -> store- and product-level XGBoost forecasts
  -> historical forecast CSVs + inventory threshold reports
  -> Streamlit app (Executive / Store / Product / Risk / Evaluation)
  -> GitHub -> Streamlit Community Cloud
```

- **MySQL:** analytical layer for reusable measures and joins during development.
- **Power BI:** business reporting layer for sales and product analysis during development.
- **Python / XGBoost:** data processing, baseline evaluation, forecasting, error metrics, and inventory computations.
- **Streamlit / Altair:** interactive decision-support presentation.
- **GitHub / Streamlit Cloud:** version control and accessible demonstration.

## 8. Challenges and lessons learned

**Avoiding temporal leakage.** Lags and rolling features must use strictly prior observations; product selection for evaluation should not depend on the future test period. This motivated shifted features, chronological splits, and fold-specific selection in product backtesting.

**Separating aggregate versus SKU uncertainty.** Store demand smooths some item-level volatility; the much higher product WAPE makes it risky to assume that a strong store model automatically implies accurate SKU replenishment.

**Distinguishing observed and assumed data.** The M5 dataset supports historical sales forecasting but not verified stock-on-hand status. Labeling every risk class and slider input as **simulated** avoids misleading business claims.

**Making deployment independent.** Packaging the app with precomputed CSVs avoids shipping raw large files, credentials, and a database server into a public Streamlit service.

## 9. Business value and limitations

**Demonstrated value:** A single interface links forecasts, historical evaluation, and explainable scenario rules; XGBoost reduced historical backtest error relative to the selected seasonal baseline.

**Not demonstrated:** Measured stockout reduction, revenue gain, cost savings, service-level improvement, or performance on post-2016/live retailer data. These require a real operational pilot, inventory and supplier records, and suitable business KPIs.

**Important scope boundaries:** the 20-item product subset is not the full assortment; independently trained store and SKU forecasts are not reconciled; the dashboard visualizes offline forecasts rather than forecasting on demand.

## 10. Suggested next iterations

1. Add new transactional feeds with automated daily refresh and monitoring.
2. Model all store-product hierarchies and reconcile aggregate/item predictions.
3. Benchmark against additional time-series models and report calibration/uncertainty intervals.
4. Use real inventory on hand, supplier lead times, and outstanding purchase orders.
5. Backtest actual replenishment decisions against stockout, waste, and holding-cost objectives.
6. Add reproducible training and CI tests to a separate, appropriately sanitized development repository.

## 11. Interview walkthrough (60–90 seconds)

> I built a historical Retail Demand Intelligence platform to connect sales analysis with ML forecasting and inventory decision support. I prepared the M5 sales and calendar data, analyzed CA_1 store performance with Python and MySQL, and built Power BI reports. For forecasting, I trained store-level and pooled product-level XGBoost models, compared both against a 28-day seasonal-naïve baseline, and used four rolling-origin backtests to reduce the risk of relying on one lucky split. The store model achieved 7.70% pooled backtest WAPE versus 11.18% for the baseline; the 20-product model achieved 38.95% versus 45.94%. I then built a five-tab Streamlit app with 28-day forecasts and an inventory simulator. The key limitation is that stock inputs are simulated and the data is historical, so the app demonstrates decision-support logic rather than real operational savings. Finally, I packaged and deployed it using GitHub and Streamlit Community Cloud.

## Dataset acknowledgement

M5 Forecasting – Accuracy: https://www.kaggle.com/competitions/m5-forecasting-accuracy
