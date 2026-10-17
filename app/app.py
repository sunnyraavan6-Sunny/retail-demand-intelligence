
import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

st.set_page_config(
    page_title="Retail Demand Intelligence",
    page_icon="📊",
    layout="wide"
)

ROOT = Path(__file__).resolve().parents[1]

required_files = {
    "Store forecast": ROOT / "data/processed/ca1_28day_forecast.csv",
    "Product forecast": ROOT / "data/processed/ca1_top20_28day_forecasts.csv",
    "Product demand plan": ROOT / "reports/ca1_top20_inventory_demand_plan.csv",
    "Inventory risk": ROOT / "reports/ca1_top20_inventory_risk_simulated.csv"
}

missing_files = [
    str(path)
    for path in required_files.values()
    if not path.exists()
]

if missing_files:
    st.error("Some required project files are missing.")
    st.code("\n".join(missing_files))
    st.stop()

@st.cache_data
def load_csv(path, date_columns=()):
    return pd.read_csv(
        path,
        parse_dates=list(date_columns)
    )

store_forecast = load_csv(
    required_files["Store forecast"], ("date",)
)

product_forecast = load_csv(
    required_files["Product forecast"], ("date",)
)

demand_plan = load_csv(
    required_files["Product demand plan"]
)

inventory = load_csv(
    required_files["Inventory risk"]
)

st.title("📊 Retail Demand Intelligence Platform")

st.caption(
    "CA_1 Store | Historical Forecast: "
    "April 25 – May 22, 2016"
)

st.info(
    "Portfolio demonstration using historical M5 data. "
    "Inventory stock levels are simulated, not actual."
)

tab0, tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Executive Overview",
    "📈 Store Forecast",
    "📦 Product Intelligence",
    "🚨 Inventory Risk",
    "📊 Model Performance"
])

# =====================================================
# TAB 1: STORE FORECASTING
# =====================================================

with tab1:
    st.header("Store-Level Demand Forecast")

    total = int(store_forecast["predicted_units"].sum())
    average = store_forecast["predicted_units"].mean()

    c1, c2, c3 = st.columns(3)

    c1.metric("Forecast Horizon", "28 Days")
    c2.metric("Predicted Total Units", f"{total:,}")
    c3.metric("Average Daily Units", f"{average:,.0f}")

    st.subheader("Daily Forecast")

    st.line_chart(
        store_forecast.set_index("date")["predicted_units"]
    )

    weekly = store_forecast.copy()

    weekly["week"] = (
        (weekly["date"] - weekly["date"].min()).dt.days
        // 7 + 1
    )

    weekly = (
        weekly.groupby("week")["predicted_units"]
        .sum()
        .reset_index()
    )

    st.subheader("Weekly Demand")
    st.bar_chart(weekly.set_index("week"))

# =====================================================
# TAB 2: PRODUCT INTELLIGENCE
# =====================================================

with tab2:
    st.header("Product-Level Demand Forecasting")

    product_ids = sorted(
        product_forecast["item_id"].unique()
    )

    selected_product = st.selectbox(
        "Select Product",
        product_ids
    )

    selected_data = product_forecast.loc[
        product_forecast["item_id"] == selected_product
    ].sort_values("date")

    selected_plan = demand_plan.loc[
        demand_plan["item_id"] == selected_product
    ].iloc[0]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Next 7 Days",
        f"{int(selected_plan['predicted_7d_units']):,}"
    )

    c2.metric(
        "Next 14 Days",
        f"{int(selected_plan['predicted_14d_units']):,}"
    )

    c3.metric(
        "Next 28 Days",
        f"{int(selected_plan['predicted_28d_units']):,}"
    )

    st.subheader("Product Demand Forecast")

    st.line_chart(
        selected_data.set_index("date")["predicted_units"]
    )

    st.subheader("All 20 Product Demand Estimates")
    st.dataframe(demand_plan, hide_index=True)

    st.caption(
        "Historical product-level backtesting WAPE: 38.95%."
    )

# =====================================================
# TAB 3: INVENTORY RISK
# =====================================================

