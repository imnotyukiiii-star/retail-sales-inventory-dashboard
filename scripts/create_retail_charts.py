"""
Create clean portfolio charts for the retail operations project.

The charts are designed to support business storytelling in the README,
dashboard, and final report.
"""

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Keep matplotlib cache inside the project so the script runs cleanly.
os.environ["MPLCONFIGDIR"] = str(PROJECT_ROOT / ".matplotlib_cache")

import matplotlib.pyplot as plt
import pandas as pd


PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "retail_sales_inventory_cleaned.csv"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"


CHART_COLOR = "#2F5597"
ACCENT_COLOR = "#70AD47"
WARNING_COLOR = "#C00000"
NEUTRAL_COLOR = "#595959"


def load_data():
    """Load the cleaned retail dataset."""
    return pd.read_csv(PROCESSED_DATA_PATH, parse_dates=["date"])


def save_chart(filename):
    """Save the current matplotlib chart with consistent settings."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / filename
    plt.tight_layout()
    plt.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close()
    print(f"Saved chart: {output_path}")


def format_dollars(axis):
    """Format y-axis labels as dollar amounts in millions."""
    axis.set_major_formatter(lambda value, _: f"${value / 1_000_000:.1f}M")


def create_monthly_revenue_trend(df):
    """Create a monthly revenue trend line chart."""
    monthly = (
        df.groupby("month", as_index=False)
        .agg(revenue=("revenue", "sum"))
        .sort_values("month")
    )

    plt.figure(figsize=(10, 5))
    plt.plot(monthly["month"], monthly["revenue"], marker="o", linewidth=2.5, color=CHART_COLOR)
    plt.title("Monthly Revenue Trend", fontsize=15, weight="bold")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    format_dollars(plt.gca().yaxis)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", alpha=0.25)
    save_chart("monthly_revenue_trend.png")


def create_revenue_by_category(df):
    """Create a bar chart showing revenue by product category."""
    category = (
        df.groupby("product_category", as_index=False)
        .agg(revenue=("revenue", "sum"))
        .sort_values("revenue", ascending=True)
    )

    plt.figure(figsize=(9, 5))
    plt.barh(category["product_category"], category["revenue"], color=CHART_COLOR)
    plt.title("Revenue by Product Category", fontsize=15, weight="bold")
    plt.xlabel("Revenue")
    plt.ylabel("Product Category")
    format_dollars(plt.gca().xaxis)
    plt.grid(axis="x", alpha=0.25)
    save_chart("revenue_by_category.png")


def create_top_products_by_revenue(df):
    """Create a horizontal bar chart for the top 10 products by revenue."""
    top_products = (
        df.groupby("product_name", as_index=False)
        .agg(revenue=("revenue", "sum"))
        .sort_values("revenue", ascending=False)
        .head(10)
        .sort_values("revenue", ascending=True)
    )

    plt.figure(figsize=(10, 6))
    plt.barh(top_products["product_name"], top_products["revenue"], color=ACCENT_COLOR)
    plt.title("Top 10 Products by Revenue", fontsize=15, weight="bold")
    plt.xlabel("Revenue")
    plt.ylabel("Product")
    format_dollars(plt.gca().xaxis)
    plt.grid(axis="x", alpha=0.25)
    save_chart("top_10_products_by_revenue.png")


def create_conversion_rate_trend(df):
    """Create a monthly conversion rate trend chart."""
    monthly = (
        df.groupby("month", as_index=False)
        .agg(transactions=("transactions", "sum"), customer_visits=("customer_visits", "sum"))
        .sort_values("month")
    )
    monthly["conversion_rate"] = monthly["transactions"] / monthly["customer_visits"]

    plt.figure(figsize=(10, 5))
    plt.plot(monthly["month"], monthly["conversion_rate"], marker="o", linewidth=2.5, color=NEUTRAL_COLOR)
    plt.title("Monthly Conversion Rate Trend", fontsize=15, weight="bold")
    plt.xlabel("Month")
    plt.ylabel("Conversion Rate")
    plt.gca().yaxis.set_major_formatter(lambda value, _: f"{value:.1%}")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", alpha=0.25)
    save_chart("conversion_rate_trend.png")


def create_inventory_vs_units_sold(df):
    """Create a scatter chart comparing average inventory and units sold by product."""
    product_summary = (
        df.groupby("product_name", as_index=False)
        .agg(
            average_inventory_level=("inventory_level", "mean"),
            units_sold=("units_sold", "sum"),
            product_category=("product_category", "first"),
        )
    )

    plt.figure(figsize=(9, 6))
    plt.scatter(
        product_summary["average_inventory_level"],
        product_summary["units_sold"],
        s=90,
        color=CHART_COLOR,
        alpha=0.75,
    )

    for _, row in product_summary.iterrows():
        plt.annotate(
            row["product_name"],
            (row["average_inventory_level"], row["units_sold"]),
            fontsize=8,
            xytext=(5, 4),
            textcoords="offset points",
        )

    plt.title("Inventory Level vs Units Sold", fontsize=15, weight="bold")
    plt.xlabel("Average Inventory Level")
    plt.ylabel("Total Units Sold")
    plt.grid(alpha=0.25)
    save_chart("inventory_level_vs_units_sold.png")


def create_low_stock_table(df):
    """Create a visual table of products with the most low-stock days."""
    low_stock = (
        df[df["low_stock_flag"]]
        .groupby(["store_name", "product_name"], as_index=False)
        .agg(low_stock_days=("low_stock_flag", "sum"), total_units_sold=("units_sold", "sum"))
        .sort_values(["low_stock_days", "total_units_sold"], ascending=[False, False])
        .head(8)
    )

    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.axis("off")
    ax.set_title("Low-Stock Product Watchlist", fontsize=15, weight="bold", pad=18)

    table = ax.table(
        cellText=low_stock.values,
        colLabels=["Store", "Product", "Low-Stock Days", "Units Sold"],
        cellLoc="left",
        colLoc="left",
        loc="center",
    )

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.5)

    for (row, column), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight="bold", color="white")
            cell.set_facecolor(WARNING_COLOR)
        else:
            cell.set_facecolor("#F7F7F7" if row % 2 else "white")

    save_chart("low_stock_product_table.png")


def main():
    """Create all charts for the portfolio project."""
    df = load_data()

    create_monthly_revenue_trend(df)
    create_revenue_by_category(df)
    create_top_products_by_revenue(df)
    create_conversion_rate_trend(df)
    create_inventory_vs_units_sold(df)
    create_low_stock_table(df)


if __name__ == "__main__":
    main()
