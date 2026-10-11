"""
Exercise 8: Joins + Window Functions (pandas)
See README.md in this folder for the full task description.

Fill in the functions below. Run with:
    python exercise_pandas.py
"""

import pandas as pd

ORDERS_FILE = "orders_clean.csv"
REGIONS_FILE = "regions_lookup.csv"


def load_data():
    orders = pd.read_csv(ORDERS_FILE, parse_dates=["order_date"])
    regions = pd.read_csv(REGIONS_FILE)
    return orders, regions


def join_orders_with_regions(orders, regions):
    """Left-join orders with the regions lookup table on region."""
    orders_regions_df = orders.merge(regions, on="region", how="left")
    return orders_regions_df


def add_region_rank(df):
    """Add region_rank: rank of each order by total (desc), within its region."""
    df["region_rank"] = (df.groupby("region")["total"].rank(method="min", ascending=False))
    return df


def add_running_total(df):
    """Add running_total: cumulative sum of total within each region, ordered by order_date."""
    df = df.sort_values(["region", "order_date"])
    df["running_total"] = (df.groupby("region")["total"].cumsum())
    return df


def top_order_per_region(df):
    """Return just the rank-1 order per region, with regional_manager attached."""
    df = df[df["region_rank"] == 1][["order_id", "customer_name", "total", "region", "regional_manager"]]
    return df


def main():
    orders, regions = load_data()
    df = join_orders_with_regions(orders, regions)
    df = add_region_rank(df)
    df = add_running_total(df)
    print(df)

    top = top_order_per_region(df)
    print("\nTop order per region:")
    print(top)


if __name__ == "__main__":
    main()
