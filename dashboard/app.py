"""
Streamlit dashboard for the Retail Sales and Inventory Operations project.

Run from the project root with:
streamlit run dashboard/app.py
"""

from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "retail_sales_inventory_cleaned.csv"


st.set_page_config(
    page_title="Retail Sales and Inventory Operations Dashboard",
    layout="wide",
)


@st.cache_data
def load_data():
    """Load cleaned data once so the dashboard stays fast."""
    data = pd.read_csv(DATA_PATH, parse_dates=["date"])
    return data


def format_dollars(value):
    """Format numbers as business-friendly dollar amounts."""
    return f"${value:,.0f}"


def format_percent(value):
    """Format decimal rates as percentages."""
    return f"{value:.1%}"


def filter_data(data, selected_categories, selected_stores, start_date, end_date):
    """Apply sidebar filters to the dataset."""
    filtered = data[
        (data["product_category"].isin(selected_categories))
        & (data["store_name"].isin(selected_stores))
        & (data["date"].dt.date >= start_date)
        & (data["date"].dt.date <= end_date)
    ]
    return filtered


def show_kpis(data):
    """Show high-level KPI cards for the selected data."""
    total_revenue = data["revenue"].sum()
    total_units = data["units_sold"].sum()
    total_transactions = data["transactions"].sum()
    total_visits = data["customer_visits"].sum()
    average_order_value = total_revenue / total_transactions if total_transactions else 0
    conversion_rate = total_transactions / total_visits if total_visits else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", format_dollars(total_revenue))
    col2.metric("Units Sold", f"{total_units:,.0f}")
    col3.metric("Average Order Value", format_dollars(average_order_value))
    col4.metric("Conversion Rate", format_percent(conversion_rate))


def show_revenue_trend(data):
    """Display monthly revenue trend for the selected data."""
    monthly_revenue = (
        data.groupby("month", as_index=False)
        .agg(revenue=("revenue", "sum"))
        .sort_values("month")
    )
    monthly_revenue = monthly_revenue.set_index("month")

    st.subheader("Monthly Revenue Trend")
    st.line_chart(monthly_revenue["revenue"])
    st.caption("Business meaning: this trend helps identify seasonality and months that may need stronger inventory planning or marketing support.")


def show_product_ranking(data):
    """Display product ranking table by revenue."""
    product_ranking = (
        data.groupby(["product_category", "product_name"], as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            units_sold=("units_sold", "sum"),
            average_sell_through_rate=("sell_through_rate", "mean"),
        )
        .sort_values("revenue", ascending=False)
    )

    product_ranking["revenue"] = product_ranking["revenue"].round(0)
    product_ranking["average_sell_through_rate"] = product_ranking["average_sell_through_rate"].round(3)

    st.subheader("Product Ranking")
    st.dataframe(product_ranking.head(15), use_container_width=True)
    st.caption("Business meaning: high-revenue and high-sell-through products are candidates for stronger replenishment and display priority.")


def show_inventory_warnings(data):
    """Display products and stores with frequent low-stock records."""
    inventory_warning = (
        data[data["low_stock_flag"]]
        .groupby(["store_id", "store_name", "product_category", "product_name"], as_index=False)
        .agg(
            low_stock_days=("low_stock_flag", "sum"),
            average_inventory_level=("inventory_level", "mean"),
            units_sold=("units_sold", "sum"),
            revenue=("revenue", "sum"),
        )
        .sort_values(["low_stock_days", "revenue"], ascending=[False, False])
    )

    inventory_warning["average_inventory_level"] = inventory_warning["average_inventory_level"].round(1)
    inventory_warning["revenue"] = inventory_warning["revenue"].round(0)

    st.subheader("Inventory Warning Table")
    st.dataframe(inventory_warning.head(20), use_container_width=True)
    st.caption("Business meaning: frequent low-stock days may signal lost sales risk and should be reviewed for replenishment.")


def show_store_performance(data):
    """Display store-level operations performance."""
    store_performance = (
        data.groupby(["store_id", "store_name", "region"], as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            customer_visits=("customer_visits", "sum"),
            transactions=("transactions", "sum"),
            low_stock_records=("low_stock_flag", "sum"),
        )
        .sort_values("revenue", ascending=False)
    )
    store_performance["conversion_rate"] = store_performance["transactions"] / store_performance["customer_visits"]
    store_performance["conversion_rate"] = store_performance["conversion_rate"].round(3)
    store_performance["revenue"] = store_performance["revenue"].round(0)

    st.subheader("Store Performance")
    st.dataframe(store_performance, use_container_width=True)
    st.caption("Business meaning: store-level traffic, conversion, and stock warnings support staffing and operations decisions.")


def main():
    """Build the dashboard page."""
    data = load_data()

    st.title("Retail Sales and Inventory Operations Dashboard")
    st.write("Simulated outdoor retail dataset for portfolio demonstration. Not real The North Face or VF Corporation data.")

    with st.sidebar:
        st.header("Filters")

        categories = sorted(data["product_category"].unique())
        stores = sorted(data["store_name"].unique())

        selected_categories = st.multiselect("Product Category", categories, default=categories)
        selected_stores = st.multiselect("Store", stores, default=stores)

        min_date = data["date"].min().date()
        max_date = data["date"].max().date()
        selected_date_range = st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

        if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
            start_date, end_date = selected_date_range
        else:
            start_date = min_date
            end_date = max_date

    filtered_data = filter_data(data, selected_categories, selected_stores, start_date, end_date)

    if filtered_data.empty:
        st.warning("No data matches the selected filters.")
        return

    show_kpis(filtered_data)
    show_revenue_trend(filtered_data)

    left_column, right_column = st.columns(2)
    with left_column:
        show_product_ranking(filtered_data)
    with right_column:
        show_inventory_warnings(filtered_data)

    show_store_performance(filtered_data)


if __name__ == "__main__":
    main()
