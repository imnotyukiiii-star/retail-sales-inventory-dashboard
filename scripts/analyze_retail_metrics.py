"""
Analyze retail sales, inventory, and operations metrics.

This script creates business-friendly metric tables that can be used in the
README, charts, dashboard, and final business report.
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "retail_sales_inventory_cleaned.csv"
OUTPUT_DATA_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_PATH = PROJECT_ROOT / "reports" / "key_metrics_summary.md"


def load_cleaned_data():
    """Load the cleaned retail dataset."""
    return pd.read_csv(PROCESSED_DATA_PATH, parse_dates=["date"])


def calculate_overall_metrics(df):
    """Calculate high-level business KPIs."""
    total_revenue = df["revenue"].sum()
    total_units_sold = df["units_sold"].sum()
    total_transactions = df["transactions"].sum()
    total_customer_visits = df["customer_visits"].sum()

    metrics = {
        "total_revenue": total_revenue,
        "total_units_sold": total_units_sold,
        "average_order_value": total_revenue / total_transactions,
        "conversion_rate": total_transactions / total_customer_visits,
        "total_transactions": total_transactions,
        "total_customer_visits": total_customer_visits,
    }

    return pd.DataFrame([metrics])


def create_metric_tables(df):
    """Create detailed metric tables for portfolio analysis."""
    top_products_by_revenue = (
        df.groupby("product_name", as_index=False)
        .agg(
            product_category=("product_category", "first"),
            revenue=("revenue", "sum"),
            units_sold=("units_sold", "sum"),
            average_sell_through_rate=("sell_through_rate", "mean"),
        )
        .sort_values("revenue", ascending=False)
        .head(10)
    )

    top_products_by_units = (
        df.groupby("product_name", as_index=False)
        .agg(
            product_category=("product_category", "first"),
            units_sold=("units_sold", "sum"),
            revenue=("revenue", "sum"),
        )
        .sort_values("units_sold", ascending=False)
        .head(10)
    )

    product_performance = (
        df.groupby(["product_category", "product_name"], as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            units_sold=("units_sold", "sum"),
            average_inventory_level=("inventory_level", "mean"),
            average_sell_through_rate=("sell_through_rate", "mean"),
            promotion_rate=("promotion_flag", "mean"),
        )
    )

    slow_moving_products = (
        product_performance.sort_values(["average_sell_through_rate", "units_sold"], ascending=[True, True])
        .head(10)
    )

    low_stock_products = (
        df[df["low_stock_flag"]]
        .groupby(["store_id", "store_name", "product_category", "product_name"], as_index=False)
        .agg(
            low_stock_days=("low_stock_flag", "sum"),
            average_inventory_level=("inventory_level", "mean"),
            total_units_sold=("units_sold", "sum"),
            total_revenue=("revenue", "sum"),
        )
        .sort_values(["low_stock_days", "total_revenue"], ascending=[False, False])
        .head(20)
    )

    revenue_by_category = (
        df.groupby("product_category", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            units_sold=("units_sold", "sum"),
            average_sell_through_rate=("sell_through_rate", "mean"),
        )
        .sort_values("revenue", ascending=False)
    )

    revenue_by_month = (
        df.groupby("month", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            units_sold=("units_sold", "sum"),
            transactions=("transactions", "sum"),
            customer_visits=("customer_visits", "sum"),
        )
        .sort_values("month")
    )
    revenue_by_month["conversion_rate"] = (
        revenue_by_month["transactions"] / revenue_by_month["customer_visits"]
    )

    store_performance = (
        df.groupby(["store_id", "store_name", "region"], as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            units_sold=("units_sold", "sum"),
            transactions=("transactions", "sum"),
            customer_visits=("customer_visits", "sum"),
            low_stock_records=("low_stock_flag", "sum"),
        )
        .sort_values("revenue", ascending=False)
    )
    store_performance["conversion_rate"] = (
        store_performance["transactions"] / store_performance["customer_visits"]
    )

    return {
        "top_products_by_revenue": top_products_by_revenue,
        "top_products_by_units": top_products_by_units,
        "slow_moving_products": slow_moving_products,
        "low_stock_products": low_stock_products,
        "revenue_by_category": revenue_by_category,
        "revenue_by_month": revenue_by_month,
        "store_performance": store_performance,
    }


def save_tables(overall_metrics, metric_tables):
    """Save metric tables as Excel-compatible CSV files."""
    overall_metrics.to_csv(OUTPUT_DATA_DIR / "overall_metrics.csv", index=False)

    for table_name, table in metric_tables.items():
        table.to_csv(OUTPUT_DATA_DIR / f"{table_name}.csv", index=False)


def money(value):
    """Format a number as a simple dollar amount."""
    return f"${value:,.0f}"


def percent(value):
    """Format a decimal as a percentage."""
    return f"{value:.1%}"


def create_report(overall_metrics, metric_tables):
    """Create a concise business summary in markdown."""
    metrics = overall_metrics.iloc[0]
    top_product = metric_tables["top_products_by_revenue"].iloc[0]
    top_category = metric_tables["revenue_by_category"].iloc[0]
    top_store = metric_tables["store_performance"].iloc[0]

    report_lines = [
        "# Key Metrics Summary",
        "",
        "## Executive Snapshot",
        "",
        f"- Total revenue: {money(metrics['total_revenue'])}",
        f"- Total units sold: {int(metrics['total_units_sold']):,}",
        f"- Average order value: {money(metrics['average_order_value'])}",
        f"- Overall conversion rate: {percent(metrics['conversion_rate'])}",
        f"- Total transactions: {int(metrics['total_transactions']):,}",
        f"- Total customer visits: {int(metrics['total_customer_visits']):,}",
        "",
        "## Key Findings",
        "",
        f"- Top revenue product: {top_product['product_name']} with {money(top_product['revenue'])} in revenue.",
        f"- Top revenue category: {top_category['product_category']} with {money(top_category['revenue'])} in revenue.",
        f"- Top store by revenue: {top_store['store_name']} with {money(top_store['revenue'])} in revenue.",
        "- Slow-moving products are identified using low average sell-through rate and lower unit sales.",
        "- Low-stock products are identified by the number of days ending inventory was at or below the threshold.",
        "",
        "## Business Meaning",
        "",
        "These metrics help a retail operations team understand where revenue is coming from, which products may need replenishment, "
        "which products may need promotion, and where customer traffic is not converting into purchases efficiently.",
    ]

    return "\n".join(report_lines)


def main():
    """Run the full metric analysis workflow."""
    df = load_cleaned_data()

    overall_metrics = calculate_overall_metrics(df)
    metric_tables = create_metric_tables(df)

    save_tables(overall_metrics, metric_tables)
    REPORT_PATH.write_text(create_report(overall_metrics, metric_tables), encoding="utf-8")

    print("Saved overall metrics and detailed metric tables.")
    print(f"Saved key metrics summary to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
