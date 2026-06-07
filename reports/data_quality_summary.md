# Data Quality Summary

Dataset: `data/processed/retail_sales_inventory_cleaned.csv`

## Cleaning Checks

- Raw rows: 25,550
- Cleaned rows: 25,550
- Duplicate rows found in raw data: 0
- Missing values found in raw data: 0

## Missing Values by Column

| Column | Missing Values |
| --- | ---: |
| `date` | 0 |
| `store_id` | 0 |
| `store_name` | 0 |
| `region` | 0 |
| `product_category` | 0 |
| `product_name` | 0 |
| `units_sold` | 0 |
| `unit_price` | 0 |
| `revenue` | 0 |
| `starting_inventory` | 0 |
| `inventory_level` | 0 |
| `customer_visits` | 0 |
| `transactions` | 0 |
| `promotion_flag` | 0 |

## Created Business Metrics

- `conversion_rate` = transactions / customer visits
- `sell_through_rate` = units sold / starting inventory
- `low_stock_flag` = inventory level <= 20
- `month` = monthly period used for trend analysis

## Business Meaning

The cleaned dataset is ready for sales, merchandising, inventory, and store operations analysis. The added metrics help compare product performance, identify replenishment needs, and evaluate how effectively stores convert customer traffic into purchases.