with tab3:
    st.header("Inventory Risk Monitoring")

    st.warning(
        "SIMULATED INVENTORY SCENARIO. "
        "Stock quantities and supplier lead times are "
        "illustrative, not real inventory records."
    )

    counts = inventory["risk_status"].value_counts()

    critical = int(counts.get("Critical", 0))
    review = int(counts.get("Reorder Review", 0))
    adequate = int(counts.get("Adequate", 0))

    c1, c2, c3 = st.columns(3)

    c1.metric("Critical", critical)
    c2.metric("Reorder Review", review)
    c3.metric("Adequate", adequate)

    st.subheader("Product Inventory Status")

    risk_filter = st.selectbox(
        "Filter by Risk",
        ["All", "Critical", "Reorder Review", "Adequate"]
    )

    filtered = inventory.copy()

    if risk_filter != "All":
        filtered = filtered.loc[
            filtered["risk_status"] == risk_filter
        ]

    columns = [
        "item_id",
        "stock_on_hand",
        "inventory_position",
        "expected_demand",
        "safety_stock",
        "reorder_point",
        "risk_status"
    ]

    st.dataframe(
        filtered[columns],
        hide_index=True
    )

    st.caption(
        "Reorder thresholds are illustrative and should "
        "not be interpreted as verified purchasing advice."
    )



# =====================================================
# MODEL PERFORMANCE DASHBOARD - STEP 25
# =====================================================

with tab4:

    st.header("Machine Learning Model Performance")

    st.caption(
        "Historical rolling-origin backtesting. "
        "Metrics describe validation performance, "
        "not guaranteed future accuracy."
    )

    evaluation_level = st.radio(
        "Select forecasting level",
        ["Store-Level", "Product-Level"],
        horizontal=True
    )

    if evaluation_level == "Store-Level":

        backtest_file = (
            ROOT / "reports"
            / "ca1_rolling_backtest_results.csv"
        )

        st.subheader("Store Demand Forecasting")

    else:

        backtest_file = (
            ROOT / "reports"
            / "ca1_top20_rolling_backtest.csv"
        )

        st.subheader("Product Demand Forecasting")

    if not backtest_file.exists():

        st.error(
            f"Backtesting report not found: {backtest_file}"
        )

    else:

        backtest = load_csv(backtest_file)

        # Standardize column names from both reports
        backtest = backtest.rename(columns={
            "Fold": "fold",
            "Model": "model",
            "Absolute Error Sum": "abs_error",
            "Squared Error Sum": "squared_error",
            "Actual Units": "actual_units",
            "Days": "observations",
            "absolute_error_sum": "abs_error",
            "squared_error_sum": "squared_error"
        })

        # Aggregate errors correctly across folds
        overall = backtest.groupby("model").agg(
            abs_error=("abs_error", "sum"),
            squared_error=("squared_error", "sum"),
            actual_units=("actual_units", "sum"),
            observations=("observations", "sum")
        )

        overall["MAE"] = (
            overall["abs_error"] /
            overall["observations"]
        )

        overall["RMSE"] = (
            overall["squared_error"] /
            overall["observations"]
        ) ** 0.5

        overall["WAPE (%)"] = (
            overall["abs_error"] /
            overall["actual_units"] * 100
        )

        baseline = overall.loc["Seasonal Naive"]
        xgboost = overall.loc["XGBoost"]

        improvement_pp = (
            baseline["WAPE (%)"] -
            xgboost["WAPE (%)"]
        )

        relative_improvement = (
            improvement_pp /
            baseline["WAPE (%)"] * 100
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Seasonal Naive WAPE",
            f"{baseline['WAPE (%)']:.2f}%"
        )

        c2.metric(
            "XGBoost WAPE",
            f"{xgboost['WAPE (%)']:.2f}%"
        )

        c3.metric(
            "Relative WAPE Reduction",
            f"{relative_improvement:.1f}%"
        )

        st.subheader("Forecasting Error by Validation Fold")

        fold_chart = (
            backtest.pivot(
                index="fold",
                columns="model",
                values="WAPE (%)"
            )
            .sort_index()
        )

        st.bar_chart(fold_chart)

        st.subheader("Overall Model Comparison")

        comparison = pd.DataFrame({
            "Model": [
                "Seasonal Naive",
                "XGBoost"
            ],
            "MAE": [
                baseline["MAE"],
                xgboost["MAE"]
            ],
            "RMSE": [
                baseline["RMSE"],
                xgboost["RMSE"]
            ],
            "WAPE (%)": [
                baseline["WAPE (%)"],
                xgboost["WAPE (%)"]
            ]
        })

        st.dataframe(
            comparison.round(2),
            hide_index=True,
            use_container_width=True
        )

        st.subheader("Individual Validation Folds")

        st.dataframe(
            backtest[
                ["fold", "model", "MAE",
                 "RMSE", "WAPE (%)"]
            ].round(2),
            hide_index=True,
            use_container_width=True
        )

        st.info(
            "Store-level and product-level metrics "
            "measure different prediction targets "
            "and should not be compared directly."
        )



