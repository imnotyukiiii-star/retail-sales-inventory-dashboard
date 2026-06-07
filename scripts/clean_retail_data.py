"""
Clean the simulated retail sales and inventory dataset.

This script checks data quality, creates business metrics, and saves an
analysis-ready CSV file for charts, reports, and the Streamlit dashboard.
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "retail_sales_inventory_simulated.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "retail_sales_inventory_cleaned.csv"
QUALITY_REPORT_PATH = PROJECT_ROOT / "reports" / "data_quality_summary.md"


LOW_STOCK_THRESHOLD = 20


def load_raw_data():
    """Load the raw simulated retail dataset."""
    return pd.read_csv(RAW_DATA_PATH)


def clean_data(df):
    """Clean the dataset and create business metrics."""
    cleaned = df.copy()

    # Convert the date column so pandas can group by month and filter date ranges.
    cleaned["date"] = pd.to_datetime(cleaned["date"])

    # Remove duplicate rows if any exist.
    cleaned = cleaned.drop_duplicates()

    # Revenue should equal units sold multiplied by unit price.
    # Recalculate it to make the metric consistent for analysis.
    cleaned["revenue"] = cleaned["units_sold"] * cleaned["unit_price"]

    # Conversion rate measures how effectively visits turn into purchases.
    cleaned["conversion_rate"] = cleaned["transactions"] / cleaned["customer_visits"]

    # Sell-through rate measures how much starting inventory was sold.
    cleaned["sell_through_rate"] = cleaned["units_sold"] / cleaned["starting_inventory"]

    # Low-stock flag helps identify products that may need replenishment.
    cleaned["low_stock_flag"] = cleaned["inventory_level"] <= LOW_STOCK_THRESHOLD

    # Month is useful for trend charts and seasonal sales analysis.
    cleaned["month"] = cleaned["date"].dt.to_period("M").astype(str)

    return cleaned


def create_quality_summary(raw_df, cleaned_df):
    """Create a beginner-friendly data quality summary."""
    missing_values = raw_df.isna().sum()
    duplicate_rows = raw_df.duplicated().sum()

    summary_lines = [
        "# Data Quality Summary",
        "",
        "Dataset: `data/processed/retail_sales_inventory_cleaned.csv`",
        "",
        "## Cleaning Checks",
        "",
        f"- Raw rows: {len(raw_df):,}",
        f"- Cleaned rows: {len(cleaned_df):,}",
        f"- Duplicate rows found in raw data: {duplicate_rows:,}",
        f"- Missing values found in raw data: {int(missing_values.sum()):,}",
        "",
        "## Missing Values by Column",
        "",
        "| Column | Missing Values |",
        "| --- | ---: |",
    ]

    for column, value in missing_values.items():
        summary_lines.append(f"| `{column}` | {int(value):,} |")

    summary_lines.extend(
        [
            "",
            "## Created Business Metrics",
            "",
            "- `conversion_rate` = transactions / customer visits",
            "- `sell_through_rate` = units sold / starting inventory",
            f"- `low_stock_flag` = inventory level <= {LOW_STOCK_THRESHOLD}",
            "- `month` = monthly period used for trend analysis",
            "",
            "## Business Meaning",
            "",
            "The cleaned dataset is ready for sales, merchandising, inventory, and store operations analysis. "
            "The added metrics help compare product performance, identify replenishment needs, and evaluate how effectively stores convert customer traffic into purchases.",
        ]
    )

    return "\n".join(summary_lines)


def main():
    """Run the full cleaning workflow."""
    raw_df = load_raw_data()
    cleaned_df = clean_data(raw_df)

    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUALITY_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    cleaned_df.to_csv(PROCESSED_DATA_PATH, index=False)
    QUALITY_REPORT_PATH.write_text(create_quality_summary(raw_df, cleaned_df), encoding="utf-8")

    print(f"Saved cleaned dataset to: {PROCESSED_DATA_PATH}")
    print(f"Saved data quality summary to: {QUALITY_REPORT_PATH}")
    print(f"Cleaned rows: {len(cleaned_df):,}")
    print(f"Cleaned columns: {len(cleaned_df.columns)}")


if __name__ == "__main__":
    main()
