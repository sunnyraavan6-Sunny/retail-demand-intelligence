# Retail Demand Intelligence Platform

Retail forecasting and inventory analytics portfolio project.

## Features
- Store-level demand forecasting
- Forecasting for 20 products
- XGBoost model performance analysis
- Simulated inventory risk monitoring
- Interactive inventory simulator
- Streamlit executive dashboard

## Model Performance
- Store XGBoost backtest WAPE: 7.70%
- Product XGBoost backtest WAPE: 38.95%

## Run Locally
Install dependencies: pip install -r requirements.txt
Start app: streamlit run app/app.py

## Limitations
- Historical M5 data from 2016
- Precomputed forecasts
- Simulated inventory stock levels
- No live inventory integration