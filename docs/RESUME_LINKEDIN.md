# Retail Demand Intelligence — Resume, LinkedIn and Portfolio Copy

These descriptions are intended for an **independent academic/personal portfolio project**; do not present it as paid client work or a retailer production deployment.

**Project:** Retail Demand Intelligence Platform  
**Repository:** https://github.com/sunnyraavan6-Sunny/retail-demand-intelligence  
**Live demo:** https://retail-demand-intelligence-scbt7jcazpccwnp9mxmqpl.streamlit.app/

## A. Recommended resume entry (Data Analyst / Business Analyst)

**Retail Demand Intelligence Platform | Python, SQL, Power BI, XGBoost, Streamlit**

- Built an end-to-end historical retail analytics platform using M5 sales data, Python and MySQL, with Power BI views for store, category and product performance.
- Developed 28-day demand forecasts for **CA_1 store and 20 selected products**; reduced pooled rolling-backtest WAPE from **11.18% to 7.70%** at store level and from **45.94% to 38.95%** at product level versus a seasonal-naïve baseline.
- Deployed a **five-tab Streamlit dashboard** with forecast visualizations, model comparisons, and an interactive **simulated** inventory-risk/reorder-point scenario tool.

## B. Recommended resume entry (Data Science / ML Engineer)

**Retail Demand Intelligence Platform | Python, XGBoost, pandas, scikit-learn, MySQL, Streamlit**

- Engineered time-series forecasting features from **730 days of historical CA_1 sales**, including calendar, holiday/SNAP, lag and shifted rolling statistics.
- Trained store- and item-level XGBoost models, validated against a **28-day seasonal-naïve baseline** using a chronological holdout and **four rolling-origin folds**; achieved pooled WAPE of **7.70% (store)** and **38.95% (20 products)**.
- Exported 28-day forecasts and built a cloud-deployed Streamlit application featuring model evaluation and adjustable, assumption-based inventory thresholds.

## C. Compact version (for a one-page fresher resume)

**Retail Demand Intelligence Platform — Python, SQL, XGBoost, Power BI, Streamlit**

- Forecasted 28-day retail demand for **one store and 20 products**, achieving **7.70% store-level** and **38.95% item-level pooled backtest WAPE** using XGBoost.
- Built and deployed a **five-tab analytics dashboard** combining historical model validation, product forecasts and **simulated** stock-risk scenarios.

## D. LinkedIn Featured project description

**Retail Demand Intelligence Platform | Sales Analytics + Forecasting + Inventory Simulation**

Built and deployed an end-to-end historical retail analytics and forecasting project using Python, MySQL, Power BI, XGBoost, and Streamlit. The application shows 28-day projected demand for M5 store CA_1 and 20 selected products, compares XGBoost against a seasonal-naïve baseline using rolling-origin backtesting, and supports interactive simulated inventory-risk scenarios.

**Backtesting:** Store WAPE **7.70%** (baseline 11.18%); product WAPE **38.95%** (baseline 45.94%). Results are historical, not live; inventory inputs are simulated.

**Live app:** https://retail-demand-intelligence-scbt7jcazpccwnp9mxmqpl.streamlit.app/  
**Code:** https://github.com/sunnyraavan6-Sunny/retail-demand-intelligence

## E. LinkedIn announcement draft

I recently completed and deployed my **Retail Demand Intelligence Platform**, an end-to-end portfolio project combining data analytics, machine learning, and inventory decision support.

Using historical M5 retail data, I worked through Python-based data processing, SQL analysis, Power BI exploration, and XGBoost forecasting. I evaluated the forecasts against a seasonal-naïve baseline with rolling-origin backtesting rather than relying on a single split.

**Results:** 7.70% pooled backtest WAPE for store demand and 38.95% for a selected set of 20 products, both better than their respective baselines.

The live Streamlit app has an executive overview, store and product forecasts, model performance, and an interactive **simulated inventory-risk** tool. The forecast dates are historical (2016), and the stock inputs are demonstration values, not real business inventory.

Live demo: https://retail-demand-intelligence-scbt7jcazpccwnp9mxmqpl.streamlit.app/  
GitHub: https://github.com/sunnyraavan6-Sunny/retail-demand-intelligence

#Python #DataAnalytics #MachineLearning #XGBoost #PowerBI #SQL #Streamlit #PortfolioProject

## F. Portfolio website card

**Title:** Retail Demand Intelligence  
**Subtitle:** Historical retail forecasting and inventory decision-support dashboard  
**Stack:** Python · MySQL · Power BI · XGBoost · Streamlit · Altair  
**Description:** Built and deployed a five-tab dashboard combining CA_1 store forecasts, 20-product demand intelligence, model evaluation and simulated inventory scenarios. Four rolling-origin folds showed XGBoost WAPE of 7.70% at store level and 38.95% across selected products, outperforming the 28-day seasonal-naïve baseline at both levels.  
**Links:** [Live demo](https://retail-demand-intelligence-scbt7jcazpccwnp9mxmqpl.streamlit.app/) · [GitHub](https://github.com/sunnyraavan6-Sunny/retail-demand-intelligence)

## G. Interview answers: claims you can defend

**What does 7.70% mean?**  
It's pooled WAPE across four rolling-origin backtest folds for daily **aggregate store demand**, not "92.30% overall business accuracy" or a result guaranteed for future data.

**Why is product WAPE higher?**  
Individual items have much noisier demand and a larger share of low/zero-demand days than aggregate store totals. SKU-level uncertainty remains an operational risk.

**Did this reduce real-world stockouts or costs?**  
No. The inventory module is an illustrative simulator because the M5 dataset lacks live stock-on-hand and actual supplier lead times. I did not measure cost savings or stockout reductions.

**Does the deployed app generate forecasts live?**  
No. Model fitting and forecast generation ran offline. Streamlit serves precomputed 2016 forecasts and supports live interaction only for visualization and hypothetical inventory scenarios.

**Why use rolling-origin evaluation?**  
It tests the forecasting procedure over several historical prediction origins and reduces dependence on one final test period while respecting time order.

**What would you do next?**  
Automate data ingestion and retraining, validate feature/data drift, reconcile forecast hierarchies, add real inventory and lead-time feeds, and evaluate business KPIs in a controlled pilot.

## H. Resume presentation guidelines

- Present this as a **portfolio project**, not employer experience.
- Pair the numeric WAPE metric with **rolling-origin backtesting** and the correct store-versus-product scope.
- Say **"simulated inventory risk"**, never "live stockouts prevented" or "95% guaranteed service level."
- Include both GitHub and live demo links, preferably under the project title.
- Do not claim your publicly deployed repository contains raw datasets, PBIX files, or training notebooks unless you've actually committed them.