# =====================================================
# INVENTORY SIMULATOR - STEP 26
# =====================================================

with tab3:

    st.divider()
    st.subheader("Interactive Inventory Simulator")

    st.info(
        "Simulation only. Adjust inventory inputs to "
        "explore how modeled stock risk changes."
    )

    reorder_file = (
        ROOT / "reports"
        / "ca1_top20_inventory_reorder_points.csv"
    )

    if not reorder_file.exists():
        st.error("Reorder-point report is missing.")

    else:
        reorder_data = load_csv(reorder_file)

        selected_item = st.selectbox(
            "Select product to simulate",
            sorted(reorder_data["item_id"].unique()),
            key="sim_product"
        )

        lead_time = st.select_slider(
            "Supplier lead time (days)",
            options=[7, 14, 28],
            value=7,
            key="sim_lead_time"
        )

        selected_plan = reorder_data.loc[
            (reorder_data["item_id"] == selected_item) &
            (reorder_data["lead_time_days"] == lead_time)
        ]

        original_stock = inventory.loc[
            inventory["item_id"] == selected_item
        ]

        if selected_plan.empty or original_stock.empty:
            st.error("Inventory data unavailable for this product.")

        else:
            plan = selected_plan.iloc[0]
            initial = original_stock.iloc[0]

            c1, c2, c3 = st.columns(3)

            with c1:
                stock = st.number_input(
                    "Stock on hand",
                    min_value=0,
                    value=int(initial["stock_on_hand"]),
                    step=1,
                    key=f"sim_stock_{selected_item}"
                )

            with c2:
                on_order = st.number_input(
                    "Incoming stock",
                    min_value=0,
                    value=int(initial["units_on_order"]),
                    step=1,
                    key=f"sim_order_{selected_item}"
                )

            with c3:
                backorders = st.number_input(
                    "Backordered units",
                    min_value=0,
                    value=int(initial["backordered_units"]),
                    step=1,
                    key=f"sim_backorders_{selected_item}"
                )

            # Calculate the inventory position
            inventory_position = (
                stock + on_order - backorders
            )

            expected_demand = int(plan["expected_demand"])
            safety_stock = int(plan["safety_stock"])
            reorder_point = int(plan["reorder_point"])

            # Determine inventory risk
            if inventory_position < expected_demand:
                risk_status = "Critical"

            elif inventory_position <= reorder_point:
                risk_status = "Reorder Review"

            else:
                risk_status = "Adequate"

            shortfall = max(
                0, reorder_point - inventory_position
            )

            st.subheader("Calculated Inventory Metrics")

            m1, m2, m3, m4 = st.columns(4)

            m1.metric(
                "Inventory Position",
                f"{inventory_position:,}"
            )

            m2.metric(
                "Expected Demand",
                f"{expected_demand:,}"
            )

            m3.metric(
                "Safety Stock",
                f"{safety_stock:,}"
            )

            m4.metric(
                "Reorder Point",
                f"{reorder_point:,}"
            )

            if risk_status == "Critical":
                st.error(
                    "CRITICAL: Inventory position is below "
                    "expected lead-time demand."
                )

            elif risk_status == "Reorder Review":
                st.warning(
                    "REORDER REVIEW: Demand is covered, "
                    "but the modeled safety buffer is insufficient."
                )

            else:
                st.success(
                    "ADEQUATE: Inventory position exceeds "
                    "the modeled reorder point."
                )

            st.metric(
                "Shortfall to Reorder Point",
                f"{shortfall:,} units"
            )

            st.caption(
                "Shortfall is a threshold gap, not a "
                "recommended purchase quantity. "
                "Incoming stock is assumed available within "
                "the selected lead time. Changes are "
                "temporary and are not saved."
            )



# =====================================================
# EXECUTIVE OVERVIEW - STEP 27
# =====================================================

