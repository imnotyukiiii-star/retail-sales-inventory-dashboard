# Data Dictionary

Dataset: `retail_sales_inventory_simulated.csv`

This dataset is simulated for portfolio demonstration. It is not real company data.

| Column | Meaning |
| --- | --- |
| `date` | Business date for the sales and inventory record |
| `store_id` | Unique store identifier |
| `store_name` | Store name used for analysis and reporting |
| `region` | Geographic region of the store |
| `product_category` | Product category, such as Jackets, Fleece, or Backpacks |
| `product_name` | Product name |
| `units_sold` | Number of units sold for that product in that store on that date |
| `unit_price` | Selling price per unit |
| `revenue` | Sales revenue, calculated as units sold multiplied by unit price |
| `starting_inventory` | Estimated beginning inventory for that product in that store on that date |
| `inventory_level` | Ending inventory after daily units sold |
| `customer_visits` | Estimated product- or category-related customer visits for that store day |
| `transactions` | Number of purchase transactions related to the product |
| `promotion_flag` | Whether the product was promoted on that date |

## Business Notes

- The data is created at the store-date-product level.
- Seasonality is included so winter products sell more in colder months.
- Weekend traffic is slightly higher than weekday traffic.
- Promotions increase expected product demand.
- Inventory levels are intentionally imperfect so the project can identify low-stock and stockout-risk products.

