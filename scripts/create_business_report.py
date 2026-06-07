"""
Create the short business report for the retail operations project.

The report translates analysis outputs into practical recommendations for
retail operations, merchandising, finance, and marketing internship audiences.
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_PATH = PROJECT_ROOT / "reports" / "retail_operations_business_report.md"


def money(value):
    """Format numbers as dollar amounts."""
    return f"${float(value):,.0f}"


def percent(value, decimals=1):
    """Format decimal values as percentages."""
    return f"{float(value):.{decimals}%}"


def load_tables():
    """Load the processed tables needed for the report."""
    return {
        "overall": pd.read_csv(PROCESSED_DIR / "overall_metrics.csv"),
        "top_revenue": pd.read_csv(PROCESSED_DIR / "top_products_by_revenue.csv"),
        "top_units": pd.read_csv(PROCESSED_DIR / "top_products_by_units.csv"),
        "slow": pd.read_csv(PROCESSED_DIR / "slow_moving_products.csv"),
        "low_stock": pd.read_csv(PROCESSED_DIR / "low_stock_products.csv"),
        "category": pd.read_csv(PROCESSED_DIR / "revenue_by_category.csv"),
        "month": pd.read_csv(PROCESSED_DIR / "revenue_by_month.csv"),
        "store": pd.read_csv(PROCESSED_DIR / "store_performance.csv"),
    }


def markdown_table(df, columns, max_rows=5):
    """Create a compact markdown table from selected columns."""
    table = df.loc[:, columns].head(max_rows).copy()

    for column in table.columns:
        if "revenue" in column or column == "total_revenue":
            table[column] = table[column].apply(money)
        elif "rate" in column:
            table[column] = table[column].apply(lambda value: percent(value, decimals=2))
        elif table[column].dtype.kind in "if":
            table[column] = table[column].round(0).astype(int)

    header = "| " + " | ".join(table.columns) + " |"
    separator = "| " + " | ".join(["---"] * len(table.columns)) + " |"
    rows = []

    for _, row in table.iterrows():
        rows.append("| " + " | ".join(str(value) for value in row.values) + " |")

    return "\n".join([header, separator] + rows)


def create_report(tables):
    """Create a concise business report in markdown."""
    overall = tables["overall"].iloc[0]
    top_product = tables["top_revenue"].iloc[0]
    top_category = tables["category"].iloc[0]
    top_store = tables["store"].iloc[0]
    top_month = tables["month"].sort_values("revenue", ascending=False).iloc[0]
    lowest_store_conversion = tables["store"].sort_values("conversion_rate", ascending=True).iloc[0]

    report = f"""# Retail Sales and Inventory Operations Business Report

## Executive Summary

- **Jackets are the main revenue engine.** The category generated {money(top_category['revenue'])}, led by {top_product['product_name']}, the top product by revenue.
- **Inventory risk is concentrated in fast-moving smaller items.** The low-stock watchlist is led by accessories and base-layer products, which suggests replenishment should not focus only on high-ticket outerwear.
- **Denver Outdoor Flagship is the strongest revenue store.** It generated {money(top_store['revenue'])}, making it a useful benchmark for staffing, merchandising, and replenishment planning.
- **The business should balance premium revenue with operational availability.** High-price jackets drive revenue, while frequent low-stock products may create preventable lost sales.

## Business Context and Metric Definitions

This report uses a simulated store-date-product dataset for an outdoor retail business inspired by brands such as The North Face. It is not real The North Face or VF Corporation data.

- Total revenue measures sales dollars.
- Average order value measures revenue per transaction.
- Conversion rate measures transactions divided by customer visits.
- Sell-through rate measures units sold divided by starting inventory.
- Low-stock products are products with ending inventory at or below 20 units.

## Revenue Is Concentrated in Outerwear

The simulated business generated **{money(overall['total_revenue'])}** in revenue and sold **{int(overall['total_units_sold']):,}** units. The overall average order value was **{money(overall['average_order_value'])}**, while the conversion rate was **{percent(overall['conversion_rate'])}**.

