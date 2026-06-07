"""
Generate a simulated retail sales and inventory dataset.

This script creates store-level retail operations data for an outdoor apparel
business. The product mix is inspired by outdoor retail brands, but the data is
fully simulated for portfolio demonstration.
"""

from pathlib import Path
import random

import pandas as pd


# A fixed random seed makes the dataset reproducible.
random.seed(42)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "retail_sales_inventory_simulated.csv"


stores = [
    {"store_id": "S001", "store_name": "Denver Outdoor Flagship", "region": "Mountain"},
    {"store_id": "S002", "store_name": "Seattle Trail Store", "region": "Pacific Northwest"},
    {"store_id": "S003", "store_name": "Boston Winter Gear", "region": "Northeast"},
    {"store_id": "S004", "store_name": "Chicago Urban Outdoor", "region": "Midwest"},
    {"store_id": "S005", "store_name": "San Francisco Summit", "region": "West Coast"},
]


products = [
    {"category": "Jackets", "product_name": "Summit Waterproof Shell", "unit_price": 329, "base_demand": 8},
    {"category": "Jackets", "product_name": "Alpine Down Parka", "unit_price": 399, "base_demand": 7},
    {"category": "Jackets", "product_name": "Trail Rain Jacket", "unit_price": 189, "base_demand": 10},
    {"category": "Fleece", "product_name": "Canyon Fleece Pullover", "unit_price": 89, "base_demand": 15},
    {"category": "Fleece", "product_name": "Mountain Zip Hoodie", "unit_price": 119, "base_demand": 13},
    {"category": "Backpacks", "product_name": "Boreal Daypack 28L", "unit_price": 99, "base_demand": 12},
    {"category": "Backpacks", "product_name": "Expedition Duffel 60L", "unit_price": 149, "base_demand": 9},
    {"category": "Footwear", "product_name": "Ridge Hiking Boot", "unit_price": 159, "base_demand": 11},
    {"category": "Footwear", "product_name": "Trail Runner Shoe", "unit_price": 129, "base_demand": 14},
    {"category": "Base Layers", "product_name": "Thermal Crew Base Layer", "unit_price": 69, "base_demand": 16},
    {"category": "Base Layers", "product_name": "Merino Trek Legging", "unit_price": 79, "base_demand": 12},
    {"category": "Accessories", "product_name": "Summit Beanie", "unit_price": 34, "base_demand": 20},
    {"category": "Accessories", "product_name": "Trail Gloves", "unit_price": 44, "base_demand": 18},
    {"category": "Accessories", "product_name": "Insulated Bottle", "unit_price": 29, "base_demand": 17},
]


def get_season_factor(month, category):
    """Return a demand multiplier based on month and product category."""
    winter_months = [11, 12, 1, 2]
    spring_months = [3, 4, 5]
    summer_months = [6, 7, 8]

    if category in ["Jackets", "Fleece", "Base Layers"] and month in winter_months:
        return 1.6
    if category in ["Backpacks", "Footwear"] and month in spring_months + summer_months:
        return 1.4
    if category == "Accessories" and month in winter_months:
        return 1.3
    return 1.0


def get_store_factor(store_id):
    """Return a demand multiplier for each store."""
    store_factors = {
        "S001": 1.20,
        "S002": 1.10,
        "S003": 1.15,
        "S004": 0.90,
        "S005": 1.05,
    }
    return store_factors[store_id]


def create_dataset():
    """Create the simulated retail dataset and return it as a DataFrame."""
    dates = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
    rows = []

    for date in dates:
        is_weekend = date.weekday() >= 5
        month = date.month

        for store in stores:
            # Customer visits are tracked at the store-day level.
            base_visits = random.randint(180, 420)
            weekend_boost = 1.25 if is_weekend else 1.0
            customer_visits = int(base_visits * weekend_boost * get_store_factor(store["store_id"]))

            for product in products:
                promotion_flag = random.random() < 0.18
                promotion_factor = 1.25 if promotion_flag else 1.0
                season_factor = get_season_factor(month, product["category"])
                store_factor = get_store_factor(store["store_id"])

                expected_units = product["base_demand"] * season_factor * store_factor * promotion_factor
                noise = random.uniform(0.65, 1.35)
                units_sold = max(0, int(expected_units * noise))

                # Starting inventory is intentionally imperfect so low-stock situations appear.
                starting_inventory = random.randint(35, 180)
                inventory_level = max(0, starting_inventory - units_sold)

                # Transactions are related to units sold, but not identical.
                transactions = max(1, int(units_sold / random.uniform(1.1, 2.3)))
                transactions = min(transactions, customer_visits)

                revenue = units_sold * product["unit_price"]

                rows.append(
                    {
                        "date": date.strftime("%Y-%m-%d"),
                        "store_id": store["store_id"],
                        "store_name": store["store_name"],
                        "region": store["region"],
                        "product_category": product["category"],
                        "product_name": product["product_name"],
                        "units_sold": units_sold,
                        "unit_price": product["unit_price"],
                        "revenue": revenue,
                        "starting_inventory": starting_inventory,
                        "inventory_level": inventory_level,
                        "customer_visits": customer_visits,
                        "transactions": transactions,
                        "promotion_flag": promotion_flag,
                    }
                )

    return pd.DataFrame(rows)


def main():
    """Generate and save the simulated raw dataset."""
    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    dataset = create_dataset()
    dataset.to_csv(RAW_DATA_PATH, index=False)

    print(f"Saved simulated dataset to: {RAW_DATA_PATH}")
    print(f"Rows: {len(dataset):,}")
    print(f"Columns: {len(dataset.columns)}")


if __name__ == "__main__":
    main()