with tab0:

    st.header("Executive Overview")

    st.caption(
        "CA_1 Retail Demand Intelligence | "
        "Historical demonstration: April-May 2016"
    )



    # -------------------------------------------------
    # LOAD HISTORICAL MODEL PERFORMANCE
    # -------------------------------------------------

    store_bt = pd.read_csv(
        ROOT / "reports"
        / "ca1_rolling_backtest_results.csv"
    )

    product_bt = pd.read_csv(
        ROOT / "reports"
        / "ca1_top20_rolling_backtest.csv"
    )

    store_xgb = store_bt.loc[
        store_bt["Model"] == "XGBoost"
    ]

    product_xgb = product_bt.loc[
        product_bt["model"] == "XGBoost"
    ]

    store_wape = (
        store_xgb["Absolute Error Sum"].sum()
        / store_xgb["Actual Units"].sum()
        * 100
    )

    product_wape = (
        product_xgb["absolute_error_sum"].sum()
        / product_xgb["actual_units"].sum()
        * 100
    )

    # -------------------------------------------------
    # KPI METRICS
    # -------------------------------------------------

    total_store_demand = int(
        store_forecast["predicted_units"].sum()
    )

    products_count = (
        product_forecast["item_id"].nunique()
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "28-Day Store Forecast",
        f"{total_store_demand:,} units"
    )

    c2.metric(
        "Products Forecasted",
        f"{products_count:,}"
    )

    c3.metric(
        "Store Model WAPE",
        f"{store_wape:.2f}%"
    )

    c4.metric(
        "Product Model WAPE",
        f"{product_wape:.2f}%"
    )

    st.caption(
        "Accuracy metrics are from historical "
        "rolling-origin backtesting."
    )

    st.divider()

    # -------------------------------------------------
    # FORECAST VISUALIZATIONS
    # -------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.subheader("28-Day Store Forecast")

        daily = store_forecast.sort_values(
            "date"
        ).set_index("date")

        st.line_chart(
            daily["predicted_units"]
        )

    with right:

        st.subheader("Top 10 Products by Forecast Demand")

        top10 = (
            demand_plan.sort_values(
                "predicted_28d_units",
                ascending=False
            )
            .head(10)
        )

        # STEP 29: HORIZONTAL PRODUCT CHART

        chart = (
            alt.Chart(top10)
            .mark_bar(
                color="#28B8A6",
                cornerRadiusEnd=4
            )
            .encode(
                x=alt.X(
                    "predicted_28d_units:Q",
                    title="Forecasted Units (28 Days)"
                ),
                y=alt.Y(
                    "item_id:N",
                    sort="-x",
                    title=None
                ),
                tooltip=[
                    alt.Tooltip(
                        "item_id:N",
                        title="Product"
                    ),
                    alt.Tooltip(
                        "predicted_28d_units:Q",
                        title="Predicted Units",
                        format=",.0f"
                    )
                ]
            )
            .properties(height=370)
        )

        st.altair_chart(
            chart,
            use_container_width=True
        )

    st.caption(
        "The product forecasts cover 20 selected items, "
        "not every product in the store. The separate "
        "store and product models are not reconciled."
    )

    st.divider()

    # -------------------------------------------------
    # INVENTORY RISK
    # -------------------------------------------------

    st.subheader("Simulated Inventory Risk")

    risk_counts = (
        inventory["risk_status"]
        .value_counts()
        .reindex(
            ["Critical", "Reorder Review", "Adequate"],
            fill_value=0
        )
    )

    r1, r2, r3 = st.columns(3)

    r1.metric(
        "Critical",
        int(risk_counts["Critical"])
    )

    r2.metric(
        "Reorder Review",
        int(risk_counts["Reorder Review"])
    )

    r3.metric(
        "Adequate",
        int(risk_counts["Adequate"])
    )

    st.bar_chart(risk_counts)

    st.warning(
        "Inventory-risk counts are based on simulated "
        "stock quantities and illustrative lead times, "
        "not verified operational inventory."
    )

    st.divider()

    st.subheader("Machine Learning Performance")

    st.write(
        "Both XGBoost forecasting models improved on "
        "their Seasonal Naive baselines during historical "
        "backtesting. Product-level demand remains "
        "substantially more uncertain than store demand."
    )

    st.caption(
        "Select the Model Performance tab to explore "
        "individual validation folds and error metrics."
    )