The strongest revenue category was **{top_category['product_category']}**, which reflects the importance of premium outerwear in outdoor retail. The top revenue month was **{top_month['month']}**, with **{money(top_month['revenue'])}** in sales, showing the seasonal importance of winter demand.

![Monthly revenue trend](../outputs/figures/monthly_revenue_trend.png)

![Revenue by category](../outputs/figures/revenue_by_category.png)

Top products by revenue:

{markdown_table(tables['top_revenue'], ['product_name', 'product_category', 'revenue', 'units_sold', 'average_sell_through_rate'], 5)}

**So what:** Merchandising and finance teams should protect availability for premium outerwear before peak winter months because these products carry large revenue impact even when unit volume is lower than accessories.

## Fast-Moving Products Need Replenishment Attention

Low-stock risk appears most often in accessories and base layers. These products may not always have the highest price, but frequent low-stock days can create missed basket-building opportunities and customer frustration.

![Low-stock product table](../outputs/figures/low_stock_product_table.png)

Low-stock watchlist:

{markdown_table(tables['low_stock'], ['store_name', 'product_name', 'low_stock_days', 'average_inventory_level', 'total_units_sold', 'total_revenue'], 8)}

**Recommendation:** Increase replenishment frequency for Summit Beanie, Trail Gloves, Insulated Bottle, and Thermal Crew Base Layer in stores with repeated low-stock days. These products should be reviewed weekly during colder months.

## Slow-Moving Products Need Targeted Promotion, Not Blanket Discounting

Some premium products generate high revenue but have lower average sell-through rates. This means they are valuable, but inventory may move more slowly because of price point, seasonality, or customer consideration time.

Slow-moving product candidates:

{markdown_table(tables['slow'], ['product_name', 'product_category', 'revenue', 'units_sold', 'average_inventory_level', 'average_sell_through_rate'], 5)}

**Recommendation:** Avoid broad markdowns on high-revenue outerwear. Instead, use targeted promotions, bundle offers, improved in-store placement, and seasonal messaging. For example, pair premium jackets with accessories during winter campaigns to protect margin while increasing basket size.

## Store Operations Should Use Traffic and Conversion Together

The top revenue store was **{top_store['store_name']}**, while **{lowest_store_conversion['store_name']}** had the lowest conversion rate among stores in the simulation. Store planning should look at both traffic and conversion because high visits without enough transactions may point to staffing, product availability, or merchandising issues.

Store performance:

{markdown_table(tables['store'], ['store_name', 'region', 'revenue', 'units_sold', 'customer_visits', 'conversion_rate', 'low_stock_records'], 5)}

**Recommendation:** Schedule more floor coverage during high-traffic periods, especially weekends and winter months. Stores with lower conversion should review checkout wait times, fitting room support, product availability, and sales associate coverage.

## Business Recommendations

1. **Increase stock for fast-moving low-stock items.** Prioritize accessories and base layers with repeated low-stock days, especially in Denver, Boston, Seattle, and San Francisco.
2. **Protect inventory for premium outerwear before winter peaks.** Jackets are the top revenue category, so replenishment planning should start before November and December.
3. **Promote slow-moving premium products selectively.** Use targeted campaigns, bundles, and visual merchandising rather than large blanket discounts that could reduce margin.
4. **Improve conversion through staffing and in-store support.** Align staff schedules with high customer visit periods and review low-conversion stores for service or availability issues.
5. **Reduce lost sales from stockouts.** Create a weekly low-stock report by store and product, then trigger replenishment when inventory drops near the low-stock threshold.

## Further Questions

- Which stores have the highest lost-sales risk during peak winter months?
- Do promoted products produce enough incremental revenue to justify discount cost?
- Which product categories have the best margin, not only the highest revenue?
- Are conversion rates lower during high-traffic periods because of staffing constraints?

## Caveats and Assumptions

- The dataset is simulated for portfolio demonstration and is not real company data.
- Product margin and discount depth are not included, so profit recommendations are directional.
- Customer visits are estimated at the product or category level for analysis purposes.
- Low-stock risk is based on ending inventory and does not directly measure actual stockouts or lost sales.
"""

    return report


def main():
    """Create and save the business report."""
    tables = load_tables()
    report = create_report(tables)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Saved business report to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
