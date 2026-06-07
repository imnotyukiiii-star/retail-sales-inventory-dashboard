"""
Create a step-by-step Jupyter notebook for the portfolio project.

The notebook is written for recruiters and internship interviewers. It explains
the business purpose behind each metric, not only the technical steps.
"""

from pathlib import Path

import nbformat as nbf


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks" / "retail_sales_inventory_analysis.ipynb"


def markdown_cell(text):
    """Create a markdown cell."""
    return nbf.v4.new_markdown_cell(text)


def code_cell(code):
    """Create a code cell."""
    return nbf.v4.new_code_cell(code)


def create_notebook():
    """Build the notebook content."""
    notebook = nbf.v4.new_notebook()

    notebook.cells = [
        markdown_cell(
            "# Retail Sales and Inventory Operations Analysis\n\n"
            "This notebook analyzes a simulated outdoor retail dataset at the store-date-product level. "
            "The goal is to identify sales drivers, inventory risks, product performance patterns, and operations recommendations.\n\n"
            "**Data transparency:** this dataset is simulated for portfolio demonstration. It is not real The North Face or VF Corporation data."
        ),
        markdown_cell(
            "## 1. Load Libraries and Data\n\n"
            "The analysis uses pandas for data work and matplotlib for clean portfolio charts."
        ),
        code_cell(
            "from pathlib import Path\n"
            "import pandas as pd\n"
            "import matplotlib.pyplot as plt\n\n"
            "PROJECT_ROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\n"
            "DATA_PATH = PROJECT_ROOT / 'data' / 'processed' / 'retail_sales_inventory_cleaned.csv'\n\n"
            "df = pd.read_csv(DATA_PATH, parse_dates=['date'])\n"
            "df.head()"
        ),
        markdown_cell(
            "## 2. Data Quality Checks\n\n"
            "Before analyzing performance, check whether the dataset has missing values, duplicate rows, and the right date format."
        ),
        code_cell(
            "print('Rows:', len(df))\n"
            "print('Columns:', len(df.columns))\n"
            "print('Duplicate rows:', df.duplicated().sum())\n"
            "print('Missing values:', df.isna().sum().sum())\n"
            "print('Date range:', df['date'].min().date(), 'to', df['date'].max().date())"
        ),
        markdown_cell(
            "## 3. Create Business Metrics\n\n"
            "These metrics translate raw sales and traffic data into business meaning:\n\n"
            "- **Revenue** shows sales dollars.\n"
            "- **Conversion rate** shows how effectively customer visits become transactions.\n"
            "- **Sell-through rate** shows how quickly inventory moves.\n"
            "- **Low-stock flag** highlights potential lost sales risk."
        ),
        code_cell(
            "df['revenue_check'] = df['units_sold'] * df['unit_price']\n"
            "df['conversion_rate_check'] = df['transactions'] / df['customer_visits']\n"
            "df['sell_through_rate_check'] = df['units_sold'] / df['starting_inventory']\n\n"
            "df[['revenue', 'revenue_check', 'conversion_rate', 'sell_through_rate', 'low_stock_flag']].head()"
        ),
        markdown_cell(
            "## 4. Executive KPI Snapshot\n\n"
            "These top-line metrics summarize the simulated retail business."
        ),
        code_cell(
            "total_revenue = df['revenue'].sum()\n"
            "total_units_sold = df['units_sold'].sum()\n"
            "total_transactions = df['transactions'].sum()\n"
            "total_customer_visits = df['customer_visits'].sum()\n"
            "average_order_value = total_revenue / total_transactions\n"
            "overall_conversion_rate = total_transactions / total_customer_visits\n\n"
            "kpi_snapshot = pd.DataFrame({\n"
            "    'Metric': ['Total Revenue', 'Total Units Sold', 'Average Order Value', 'Conversion Rate'],\n"
            "    'Value': [\n"
            "        f'${total_revenue:,.0f}',\n"
            "        f'{total_units_sold:,.0f}',\n"
            "        f'${average_order_value:,.0f}',\n"
            "        f'{overall_conversion_rate:.1%}'\n"
            "    ]\n"
            "})\n"
            "kpi_snapshot"
        ),
        markdown_cell(
            "## 5. Revenue by Month\n\n"
            "Monthly revenue helps identify seasonality and planning periods for inventory, promotions, and staffing."
        ),
        code_cell(
            "monthly_revenue = (\n"
            "    df.groupby('month', as_index=False)\n"
            "    .agg(revenue=('revenue', 'sum'), units_sold=('units_sold', 'sum'))\n"
            "    .sort_values('month')\n"
            ")\n\n"
            "plt.figure(figsize=(10, 5))\n"
            "plt.plot(monthly_revenue['month'], monthly_revenue['revenue'], marker='o', linewidth=2.5)\n"
            "plt.title('Monthly Revenue Trend')\n"
            "plt.xlabel('Month')\n"
            "plt.ylabel('Revenue')\n"
            "plt.xticks(rotation=45, ha='right')\n"
            "plt.grid(axis='y', alpha=0.25)\n"
            "plt.show()\n\n"
            "monthly_revenue.sort_values('revenue', ascending=False).head()"
        ),
        markdown_cell(
            "## 6. Product Category Performance\n\n"
            "Category-level revenue shows where the business earns most sales dollars. This supports merchandising and finance decisions."
        ),
        code_cell(
            "category_revenue = (\n"
            "    df.groupby('product_category', as_index=False)\n"
            "    .agg(revenue=('revenue', 'sum'), units_sold=('units_sold', 'sum'), average_sell_through_rate=('sell_through_rate', 'mean'))\n"
            "    .sort_values('revenue', ascending=False)\n"
            ")\n"
            "category_revenue"
        ),
        code_cell(
            "plt.figure(figsize=(9, 5))\n"
            "plt.barh(category_revenue.sort_values('revenue')['product_category'], category_revenue.sort_values('revenue')['revenue'])\n"
            "plt.title('Revenue by Product Category')\n"
            "plt.xlabel('Revenue')\n"
            "plt.ylabel('Product Category')\n"
            "plt.grid(axis='x', alpha=0.25)\n"
            "plt.show()"
        ),
        markdown_cell(
            "## 7. Product Ranking\n\n"
            "Product ranking identifies the items that drive revenue and the items that drive unit volume."
        ),
        code_cell(
            "top_products_by_revenue = (\n"
            "    df.groupby(['product_category', 'product_name'], as_index=False)\n"
            "    .agg(revenue=('revenue', 'sum'), units_sold=('units_sold', 'sum'), average_sell_through_rate=('sell_through_rate', 'mean'))\n"
            "    .sort_values('revenue', ascending=False)\n"
            ")\n"
            "top_products_by_revenue.head(10)"
        ),
        markdown_cell(
            "## 8. Inventory Risk and Low-Stock Products\n\n"
            "Low-stock products can create lost sales risk. This table shows which products and stores need replenishment attention."
        ),
        code_cell(
            "low_stock_watchlist = (\n"
            "    df[df['low_stock_flag']]\n"
            "    .groupby(['store_name', 'product_category', 'product_name'], as_index=False)\n"
            "    .agg(low_stock_days=('low_stock_flag', 'sum'), average_inventory_level=('inventory_level', 'mean'), units_sold=('units_sold', 'sum'), revenue=('revenue', 'sum'))\n"
            "    .sort_values(['low_stock_days', 'revenue'], ascending=[False, False])\n"
            ")\n"
            "low_stock_watchlist.head(10)"
        ),
        markdown_cell(
            "## 9. Store Performance\n\n"
            "Store-level performance connects revenue, traffic, conversion, and inventory risk. This supports operations and staffing decisions."
        ),
        code_cell(
            "store_performance = (\n"
            "    df.groupby(['store_id', 'store_name', 'region'], as_index=False)\n"
            "    .agg(revenue=('revenue', 'sum'), units_sold=('units_sold', 'sum'), transactions=('transactions', 'sum'), customer_visits=('customer_visits', 'sum'), low_stock_records=('low_stock_flag', 'sum'))\n"
            "    .sort_values('revenue', ascending=False)\n"
            ")\n"
            "store_performance['conversion_rate'] = store_performance['transactions'] / store_performance['customer_visits']\n"
            "store_performance"
        ),
        markdown_cell(
            "## 10. Business Recommendations\n\n"
            "1. **Increase stock for fast-moving low-stock items.** Accessories and base layers with repeated low-stock days should be reviewed weekly during peak seasons.\n"
            "2. **Protect premium outerwear inventory before winter.** Jackets generate the most revenue, so stock planning should happen before November and December.\n"
            "3. **Promote slow-moving premium products selectively.** Use targeted campaigns and bundles instead of broad markdowns.\n"
            "4. **Improve conversion through staffing.** Schedule more floor coverage during high-traffic periods and review lower-conversion stores for service gaps.\n"
            "5. **Reduce lost sales risk.** Use a store-product low-stock report to trigger replenishment before products reach stockout levels."
        ),
        markdown_cell(
            "## 11. Portfolio Takeaway\n\n"
            "This project demonstrates the ability to clean retail data, calculate business KPIs, identify product and inventory risks, and translate findings into practical recommendations for retail operations, merchandising, finance, and marketing."
        ),
    ]

    return notebook


def main():
    """Save the notebook file."""
    NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
    notebook = create_notebook()
    nbf.write(notebook, NOTEBOOK_PATH)
    print(f"Saved notebook to: {NOTEBOOK_PATH}")


if __name__ == "__main__":
    main()
